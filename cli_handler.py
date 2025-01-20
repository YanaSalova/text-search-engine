from search_engine import SearchEngine
import argparse


class CLIHandler:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Search Engine")
        self._setup_arguments()

    def _setup_arguments(self):
        subparsers = self.parser.add_subparsers(dest="command")

        init_parser = subparsers.add_parser("init", help="Initialize search engine")
        init_parser.add_argument("--root", required=True, type=str)
        init_parser.add_argument("--drop-existing", action="store_true")

        add_parser = subparsers.add_parser("add", help="Add files to search engine")
        add_parser.add_argument("--root", required=True, type=str)
        add_parser.add_argument("filenames", nargs="+")

        info_parser = subparsers.add_parser(
            "info", help="Вывести информацию о файлах и словах"
        )

        info_parser.add_argument(
            "--root", type=str, required=True, help="Корневой каталог"
        )

        find_parser = subparsers.add_parser("find", help="Поиск файлов по словам")
        find_parser.add_argument(
            "--root", type=str, required=True, help="Корневой каталог"
        )
        find_parser.add_argument("words", type=str, nargs="+", help="Список слов")
        find_parser.add_argument(
            "--limit", type=int, nargs="?", help="Ограничение вывода"
        )

    def execute(self):
        args = self.parser.parse_args()
        engine = SearchEngine(args.root)
        if args.command == "init":
            engine.initialize(drop_existing=args.drop_existing)
        elif args.command == "add":
            engine.add_files(args.filenames)
        elif args.command == "info":
            engine.info()
        elif args.command == "find":
            engine.find(args.words, args.limit)
