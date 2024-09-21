import json
import os
import yaml
from deepl.settings import SUPPORTED_LANGUAGES

def create_yaml_file(language, code, output_path):
    data = {
        "language": language,
        "code": code.lower(),
        "keywords": [language.lower()]
    }
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as file:
        yaml.dump(data, file, allow_unicode=True, sort_keys=False)

def create_yaml_file(lang_data, output_path):
    data = {
        "language": lang_data.get("name", lang_data["language"]),
        "code": lang_data["code"].lower(),
    }
    
    if "keywords" in lang_data:
        data["keywords"] = lang_data["keywords"]
    else:
        data["keywords"] = [lang_data["language"].lower()]
    
    if "regionalVariant" in lang_data:
        data["regionalVariant"] = lang_data["regionalVariant"]
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as file:
        yaml.dump(data, file, allow_unicode=True, sort_keys=False)

def main():
    #base_dir = "langs"
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(base_dir, exist_ok=True)
    
    for lang in SUPPORTED_LANGUAGES:
        language = lang["language"]
        
        if language.lower() == "chinese":
            # Create Chinese simplified and traditional
            create_yaml_file(lang, os.path.join(base_dir, "chinese", f"chinese_{lang['name'].split()[-1].lower()}.yaml"))
        else:
            # Create other languages
            create_yaml_file(lang, os.path.join(base_dir, language.lower(), f"{language.lower()}.yaml"))

if __name__ == "__main__":
    main()
    print("YAML config files have been generated successfully.")
