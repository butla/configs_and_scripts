import os
from pathlib import Path

import pytest

from install.setup_system_links import setup_links


@pytest.fixture
def source_dir(tmp_path):
    return tmp_path / 'source'


@pytest.fixture
def target_dir(tmp_path):
    return tmp_path / 'target'


def test_setup_links_creates_the_correct_links(source_dir: Path, target_dir: Path):
    # arrange
    # ===========
    source_file_that_should_have_links = [
        'aaa.py',
        'a_dir/bbb.py',
        'b_dir/c_dir/ccc.conf',
        'b_dir/c_dir/ddd',
    ]
    source_files_that_should_not_have_links = [
        'tests/eee.py',
        'd_dir/tests/fff.py',
    ]

    # create the source files
    for path_str in source_file_that_should_have_links + source_files_that_should_not_have_links:
        path = Path(source_dir) / path_str
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('Just the file content')

    # create a multi-level empty dir to make sure that it doesn't mess anything up
    (Path(source_dir) / 'e_dir/f_dir/g_dir').mkdir(parents=True)

    # act
    # ===========
    setup_links(
        source_dir=source_dir,
        target_dir=target_dir,
    )

    # assert
    # ===========
    target_dir_expected_dirs = {
        Path(target_dir) / 'a_dir',
        Path(target_dir) / 'b_dir',
        Path(target_dir) / 'b_dir/c_dir',
    }
    target_dir_expected_files = {Path(target_dir) / file for file in source_file_that_should_have_links}
    target_dir_contents = set(target_dir.glob('**/*'))

    # assert we have the expected folders and links created
    assert target_dir_contents == target_dir_expected_dirs | target_dir_expected_files

    # assert the created links have expected targets
    expected_link_targets = {str(Path(source_dir) / file) for file in source_file_that_should_have_links}
    created_links_targets = {os.readlink(item) for item in target_dir_contents if item.is_symlink()}
    assert created_links_targets == expected_link_targets


def test_old_system_files_are_backed_up_and_replaced_with_links(source_dir: Path, target_dir: Path):
    source_file_content = 'Just some file content'
    source_file = source_dir / 'bla/whatever.py'
    source_file.parent.mkdir(parents=True)
    source_file.write_text(source_file_content)

    old_system_file_content = "I'm the old thing"
    old_system_file = target_dir / 'bla/whatever.py'
    old_system_file.parent.mkdir(parents=True)
    old_system_file.write_text(old_system_file_content)

    setup_links(
        source_dir=source_dir,
        target_dir=target_dir,
    )

    assert old_system_file.with_name('whatever.py.bak').read_text() == old_system_file_content


def test_nothing_gets_changed_on_second_pass_of_setup_links(source_dir, target_dir):
    source_file = source_dir / 'aaa'
    source_file.parent.mkdir()
    source_file.write_text('some content')

    setup_links(
        source_dir=source_dir,
        target_dir=target_dir,
    )

    expected_link = target_dir / 'aaa'
    expected_target_dir_contents = [expected_link]
    assert list(target_dir.glob('**/*')) == expected_target_dir_contents
    assert os.readlink(expected_link) == str(source_file)

    # run again
    setup_links(
        source_dir=source_dir,
        target_dir=target_dir,
    )

    assert list(target_dir.glob('**/*')) == expected_target_dir_contents
    assert os.readlink(expected_link) == str(source_file)


# TODO test that links to something else that aren't us get backed up.
# Broken links should still get destroyed.


# def test_old_broken_symlinks_are_reported_and_deleted_during_setup(tmp_path):
#     source_dir = 
