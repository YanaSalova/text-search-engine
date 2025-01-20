from text_manager import TextManager
from file_manager import FileManager
import os


class IndexManager:
    def __init__(self, index_dir):
        self.index_dir = index_dir

    def _get_index_file(self, letter):
        index = TextManager.number_by_letter(letter)
        return os.path.join(self.index_dir, f"{index:02d}")

    def _update_index(self, letter, data):
        file_path = self._get_index_file(letter)
        if not os.path.exists(file_path):
            self._write_index(file_path, data)
            return

        lines_dict = {}
        lines = FileManager.read_file(file_path).splitlines()

        for line in lines:
            word, indices = line.split(":")
            indices_set = set(indices.strip().split(","))
            lines_dict[word] = indices_set

        updated = False
        for word, indices_set in data.items():
            if word in lines_dict:
                if lines_dict[word] != indices_set:
                    lines_dict[word].update(map(lambda x: str(x), indices_set))
                    updated = True
            else:
                lines_dict[word] = indices_set
                updated = True

        if updated:
            self._write_index(file_path, lines_dict)

    def _write_index(self, file_path, data):
        text_to_record = ""
        for word, indices_set in sorted(data.items()):
            indices = ",".join(map(str, sorted(indices_set)))
            text_to_record += f"{word}: {indices}\n"
        FileManager.write_file(file_path, text_to_record)

    def update_indexes_files(self, data):
        letters = set(word[0] for word in data.keys())
        for letter in letters:
            dict_of_words = {
                key: value for key, value in data.items() if key[0] == letter
            }
            self._update_index(letter, dict_of_words)
