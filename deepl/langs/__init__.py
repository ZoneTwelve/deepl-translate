import os
import yaml

import importlib.util

from typing import Optional, Union, List, Literal
import collections

class LanguageManager:
    def __init__(
        self,
        include_path: Optional[Union[str, List]] = None,
        include_default: bool = True,
        allow_overwrite: bool = True,
    ):
        self.include_path = include_path

        self._language_index, self._group = self.initialize(
            include_path=include_path,
            include_default=include_default,
            allow_overwrite=allow_overwrite,
        )

    @property
    def group(self):
        return self._group

    @property
    def languages(self): # slow
        return self._language_index
        # return list(self._group.keys())

    def show_languages(self):
        languages_dict = {}
        for code, info in self._language_index.items():
            language_name = info['config']['name'] if 'name' in info['config'] else info['config']['language']
            if language_name not in languages_dict:
                languages_dict[language_name] = set()
            languages_dict[language_name].add(code)
            languages_dict[language_name].update(info['config'].get('keywords', []))

        for language, keywords in languages_dict.items():
            print(f"{language}:")
            for keyword in sorted(keywords):
                print(f"* {keyword}")
            print()  # Add a blank line between languages

    def __getitem__(self, key):
        return self._language_index[key] if key in self._language_index else None

    def initialize(
        self,
        include_path: Optional[Union[str, List]] = None,
        include_default: bool = True,
        allow_overwrite: bool = True,
    ):
        if include_default:
            all_paths = [os.path.dirname(os.path.abspath(__file__)) + "/"]
        else:
            all_paths = []

        code_index = []
        lang_index = {}
        group_index = {}

        if include_path is not None:
            if isinstance(include_path, str):
                include_path = [include_path]
            all_paths.extend(include_path)
        
        for lang_dir in all_paths:
            langs, group, code = self._get_language_config(lang_dir)
            code_index.extend(code)
            lang_index = {**langs, **lang_index}
            group_index = {**group, **group_index}

        return lang_index, group_index

    def _get_language_config(
            self,
            lang_dir: str,
            allow_overwrite: bool = True
    ):
        languages = collections.defaultdict()
        group = collections.defaultdict(list)
        codes = []
        ignore_dirs = [
            "__pycache__",
        ]
        dirs = dirs[:] = [d for d in os.listdir(lang_dir) if d not in ignore_dirs]
        for _lang in dirs:
            d = os.path.join(lang_dir, _lang)
            if os.path.isdir(d):
                for f in os.listdir(d):
                    yaml_path = os.path.join(d, f)
                    config = load_yaml_config(yaml_path, mode='safe')
                    lang = config['language'].lower()
                    code = config['code'].lower()
                    codes.append(code)
                    group[_lang].append(lang)
                    languages[lang] = {
                        "config": config,
                        "yaml_path": yaml_path,
                    }
                    languages[code] = languages[lang]
                    for keyword in config['keywords']:
                        # If is now allow to overwrite the keyword, that just continue to the next keyword
                        # Warning: this default allow to overwrite other config by keyword
                        if not allow_overwrite and keyword not in languages:
                            continue
                        languages[keyword] = languages[lang]

        return languages, group, codes


def load_yaml_config(yaml_path=None, yaml_config=None, yaml_dir=None, mode: Literal["safe", "full"] = "full"):
    # Added an if-else case in the pick construct function
    constructor_fn = import_function if mode != "full" else ignore_constructor

    # Add the import_function constructor to the YAML loader
    yaml.add_constructor("!function", constructor_fn)
    if yaml_config is None:
        with open(yaml_path, "rb") as file:
            yaml_config = yaml.full_load(file)

    if yaml_dir is None:
        yaml_dir = os.path.dirname(yaml_path)

    assert yaml_dir is not None
    return yaml_config


def ignore_constructor(loader, node):
    return node

def import_function(loader, node):
    function_name = loader.construct_scalar(node)
    yaml_path = os.path.dirname(loader.name)

    *module_name, function_name = function_name.split(".")
    if isinstance(module_name, list):
        module_name = ".".join(module_name)
    module_path = os.path.normpath(os.path.join(yaml_path, "{}.py".format(module_name)))

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    function = getattr(module, function_name)
    return function


# The language management is inspired by EleutherAI’s lm-evaluation-harness