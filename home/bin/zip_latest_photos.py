#!/usr/bin/env python3
# TODO get that filename from scaleaway
# TODO zip all the audio/video from /storage/9CXXXXXXX/Camera
# the output file needs to be in memory
# TODO send file to scaleaway?
# TODO check file hash to make sure it's not broken

import os
from pathlib import Path
import shlex
import subprocess
import sys
from zipfile import ZipFile


MEDIA_DIR=Path('/storage/0123-4567/DCIM/Camera/')
PC_PHOTOS_DIR='/data/zdjęcia_i_filmiki/z_telefonu_mego/samsung_s7'


def get_latest_photo_on_pc(pc_ip: str) -> str:
    get_photo_command = shlex.split(f'ssh butla@{pc_ip} "~/bin/ostatnia_fota"')
    photo_path = subprocess.check_output(get_photo_command).decode().strip()
    return Path(photo_path).name


def zip_latest_photos(older_than_file_name: str) -> str:
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


def transfer_photos(zip_path:str, pc_ip: str):
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



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Pass the PC IP address')
        exit(1)
    pc_ip = sys.argv[1]
    last_photo = get_latest_photo_on_pc(pc_ip)
    print('Last photo on the PC is', last_photo)
    zip_path = zip_latest_photos(last_photo)

    print('Sha1 sum of the photos archive:')
    subprocess.run(['sha1sum', zip_path])
    input('Press any key to delete the photos archive file...')
    os.unlink(zip_path)
    print('Archive removed.')
    # TODO this doesn't work, because Adroid is a little shit that will kill
    # long network connections no matter what I'm telling it
    #transfer_photos(zip_path, pc_ip)
    #
    #print('Removing the zip file at', zip_path)
    #os.remove(zip_path)
