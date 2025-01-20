from file_manager import FileManager
import os


class SplitManager:

    @staticmethod
    def identifier(splits_file):
        if not os.path.exists(splits_file):
            return 1
        
        total_lines = 0
        lines = FileManager.read_file(splits_file).splitlines()
        for line in lines:
            parts = line.split()
            if len(parts) > 1:
                total_lines += int(parts[1])
        return total_lines + 1
