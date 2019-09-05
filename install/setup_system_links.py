#!/usr/bin/env python3
from dataclasses import dataclass
from pathlib import Path
from pprint import pprint
import re
from typing import List, Iterable


def should_create_link(path):
    return (
        path.is_file() 
        and path.suffix != '.pyc'
        and not str(path).startswith('home/bin/test')
    )


@dataclass
class _SourceToTargetPath:
    source: Path
    target: Path


def map_to_user_home_paths(files_to_link: List[Path]) -> List[Path]:
    user_home_path = str(Path('~').expanduser())

    path_strings = [str(path) for path in files_to_link]
    system_path_strings = [
        re.sub(f'^home', user_home_path, path)
        for path in path_strings
    ]
    system_paths = [Path(path) for path in system_path_strings]

    return [
        _SourceToTargetPath(source, target)
        for source, target in zip(files_to_link, system_paths)
    ]


def ensure_parent_dirs(paths: Iterable[Path]):
    for path in paths:
        if not path.parent.exists():
            print(f'Creating directory: {path.parent}')
            path.parent.mkdir(parents=True)


def backup_existing_targets(paths: Iterable[Path]):
    for path in paths:
        if path.exists():
            print(f'Backing up {path}')
            backup_path = path.with_name(path.name + '.bak')
            #path.replace(backup_path)



def setup_links():
    scripts_root = Path('home/')

    files_and_dirs_to_link = list(scripts_root.glob('**/*'))
    files_to_link = [path for path in files_and_dirs_to_link
                     if should_create_link(path)]

    source_to_target_paths = map_to_user_home_paths(files_to_link)
    target_paths = [pair.target for pair in source_to_target_paths]

    ensure_parent_dirs(target_paths)
    backup_existing_targets(target_paths)

    # TODO create links from files_to_link to target_paths
    # Path.symlink_to



# TODO make sure all parent dirs exist
if __name__ == '__main__':
    setup_links()
