from deepl.settings import SUPPORTED_LANGUAGES
from deepl.langs import LanguageManager # This might hurt the performance
from typing import Optional, Union, Dict

supported_languages = LanguageManager()

def create_abbreviations_dictionary_legacy(languages: Optional[Union[Dict, LanguageManager]]=SUPPORTED_LANGUAGES):
    short_dict = {language["code"].lower(): language["code"] for language in languages}
    verbose_dict = {
        language["language"].lower(): language["code"] for language in languages
    }
    return {
        **short_dict,
        **verbose_dict,
    }

def create_abbreviations_dictionary(languages: Optional[Union[Dict, LanguageManager]]=supported_languages):
    return supported_languages.languages


def abbreviate_language(language, legacy: bool = False):
    language = language.lower()
    if legacy:
        abbreviations = create_abbreviations_dictionary_legacy()
    else:
        # Temporary adjustment to align with the original format
        abbreviations = create_abbreviations_dictionary()
    return abbreviations.get(language)


def read_file_lines(path):
    with open(path, "r") as file:
        return "\n".join(file.readlines())
