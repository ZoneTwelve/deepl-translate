import argparse
import sys

import deepl
from deepl import __version__
from deepl.utils import read_file_lines, supported_languages

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Python client to translate texts using deepl.com"
    )

    parser.add_argument(
        "--version", action="version", version="%(prog)s {}".format(__version__)
    )
    parser.add_argument(
        "--show-language",
        action="store_true",
        help="Show supported languages",
    )

    parser.add_argument("source_language", nargs="?", help="Source language of your text")
    parser.add_argument("target_language", nargs="?", help="Target language of your desired text")

    parser.add_argument('--lang-legacy', action='store_true', help='Enable legacy language support')

    formality_group = parser.add_mutually_exclusive_group()
    formality_group.add_argument(
        "--formal", help="Use formal tone in translation", action="store_true"
    )
    formality_group.add_argument(
        "--informal", help="Use informal tone in translation", action="store_true"
    )

    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument("-t", "--text", help="Text to be translated")
    input_group.add_argument("-f", "--file", help="File to be translated")

    return parser.parse_args()

def main():
    args = parse_arguments()
    
    if args.show_language:
        supported_languages.show_languages()
        sys.exit(0)
    
    if not args.source_language or not args.target_language:
        print("Error: Both source and target languages are required unless using --show-language")
        sys.exit(1)
    
    source_language = args.source_language
    target_language = args.target_language

    if args.file:
        text = read_file_lines(args.file)
    elif args.text:
        text = args.text
    else:
        print("Error: Either --text or --file must be provided")
        sys.exit(1)

    kwargs = {
        'lang_legacy': args.lang_legacy
    }
    if args.formal:
        kwargs["formality_tone"] = "formal"
    if args.informal:
        kwargs["formality_tone"] = "informal"

    try:
        print(deepl.translate(source_language, target_language, text, **kwargs))
    except AssertionError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
