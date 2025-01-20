import re


class TextManager:
    @staticmethod
    def clean_text(text):
        text = re.sub(r"[\"'()\[\]{}<>«»]", "", text)
        text = re.sub(r"[.,!?;:]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        text = re.sub(r"(\w+)'s?\b[.,;!?\s]*", r"\1 ", text)
        text = re.sub(r"(?<=\S)-(?=\S)", " ", text)
        text = re.sub(r"\s*-\s*", " ", text)
        return text.strip().lower()

    @staticmethod
    def number_by_letter(letter):
        if "a" <= letter <= "z":
            return ord(letter) - ord("a")
        return ord(letter) - ord("а") + 26

    @staticmethod
    def letter_by_number(number):
        if number < 26:
            return chr(number + ord("a"))
        return chr(number - 26 + ord("а"))
