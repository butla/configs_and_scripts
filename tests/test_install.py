import os
from pathlib import Path

import pytest

from install import setup_system_links
from install.setup_system_links import setup_links


def test_setup_links_creates_the_correct_links(tmp_path):
    # arrange
    # ===========
    source_dir = tmp_path / 'source'
    target_dir = tmp_path / 'target'

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

    # create an empty dir to make sure that it doesn't mess anything up
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


# TODO throw out? Just test the final output
@pytest.mark.parametrize('path_end, should_create', [
    ('bla/whatever.py', True),
    ('ble/something.conf', True),
    ('home/bin/tests/test_bla.py', False),
    ('tests/test_bla.py', False),
    ('bla/whatever.pyc', False),
])
def test_should_ensure_link_function_works_ok_for_files(tmp_path, path_end, should_create):
    path = tmp_path / path_end
    path.parent.mkdir(parents=True)
    path.touch()
    assert setup_system_links.should_ensure_link(path) is should_create


# TODO can be replaced with the single bigger test
def test_directories_should_not_have_links_created(tmp_path):
    directory = tmp_path / 'something'
    directory.mkdir()
    assert not setup_system_links.should_ensure_link(directory)


# TODO can be replaced with the single bigger test
# TODO sample source_dir should be destroyed
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
        # make sure the link is absolute
        assert os.readlink(link) == str(target.absolute())


# TODO test empty multi-level dirs don't create any dirs


def test_old_system_files_are_backed_up_and_replaced_with_links(tmp_path):
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


# TODO instead of checking for additional baks, get a list from glob twice - it should match
def test_dont_do_anything_with_properly_set_up_symlinks(tmp_path):
    source_dir = Path(__file__).parent.parent / 'sample_source_dir'
    target_dir = tmp_path / 'target'

    for _ in range(2):
        setup_system_links.setup_links(
            source_dir=source_dir,
            target_dir=target_dir,
        )

    # no backups were created
    assert not list(target_dir.glob('**/*.bak'))


# TODO test that links to something else that aren't us get backed up.
# Broken links should still get destroyed.


# TODO just have tests for `setup_links` function
# it should create the sample_source_dir
# it should have the case of the empty directory, proving nothing wrong happens

# def test_old_broken_symlinks_are_reported_and_deleted_during_setup(tmp_path):
#     source_dir = 
