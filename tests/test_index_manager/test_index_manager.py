import pytest
from unittest import mock
import os
from index_manager import (
    IndexManager,
)
from file_manager import FileManager
from text_manager import TextManager


@pytest.fixture
def mock_file_operations():
    with mock.patch.object(
        FileManager, "read_file"
    ) as mock_read_file, mock.patch.object(
        FileManager, "write_file"
    ) as mock_write_file, mock.patch.object(
        TextManager, "number_by_letter"
    ) as mock_number_by_letter:
        yield mock_read_file, mock_write_file, mock_number_by_letter


def test_get_index_file(mock_file_operations):
    _, _, mock_number_by_letter = mock_file_operations
    mock_number_by_letter.return_value = 1
    mock_path = "/some/index/dir"
    index_manager = IndexManager(mock_path)
    result = index_manager._get_index_file("a")
    assert result == os.path.join(mock_path, "01")
    mock_number_by_letter.assert_called_once_with("a")


def test_write_index(mock_file_operations):
    mock_write_file = mock_file_operations[1]
    data = {"apple": {"1", "2"}, "banana": {"3", "4"}}
    index_manager = IndexManager("/some/index/dir")

    index_manager._write_index("/some/index/dir/01", data)

    mock_write_file.assert_called_once_with(
        "/some/index/dir/01", "apple: 1,2\nbanana: 3,4\n"
    )
