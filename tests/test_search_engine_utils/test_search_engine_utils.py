from unittest import mock
from file_manager import FileManager
from search_engine_utils import (
    display_files_count,
    display_statistics,
    update_letter_count_by_context,
    get_dict_from_index,
)


def test_update_letter_count_by_context():
    content = ["apple: 1,2", "banana: 3,4", "cherry: 5,6"]
    letter_document_count = {"a": set(), "b": set(), "c": set()}

    update_letter_count_by_context(content, letter_document_count)

    assert "1" in letter_document_count["a"]
    assert "3" in letter_document_count["b"]
    assert "5" in letter_document_count["c"]


def test_display_files_count():
    # Мокаем метод read_file
    with mock.patch.object(
        FileManager, "read_file", return_value="file1\nfile2\nfile3"
    ):
        with mock.patch("builtins.print") as mock_print:
            display_files_count("fake/path")
            mock_print.assert_called_once_with("Количество файлов: 3")


def test_display_statistics():
    word_count = 5
    letter_document_count = {"a": {"1", "2"}, "b": {"3", "4"}, "c": {"5", "6"}}

    with mock.patch("builtins.print") as mock_print:
        display_statistics(word_count, letter_document_count)

        mock_print.assert_any_call("Общее количество обнаруженных слов: 5")

        mock_print.assert_any_call("  Буква 'a': 2 документ(ов)")
        mock_print.assert_any_call("  Буква 'b': 2 документ(ов)")
        mock_print.assert_any_call("  Буква 'c': 2 документ(ов)")


def test_get_dict_from_index():
    mock_content = "apple: 1,2\nbanana: 3,4"

    with mock.patch.object(FileManager, "read_file", return_value=mock_content):
        result = get_dict_from_index("fake/path")

        expected_result = {"apple": ["1", "2"], "banana": ["3", "4"]}
        assert result == expected_result
