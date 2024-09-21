import os
import re
import json
import yaml
from deepl.settings import SUPPORTED_LANGUAGES

def normalize_filename(name):
    # Remove all non-alphanumeric characters and replace spaces with underscores
    normalized = re.sub(r'[^\w\s]', '', name.lower())
    return re.sub(r'\s+', '_', normalized)



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
        name = lang["name"] if "name" in lang else language
        normalized_name = normalize_filename(name)
        dir_name = normalize_filename(lang["language"])
        print(f"Generating YAML config file for {language}... ({normalized_name}.yaml)")

        
        file_path = os.path.join(base_dir, dir_name, f"{normalized_name}.yaml")
        create_yaml_file(lang, file_path)

if __name__ == "__main__":
    main()
    print("YAML config files have been generated successfully.")
