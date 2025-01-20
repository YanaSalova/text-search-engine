import pytest
from unittest import mock
from file_manager import FileManager
from split_manager import (
    SplitManager,
)


@pytest.fixture
def mock_file_operations():
    with mock.patch.object(FileManager, "read_file") as mock_read_file:
        yield mock_read_file


def test_identifier_file_not_exist(mock_file_operations):
    splits_file = "not-exist.txt"
    mock_file_operations.return_value = None
    result = SplitManager.identifier(splits_file)

    assert result == 1
    mock_file_operations.assert_not_called()


def test_identifier_empty_file(mock_file_operations):
    splits_file = "tests/split_manager/empty.txt"
    mock_file_operations.return_value = ""

    result = SplitManager.identifier(splits_file)

    assert result == 1
    mock_file_operations.assert_called_once_with(splits_file)


def test_identifier_file_with_data(mock_file_operations):
    splits_file = "tests/split_manager/data.txt"
    mock_data = "item1 5\nitem2 10\nitem3 15"
    mock_file_operations.return_value = mock_data
    result = SplitManager.identifier(splits_file)
    assert result == 31
    mock_file_operations.assert_called_once_with(splits_file)
