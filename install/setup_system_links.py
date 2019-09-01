#!/usr/bin/env python3
from pathlib import Path
from pprint import pprint
import re

scripts_root = Path('home/')
# TODO pozbyć się folderów
files_to_link = list(scripts_root.glob('**/*'))

print(files_to_link)

def map_to_user_home_paths(files_to_link):
    path_strings = [str(path) for path in files_to_link]
    user_home_path = str(Path('~').expanduser())
    #from ptpython.repl import embed
    #embed(globals(), locals())

    return [
        re.sub(f'^home', user_home_path, path)
        for path in path_strings
    ]


# TODO filter out pyc, and bin tests
pprint(map_to_user_home_paths(files_to_link))
