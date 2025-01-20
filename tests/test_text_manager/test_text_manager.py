from text_manager import TextManager


def test_clean_text():
    input_text = " Hello, World! This is a test - text. It's a test (text) "
    expected_output = "hello world this is a test text its a test text"
    result = TextManager.clean_text(input_text)
    assert result == expected_output


def test_clean_text_with_special_characters():
    input_text = 'This is "quoted" text [and] <special> characters!'
    expected_output = "this is quoted text and special characters"
    result = TextManager.clean_text(input_text)
    assert result == expected_output


def test_clean_text_with_extra_spaces():
    input_text = "This    is   a   test."
    expected_output = "this is a test"
    result = TextManager.clean_text(input_text)
    assert result == expected_output


def test_number_by_letter():
    assert TextManager.number_by_letter("a") == 0
    assert TextManager.number_by_letter("z") == 25

    assert TextManager.number_by_letter("а") == 26
    assert TextManager.number_by_letter("я") == 57

    assert TextManager.number_by_letter("1") == ord("1") - ord("а") + 26


def test_letter_by_number():
    assert TextManager.letter_by_number(0) == "a"
    assert TextManager.letter_by_number(25) == "z"
    assert TextManager.letter_by_number(26) == "а"
    assert TextManager.letter_by_number(57) == "я"
