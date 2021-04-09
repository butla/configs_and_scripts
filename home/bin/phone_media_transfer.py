#!/usr/bin/env python3

"""
A script to run on your phone (running in Termux under Android).
"""

# TODO local sync with SFTP to an isolated location on the computer? Some watcher would pick up the files.
# TODO sync to cloud
# - get last filename from scaleaway
# - send encrypted chunks (contain entire photos)
# - encrypted manifest of files
# - can we use minio or nextcloud? Then encryption wouldn't be necessary.
#   - would be nice if VM drive would be encrypted
# TODO make it possible to specify the device by the hostname. Look it up first? How?
# TODO Getting the script args with Typer would be better, but I'd need to package it with the dependencies.
# Or vendor typer into this repo.

import argparse
import shlex
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from zipfile import ZipFile

MEDIA_DIR=Path('/storage/9C33-6BBD/DCIM/Camera/')
# TODO is this the right path?
PC_PHOTOS_DIR='/data/zdjęcia_i_filmiki/z_telefonu_mego/samsung_s10'


def _get_latest_photo_on_pc(pc_ip: str) -> str:
    get_photo_command = shlex.split(f'ssh butla@{pc_ip} "~/bin/ostatnia_fota"')
    photo_path = subprocess.check_output(get_photo_command).decode().strip()
    return Path(photo_path).name


def _transfer_photos(files_to_send: List[Path], pc_ip: str, target_path: str = PC_PHOTOS_DIR):
    # Prepending ./ so that rsync knows this is a local file path.
    # TODO make this timezone aware
    media_list_filename = f'./photos_to_transfer_on_{datetime.now().isoformat()}.txt'
    with open(media_list_filename, 'w') as media_list_file:
        for path in files_to_send:
            # Taking only the name of the file, so that all paths are relative to the media directory,
            # so that rsync won't put the files in any subdirectories.
            # There shouldn't be any subdirectories there.
            media_list_file.write(path.name + '\n')

    print(f'Transferring the files listed in {media_list_filename} with rsync...')
    subprocess.run(
        [
            'rsync', '--update', '--no-owner', '--progress',
            '--files-from', media_list_filename,
            str(MEDIA_DIR), f'butla@{pc_ip}:{target_path}'
        ],
        check=True,
    )


def _get_files_to_send(
        media_folder: Path,
        older_than_file_name: str,
        up_to_file: Optional[str] = None,
) -> List[Path]:
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


def _parse_program_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Transfers media files to another machine.')
    parser.add_argument('pc_ip', type=str,
                        help='IP of the machine we are transferring the photos to')
    parser.add_argument('files_after', nargs='?', type=str, default='',
                        help='Take media files after this one.')
    parser.add_argument('up_to_file', nargs='?', type=str, default='',
                        help='Take media files up to and including this one.')

    return parser.parse_args()


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
    _transfer_photos(files_to_send, pc_ip)

    print('Success!')


if __name__ == '__main__':
    arg_parser = _parse_program_args()
    send_over_wlan(
        pc_ip=arg_parser.pc_ip,
        last_synced_file=arg_parser.files_after,
        up_to_file=arg_parser.up_to_file,
    )
