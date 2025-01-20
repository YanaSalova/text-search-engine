import os
import tempfile
import pytest
from search_engine import SearchEngine


@pytest.fixture
def temp_search_engine():

    with tempfile.TemporaryDirectory() as temp_dir:
        yield SearchEngine(temp_dir)


def test_create_search_engine_directory(temp_search_engine):
    search_engine = temp_search_engine

    search_engine.create_search_engine_directory()

    assert os.path.exists(search_engine.root)
    assert os.path.exists(search_engine.index_dir)
    assert os.path.exists(search_engine.files_dir)
    assert os.path.isfile(search_engine.se_file)
    assert os.path.isfile(search_engine.splits_file)


def test_check_directory_valid(temp_search_engine):
    search_engine = temp_search_engine
    search_engine.create_search_engine_directory()

    search_engine.check_directory()


def test_check_directory_invalid(temp_search_engine):
    search_engine = temp_search_engine

    with pytest.raises(FileNotFoundError):
        search_engine.check_directory()


def test_initialize_with_existing_directory(temp_search_engine):
    search_engine = temp_search_engine
    search_engine.create_search_engine_directory()

    with pytest.raises(FileExistsError):
        search_engine.initialize()


def test_add_files(temp_search_engine):
    search_engine = temp_search_engine
    search_engine.create_search_engine_directory()

    test_file1 = os.path.join(search_engine.root, "test1.txt")
    test_file2 = os.path.join(search_engine.root, "test2.txt")
    with open(test_file1, "w") as f:
        f.write("word1 word2 word3")
    with open(test_file2, "w") as f:
        f.write("word3 word4 word5")

    search_engine.add_files([test_file1, test_file2])

    files = os.listdir(search_engine.files_dir)
    assert any("0_files" in file for file in files)
    assert os.path.isfile(search_engine.splits_file)


def test_find_no_results(temp_search_engine):
    search_engine = temp_search_engine
    search_engine.create_search_engine_directory()

    result = search_engine.find_word("nonexistent")
    assert result == []


def test_get_file_by_index(temp_search_engine):
    search_engine = temp_search_engine
    search_engine.create_search_engine_directory()

    test_file = os.path.join(search_engine.root, "test.txt")
    with open(test_file, "w") as f:
        f.write("word1")

    search_engine.add_files([test_file])

    file_path, idx = search_engine.get_file_by_index(0)
    assert os.path.exists(file_path)
