from pathlib import Path

import pytest

from install import setup_system_links


@pytest.mark.parametrize('path_end, should_create', [
    ('bla/whatever.py', True),
    ('home/bin/tests/test_bla.py', False),
    ('tests/test_bla.py', False),
    ('bla/whatever.pyc', False),
])
def test_choose_files_to_create_links_for(tmp_path, path_end, should_create):
    path = tmp_path / path_end
    path.parent.mkdir(parents=True)
    path.touch()
    assert setup_system_links.should_create_link(path) is should_create


def test_directories_should_not_have_links_created(tmp_path):
    directory = tmp_path / 'something'
    directory.mkdir()
    assert not setup_system_links.should_create_link(directory)


def test_system_symlinks_are_created(tmp_path):
    source_dir = Path(__file__).parent.parent / 'sample_source_dir'
    target_dir = tmp_path / 'target'

    setup_system_links.setup_links(
        source_dir=source_dir,
        target_dir=target_dir,
    )

    links_to_create = [
        (target_dir / '1.py', source_dir / '1.py'),
        (target_dir / 'a_dir/2.py', source_dir / 'a_dir/2.py'),
    ]
    for link, target in links_to_create:
        assert link.exists()
        assert link.is_symlink()
        assert link.resolve() == target.absolute()


def test_old_system_files_are_backed_up_replaced_with_links(tmp_path):
    source_dir = tmp_path / 'source'
    links_dir = tmp_path / 'target'

    source_file_content = 'Just some file content'
    source_file = source_dir / 'bla/whatever.py'
    source_file.parent.mkdir(parents=True)
    source_file.write_text(source_file_content)

    old_system_file_content = "I'm the old thing"
    old_system_file = links_dir / 'bla/whatever.py' 
    old_system_file.parent.mkdir(parents=True)
    old_system_file.write_text(old_system_file_content)

    setup_system_links.setup_links(
        source_dir=source_dir,
        target_dir=links_dir,
    )

    assert old_system_file.with_name('whatever.py.bak').read_text() == old_system_file_content
