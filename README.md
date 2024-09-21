# DeepL Translate

[![PyPI version](https://badge.fury.io/py/deepl-translate.svg)](https://badge.fury.io/py/deepl-translate)
[![Python Package](https://github.com/ptrstn/deepl-translate/actions/workflows/python-package.yml/badge.svg)](https://github.com/ptrstn/deepl-translate/actions/workflows/python-package.yml)
[![codecov](https://codecov.io/gh/ptrstn/deepl-translate/branch/master/graph/badge.svg)](https://codecov.io/gh/ptrstn/deepl-translate)
[![Downloads](https://pepy.tech/badge/deepl-translate)](https://pepy.tech/project/deepl-translate)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

An unofficial Python package for translating text using [DeepL](https://www.deepl.com/), now with improved language management and legacy support.

## Installation

```bash
pip install deepl-translate
```

## Usage

### Supported Languages

DeepL Translate supports a wide range of languages. You can use either the language abbreviation or the full name in English. For a complete list of supported languages, please refer to the [language configuration files](deepl/langs/).

### Command Line Tool

#### Basic Usage

```bash
deepl <source_language> <target_language> [options] -t "Text to translate"
```
- Legacy language management support: Use the `--lang-legacy` flag for backward compatibility.

```bash
deepl --lang-legacy <source_language> <target_language> [options] -t "Text to translate"
```

#### Examples

1. Translate Spanish to Russian:
   ```bash
   deepl spanish russian -t "¡Buenos días!"
   ```

2. Translate from a file (Italian to Portuguese):
   ```bash
   deepl IT PT --file test.txt
   ```

3. Use formal tone (Spanish to Russian):
   ```bash
   deepl ES RU --text "¿Cómo te llamas?" --formal
   ```

4. Use informal tone (Japanese to German):
   ```bash
   deepl JP DE --text "お元気ですか？" --informal
   ```

### Python Library

#### Basic Usage

```python
import deepl

translated_text = deepl.translate(source_language="ZH", target_language="NL", text="你好")
print(translated_text)  # Output: 'Hallo'
```

#### Advanced Usage

```python
import deepl

# Using full language names and specifying formality
translated_text = deepl.translate(
    source_language="danish",
    target_language="german",
    text="Ring til mig!",
    formality_tone="informal"
)
print(translated_text)  # Output: 'Ruf mich an!'

# Using legacy language support
translated_text = deepl.translate(
    source_language="ZH",
    target_language="EN",
    text="你好",
    lang_legacy=True
)
print(translated_text)  # Output: 'Hello'
```

## New Features

- **Improved Language Management**: More flexible and extensible language configuration system.
- **Legacy Support**: Backward compatibility for older language codes and configurations.
- **Enhanced Chinese Support**: Distinguish between Simplified and Traditional Chinese.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.