#!/usr/bin/env python3
from dataclasses import dataclass
from pathlib import Path
import re
from typing import List, Iterable


def should_create_link(path):
    return (
        path.is_file()
        and path.suffix != '.pyc'
        and 'tests/' not in str(path)
    )


@dataclass
class _LinkToCreate:
    target: Path
    location: Path


def get_links_to_create(
        files_to_link: List[Path],
        files_dir: Path,
        links_location: Path,
) -> List[_LinkToCreate]:
    file_path_strings = [str(path) for path in files_to_link]
    link_path_strings = [
        re.sub(f'^{files_dir}', str(links_location), path)
        for path in file_path_strings
    ]
    link_paths = [Path(path) for path in link_path_strings]

    initial_links = [
        _LinkToCreate(target=link_target, location=link_path)
        for link_target, link_path in zip(files_to_link, link_paths)
    ]
    return [link for link in initial_links if not _is_link_set_up(link)]


def _is_link_set_up(link: _LinkToCreate):
    """Prevents us doing anything if the link is already set up.
    """
    if link.location.exists() and link.location.is_symlink():
        if link.location.resolve() == link.target.absolute():
            return True
    return False


def ensure_parent_dirs(paths: Iterable[Path]):
    for path in paths:
        if not path.parent.exists():
            print(f'Creating directory: {path.parent}')
            path.parent.mkdir(parents=True)


def backup_and_remove_existing_targets(paths: Iterable[Path]):
    for path in paths:
        if path.exists():
            print(f'Backing up {path}')
            backup_path = path.with_name(path.name + '.bak')
            path.replace(backup_path)


def setup_links(source_dir: Path, target_dir: Path):
    source_dir = source_dir.absolute()
    target_dir = target_dir.absolute()

    files_and_dirs_to_link = list(source_dir.glob('**/*'))
    files_to_link = [path for path in files_and_dirs_to_link
                     if should_create_link(path)]

    links_to_create = get_links_to_create(
        files_to_link=files_to_link,
        files_dir=source_dir,
        links_location=target_dir,
    )
    link_paths = [link.location for link in links_to_create]

    ensure_parent_dirs(link_paths)
    backup_and_remove_existing_targets(link_paths)

    for link_to_create in links_to_create:
        print('Creating the link at', link_to_create.location)
        link_to_create.location.symlink_to(link_to_create.target)


if __name__ == '__main__':
    setup_links(
        source_dir=Path('home/'),
        target_dir=Path('~').expanduser(),
    )
    # TODO make sure the files here are chmod 600
    setup_links(
        source_dir=Path('configs_private/home/'),
        target_dir=Path('~').expanduser(),
    )
