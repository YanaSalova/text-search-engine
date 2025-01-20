from file_manager import FileManager
from text_manager import TextManager
from index_manager import IndexManager
from split_manager import SplitManager
from collections import defaultdict
import os

from search_engine_utils import (
    display_files_count,
    display_statistics,
    update_letter_count_by_context,
    get_dict_from_index,
)


class SearchEngine:
    def __init__(self, root):
        self.root = root
        self.index_dir = os.path.join(root, "index")
        self.files_dir = os.path.join(root, "files")
        self.se_file = os.path.join(root, ".se")
        self.splits_file = os.path.join(self.files_dir, ".splits")
        self.files_0 = os.path.join(self.files_dir, "0_files")

        self._search_engine_key = "IT'S SEARCH ENGINE"
        self.initial_splits_state = "0 0\n"

        self._split_max_size = 16

    def create_search_engine_directory(self, drop=False):
        FileManager.ensure_directory_exists(self.root)
        FileManager.ensure_directory_exists(self.index_dir, drop)
        FileManager.ensure_directory_exists(self.files_dir, drop)
        FileManager.write_file(self.se_file, self._search_engine_key)
        FileManager.write_file(self.splits_file, self.initial_splits_state)
        FileManager.write_file(self.files_0)

    def check_directory(self, check_existanse=False):
        if (not os.path.exists(self.root)) and check_existanse:
            raise FileExistsError(f"{self.root} not exist.")
        if os.path.isfile(self.root):
            raise IsADirectoryError(f"{self.root} is a file, not a directory.")
        if not os.path.isfile(self.se_file):
            raise FileNotFoundError(f"{self.se_file} not found.")
        if FileManager.read_file(self.se_file) != self._search_engine_key:
            raise ValueError(
                f"{self.se_file} doesn't contain the expected search engine key."
            )

    def validate_paths(self):
        self.check_directory(check_existanse=True)
        if not os.path.isdir(self.index_dir):
            raise IsADirectoryError(f"{self.index_dir} directory not exist.")
        if len(os.listdir(self.index_dir)) <= 1:
            raise FileExistsError("No files added yet.")

    def files_to_add(self, paths):
        files = os.listdir(self.files_dir)
        files.remove(".splits")
        paths_to_remove = set()
        for f in files:
            if len(paths) == 0:
                break
            content = FileManager.read_file(os.path.join(self.files_dir, f))
            for path in paths:
                if path in content:
                    print(f"{path} already added")
                    paths_to_remove.add(path)
        return [item for item in paths if path not in paths_to_remove]

    def initialize(self, drop_existing=False):
        if not os.path.exists(self.root):
            self.create_search_engine_directory()
            return

        self.check_directory()

        if not drop_existing:
            raise FileExistsError(
                f"{self.root} already exists as search engine directory."
            )

        self.create_search_engine_directory(drop=True)

    def add_files(self, filenames):
        self.check_directory(check_existanse=True)

        index_manager = IndexManager(self.index_dir)
        canon_paths = FileManager.transform_to_canon_path(filenames)
        canon_paths = self.files_to_add(canon_paths)

        list_of_files = sorted(os.listdir(self.files_dir))
        list_of_files.remove(".splits")
        file_to_record = list_of_files[-1]

        words_to_identifiers = self.preprocess_words(canon_paths, file_to_record)
        index_manager.update_indexes_files(words_to_identifiers)

    def preprocess_words(self, canon_paths, file_to_record):
        identifier = SplitManager.identifier(self.splits_file)
        path_to_record = os.path.join(self.files_dir, file_to_record)
        data = defaultdict(set)

        for canon_path in canon_paths:
            idx, suffix = file_to_record.split("_")

            if FileManager.size_of_file(path_to_record) > self._split_max_size:
                idx = int(idx) + 1
                file_to_record = f"{idx}_{suffix}"
                path_to_record = os.path.join(self.files_dir, file_to_record)
                FileManager.create_empty_file(path_to_record)
                FileManager.append_file(self.splits_file, f"{idx} 0")

            FileManager.rewrite_line_by_index(self.splits_file, idx)
            FileManager.append_file(path_to_record, f"{identifier} {canon_path}\n")
            content = FileManager.read_file(canon_path)
            words = set(TextManager.clean_text(content).split())

            for word in words:
                data[word].add(identifier)
            identifier += 1

        return data

    def info(self):
        self.validate_paths()
        display_files_count(self.splits_file)

        word_count = 0
        letter_document_count = defaultdict(set)

        for index_file in os.listdir(self.index_dir):
            file_path = os.path.join(self.index_dir, index_file)
            content = FileManager.read_file(file_path).replace(" ", "").splitlines()
            word_count += len(content)
            update_letter_count_by_context(content, letter_document_count)

        display_statistics(word_count, letter_document_count)

    def find_word(self, word):
        letter = word[0]
        idx = str(TextManager.number_by_letter(letter))

        if len(idx) == 1:
            idx = "0" + idx
        path = os.path.join(self.index_dir, idx)
        if not os.path.exists(path):
            return []

        content = get_dict_from_index(path)

        if word not in content:
            return []
        return content[word]

    def get_file_by_index(self, idx):
        content = FileManager.read_file(self.splits_file).splitlines()
        for line in content:
            split_id, id_count = line.split()
            if idx <= int(id_count):
                return os.path.join(self.files_dir, split_id + "_files"), idx
            idx -= int(id_count)
        raise FileNotFoundError(f"No file by index {idx}")

    def get_path_by_idx(self, idx):
        file_path, shift = self.get_file_by_index(idx)
        content = FileManager.read_file(file_path).splitlines()
        _, path = content[shift - 1].split()
        return path

    def find(self, words, limit=100):
        self.check_directory(check_existanse=True)

        candidates_set = set()
        for word in words:
            ids = self.find_word(word)
            if not ids:
                return []

            if not candidates_set:
                candidates_set = set(ids)
                continue

            candidates_set = candidates_set.intersection(ids)

            if not candidates_set:
                return []

        candidates = list(candidates_set)[:limit]
        paths = list(map(lambda idx: self.get_path_by_idx(int(idx) - 1), candidates))
        print(", ".join(paths))
        return paths
