from contextlib import contextmanager
import os
import pytest
import medvision as mv


DATA_DIR = mv.joinpath(mv.parentdir(__file__), 'data')
DCM_DIR = mv.joinpath(DATA_DIR, 'dicoms')
PNG_DIR = mv.joinpath(DATA_DIR, 'pngs')


@contextmanager
def not_raises(exception):
    try:
        yield
    except exception:
        raise pytest.fail("DID RAISE {0}".format(exception))


def test_mkdirs():
    with not_raises(FileExistsError):
        mv.mkdirs(DATA_DIR)

    path = mv.joinpath(DATA_DIR, 'temporary_subdir')
    mv.mkdirs(path)
    assert mv.isdir(path)
    mv.rmtree(path)


def test_copyfiles():
    dst_dir = mv.joinpath(DATA_DIR, 'temporary_subdir')
    mv.mkdirs(dst_dir)

    src_paths = ['brain_001.dcm', 'brain_002.dcm']
    mv.copyfiles(src_paths, dst_dir, DCM_DIR)
    assert len(mv.listdir(dst_dir)) == 2

    with not_raises(FileExistsError):
        mv.copyfiles(src_paths, dst_dir, DCM_DIR, non_overwrite=False)

    with pytest.raises(FileExistsError):
        mv.copyfiles(src_paths, dst_dir, DCM_DIR, non_overwrite=True)

    mv.empty_dir(dst_dir)
    assert mv.isdir(dst_dir)
    assert len(mv.listdir(dst_dir)) == 0
    mv.rmtree(dst_dir)


def test_glob_file():
    filepaths = mv.glob(DATA_DIR, '*.png', mode=mv.GlobMode.FILE,
                        recursive=True)
    assert len(filepaths) == 16

    filepaths = mv.glob(DATA_DIR, '*.png', mode=mv.GlobMode.FILE,
                        recursive=False)
    assert len(filepaths) == 0

    filepaths = mv.glob(PNG_DIR, '*.png', mode=mv.GlobMode.FILE,
                        recursive=False)
    assert len(filepaths) == len(mv.listdir(PNG_DIR))


def test_glob_dir():
    root = DATA_DIR
    filepaths = mv.glob(root, '*png*', mode=mv.GlobMode.DIR, recursive=True)
    assert len(filepaths) == 1

    root = DATA_DIR
    filepaths = mv.glob(root, '*', mode=mv.GlobMode.DIR, recursive=True)
    assert len(filepaths) == 8
