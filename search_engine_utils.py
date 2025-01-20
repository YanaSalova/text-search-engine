from file_manager import FileManager


def update_letter_count_by_context(content, letter_document_count):
    for line in content:
        word, identifiers = line.split(":")
        for identifier in identifiers.split(","):
            identifier = identifier.strip()
            if identifier:
                letter_document_count[word[0]].add(identifier)


def display_files_count(splits_file):
    lines = FileManager.read_file(splits_file).splitlines()
    file_count = 0
    for line in lines:
        file_count += int(line.split()[1])
    print(f"Количество файлов: {file_count}")


def display_statistics(word_count, letter_document_count):
    print(f"Общее количество обнаруженных слов: {word_count}")
    print("Документы по первой букве слов:")
    for letter, docs in sorted(letter_document_count.items()):
        print(f"  Буква '{letter}': {len(docs)} документ(ов)")


def get_dict_from_index(path):
    content = FileManager.read_file(path)
    lines = content.replace(" ", "").splitlines()
    result = dict()
    for line in lines:
        key, value = line.split(":")
        result[key] = value.split(",")
    return result
