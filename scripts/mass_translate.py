import json
import os
import time
import re
import translators as ts
from check_localization import check_locales

LANG_MAP = {
    'ar': 'ar', 'bn': 'bn', 'cs': 'cs', 'da': 'da', 'de': 'de', 'es': 'es', 'et': 'et', 'fa': 'fa',
    'fil': 'tl', 'fr': 'fr', 'gn': 'gn', 'hi': 'hi', 'hr': 'hr', 'hu': 'hu', 'id': 'id', 'it': 'it',
    'ja': 'ja', 'ka': 'ka', 'kk': 'kk', 'ko': 'ko', 'lv': 'lv', 'ms': 'ms', 'my': 'my', 'pcm': 'en', 
    'pl': 'pl', 'pt-BR': 'pt', 'ru': 'ru', 'sv': 'sv', 'tr': 'tr', 'uz': 'uz', 'zh': 'zh-CN'
}

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

def translate_text(text, target_lang):
    if target_lang == 'en' or target_lang not in LANG_MAP:
        return text
    
    try:
        placeholders = re.findall(r'\{[a-zA-Z0-9_]+\}', text)
        temp_text = text
        for i, p in enumerate(placeholders):
            temp_text = temp_text.replace(p, f"__PH{i}__")
            
        # Using translators package with bing
        translated = ts.translate_text(temp_text, translator='bing', from_language='en', to_language=LANG_MAP[target_lang])
        
        for i, p in enumerate(placeholders):
            translated = translated.replace(f"__PH{i}__", p)
            
        time.sleep(0.5)
        return translated
    except Exception as e:
        print(f"Error translating to {target_lang} with bing, trying google: {e}")
        try:
            translated = ts.translate_text(temp_text, translator='google', from_language='en', to_language=LANG_MAP[target_lang])
            for i, p in enumerate(placeholders):
                translated = translated.replace(f"__PH{i}__", p)
            time.sleep(0.5)
            return translated
        except Exception as e2:
            print(f"Error translating to {target_lang} with google: {e2}")
            return text

def main():
    print("Checking locales...")
    results = check_locales()
    
    with open('website/messages/en.json') as f:
        en_data = json.load(f)
    
    for lang, issues in results.items():
        missing = issues['missing']
        english_leak = issues['english_leak']
        
        needs_translation = missing + english_leak
        if not needs_translation:
            continue
            
        if lang == 'pcm':
            continue
            
        print(f"Translating {len(needs_translation)} keys for {lang}...")
        
        filepath = f'website/messages/{lang}.json'
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for key in needs_translation:
            try:
                en_val = get_nested_value(en_data, key)
            except (KeyError, IndexError, TypeError):
                continue
                
            if isinstance(en_val, str):
                print(f"  {key}: {en_val}")
                translated = translate_text(en_val, lang)
                set_nested_value(data, key, translated)
                
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        print(f"Updated {filepath}")

if __name__ == '__main__':
    main()
