import codecs
import os
import re
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), "r") as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="deepl-translate",
    version=find_version("deepl", "__init__.py"),
    description="Python package to translate text using deepl.com",  # fixed typo here
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/ptrstn/deepl-translate",
    author="Peter Stein",
    license="MIT",
    python_requires='>3.6',
    packages=find_packages(),  # ensure all packages (including sub-packages) are found
    install_requires=["requests", "pyyaml"],
    entry_points={"console_scripts": ["deepl=deepl.__main__:main"]},
    classifiers=["License :: OSI Approved :: MIT License"],
    include_package_data=True,  # ensures package data like langs/* will be included
    package_data={
        "deepl": ["langs/**/*"]  # include all files in langs and its subdirectories
    },
)

