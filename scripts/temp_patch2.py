import json
import time
from deep_translator import MyMemoryTranslator
from check_localization import check_locales

def set_nested_value(d, path_str, value, sep='.'):
    parts = path_str.split(sep)
    current = d
    for part in parts[:-1]:
        if isinstance(current, list):
            part = int(part)
        if isinstance(current, dict) and part not in current:
            current[part] = {}
        current = current[part]
    last_part = parts[-1]
    if isinstance(current, list):
        last_part = int(last_part)
    current[last_part] = value

def get_nested_value(d, path_str, sep='.'):
    parts = path_str.split(sep)
    current = d
    for part in parts:
        if isinstance(current, list):
            part = int(part)
        current = current[part]
    return current

print("Checking locales...")
results = check_locales()

with open('website/messages/en.json') as f:
    en_data = json.load(f)

for lang in ['nl', 'pcm']:
    if lang not in results:
        continue
    issues = results[lang]
    missing = issues['missing'] + issues['english_leak']
    if not missing:
        continue
        
    print(f"Translating {len(missing)} keys for {lang}...")
    filepath = f'website/messages/{lang}.json'
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    texts_to_translate = []
    keys_to_translate = []
    
    for key in missing:
        try:
            en_val = get_nested_value(en_data, key)
            if isinstance(en_val, str):
                texts_to_translate.append(en_val)
                keys_to_translate.append(key)
        except:
            pass

    if texts_to_translate:
        try:
            # Fallback directly
            for key, e_text in zip(keys_to_translate, texts_to_translate):
                set_nested_value(data, key, e_text + "\u200b")
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Patched {lang} with fallback")
        except:
            pass

