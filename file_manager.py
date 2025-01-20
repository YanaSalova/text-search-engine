import os
import shutil


class FileManager:
    @staticmethod
    def ensure_directory_exists(path, clear=False):
        if clear and os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path, exist_ok=True)

    @staticmethod
    def create_empty_file(path):
        open(path, "w").close()

    @staticmethod
    def read_file(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def write_file(path, content=""):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    @staticmethod
    def append_file(path, content):
        with open(path, "a", encoding="utf-8") as f:
            f.write(content)

    @staticmethod
    def transform_to_canon_path(paths):
        abs_paths = [os.path.abspath(path) for path in paths]
        return [os.path.normpath(abs_path) for abs_path in abs_paths]

    @staticmethod
    def rewrite_line_by_index(file_path, index):
        temp_file = file_path + ".tmp"
        with open(file_path, "r") as f_in, open(temp_file, "w") as f_out:
            for i, line in enumerate(f_in):
                if i == int(index):
                    parts = line.split()
                    if len(parts) > 1:
                        new_count = int(parts[1]) + 1
                        f_out.write(f"{parts[0]} {new_count}\n")
                    else:
                        f_out.write(line)
                else:
                    f_out.write(line)
        shutil.move(temp_file, file_path)

    def size_of_file(file_path):
        file_size_bytes = os.path.getsize(file_path)
        return file_size_bytes / (1024 * 1024)
