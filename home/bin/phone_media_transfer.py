#!/usr/bin/env python3

"""
A script to run on your phone (running in Termux under Android).
"""

# TODO prepare a list of files for rsync
# - save that list with date

# TODO sync to cloud
# - get that filename from scaleaway
# - send encrypted chunks (contain entire photos)
# - encrypted manifest of files
# - can we use minio or nextcloud? Then encryption wouldn't be necessary.
#   - would be nice if VM drive would be encrypted

# TODO up
# TODO zip all the audio/video from /storage/9CXXXXXXX/Camera
# the output file needs to be in memory
# TODO send file to scaleaway?
# TODO check file hash to make sure it's not broken

import argparse
import shlex
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional
from zipfile import ZipFile

MEDIA_DIR=Path('/storage/0123-4567/DCIM/Camera/')
PC_PHOTOS_DIR='/data/zdjęcia_i_filmiki/z_telefonu_mego/samsung_s7'


def _get_latest_photo_on_pc(pc_ip: str) -> str:
    get_photo_command = shlex.split(f'ssh butla@{pc_ip} "~/bin/ostatnia_fota"')
    photo_path = subprocess.check_output(get_photo_command).decode().strip()
    return Path(photo_path).name


def _zip_latest_photos(older_than_file_name: str) -> str:
    new_photos = [path for path in MEDIA_DIR.iterdir()
                  if path.name > older_than_file_name]
    start_file_name = older_than_file_name.replace('.', '_')
    zip_name = f'/sdcard/Download/photos_from_{start_file_name}.zip'

    print(f'Zipping {len(new_photos)} photos from {str(MEDIA_DIR)} to {zip_name}')
    with ZipFile(zip_name, mode='w') as zip_file:
        for path in new_photos:
            zip_file.write(
                str(path),
                arcname=path.name,
            )

    return zip_name


def _transfer_photos(zip_path:str, pc_ip: str):
    print("Transferring photos' zip")
    subprocess.run(
        shlex.split(f'scp {zip_path} butla@{pc_ip}:{PC_PHOTOS_DIR}'),
        check=True,
    )

    print("Unpacking the photos")
    zip_file_name = Path(zip_path).name
    remote_commands = f'cd {PC_PHOTOS_DIR}; unzip {zip_file_name}; rm {zip_file_name}'
    subprocess.run(
        shlex.split(f'ssh butla@{pc_ip} "{remote_commands}"'),
        check=True,
    )

    print("All done")


def _get_files_to_send(
        media_folder: Path,
        older_than_file_name: str,
        up_to_file: Optional[str] = None,
):
    """
    Args:
        media_folder: folder we'll take the media files from
        older_than_file_name: this file name won't be included in the set
        up_to_file: this file will be included in the set
    """
    files_without_upper_boundary = (
        path for path in media_folder.iterdir()
        if path.name > older_than_file_name
    )
    if up_to_file:
        return [path for path in files_without_upper_boundary if path.name <= up_to_file]
    return list(files_without_upper_boundary)


# TODO Would be better with typer, but I'd need to package it with the dependencies.
# Or vendor typer into this repo.
def _parse_program_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Transfers media files to another machine.')
    parser.add_argument('pc_ip', type=str,
                        help='IP of the machine we are transferring the photos to')
    parser.add_argument('files_after', nargs='?', type=str, default='',
                        help='Take media files after this one.')
    parser.add_argument('up_to_file', nargs='?', type=str, default='',
                        help='Take media files up to and including this one.')

    return parser.parse_args()


# TODO make it possible to specify the device by the hostname. Look it up first? How?
def send_over_wlan(
        pc_ip: str,
        last_synced_file: Optional[str] = None,
        up_to_file: Optional[str] = None,
):
    if not last_synced_file:
        print('Checking the last photo on the PC...')
        last_synced_file = _get_latest_photo_on_pc(pc_ip)
        print('Last photo on the PC is', last_synced_file)

    up_to_file_message = up_to_file if up_to_file else 'latest'
    print('Syncing photos coming after', last_synced_file, 'up to', up_to_file_message)

    files_to_send = _get_files_to_send(
        media_folder=MEDIA_DIR,
        older_than_file_name=last_synced_file,
        up_to_file=up_to_file,
    )

    # TODO make this timezone aware
    media_list_filename = f'photos_to_transfer_on_{datetime.now().isoformat()}.txt'
    with open(media_list_filename, 'w') as media_list_file:
        media_list_file.writelines(str(path) for path in files_to_send)

    print(f'Transferring the files listed in {media_list_filename} with rsync...')
    subprocess.run(
        [
            'rsync', '--update', '--no-owner', '-v'
            f'--files-from={media_list_filename}',
            MEDIA_DIR, 'butla@{pc_ip}:{PC_PHOTOS_DIR}'
        ],
        check=True,
    )
    print('Success!')
    # TODO get the files, save to a file, use it in files from
    # rsync --archive --update --no-owner --files-from=rsync_list.txt --dry-run -vv rsync_source/ rsync_target/

    # zip_path = _zip_latest_photos(last_synced_photo)

    # print('Sha1 sum of the photos archive:')
    # subprocess.run(['sha1sum', zip_path], check=True)
    # input('Press any key to delete the photos archive file...')
    # os.unlink(zip_path)
    # print('Archive removed.')


if __name__ == '__main__':
    arg_parser = _parse_program_args()
    send_over_wlan(
        pc_ip=arg_parser.pc_ip,
        last_synced_file=arg_parser.files_after,
        up_to_file=arg_parser.up_to_file,
    )

    # TODO this doesn't work, because Android is a little shit that will kill
    # long network connections no matter what I'm telling it
    # transfer_photos(zip_path, pc_ip)
    #
    # print('Removing the zip file at', zip_path)
    # os.remove(zip_path)
