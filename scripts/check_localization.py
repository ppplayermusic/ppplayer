import json
import glob
import os
import re
import sys

def flatten_dict(d, parent_key='', sep='.'):
    items = []
    if isinstance(d, dict):
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict) or isinstance(v, list):
                items.extend(flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
    elif isinstance(d, list):
        for i, v in enumerate(d):
            new_key = f"{parent_key}{sep}{i}" if parent_key else str(i)
            if isinstance(v, dict) or isinstance(v, list):
                items.extend(flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
    return dict(items)

def check_locales():
    with open('website/messages/en.json') as f:
        en_data = json.load(f)

    en_flat = flatten_dict(en_data)
    
    # Specific keys we allow to match English exactly
    allowlist = [
        'PPPlayer', 'Linux', 'Mac', 'Windows', 'iOS', 'Android', 'AppImage',
        'Apple Silicon & Intel', 'x86_64', 'ARM64', 'ARM64 / ARM / x86_64',
        '4 GB RAM (Recommended)', '2 GB RAM (Recommended)',
        'Windows 10 or later (64-bit)', 'macOS 10.15 Catalina or newer',
        'Ubuntu 20.04 or newer (Experimental)', 'iOS 13.0 or newer',
        'Android 7.0 (API 24) or newer', 'Direct Download', 'App Store',
        'Google Play', 'Microsoft Store', 'x64'
    ]

    results = {}
    json_files = glob.glob('website/messages/*.json')
    
    for file in json_files:
        lang = os.path.basename(file).replace('.json', '')
        if lang == 'en': continue
        
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        flat = flatten_dict(data)
        
        missing = []
        english_leak = []
        placeholder_mismatch = []
        
        for k, en_val in en_flat.items():
            if k not in flat:
                missing.append(k)
                continue
                
            val = flat[k]
            
            if not isinstance(en_val, str):
                continue
                
            # Check placeholders
            en_placeholders = set(re.findall(r'\{[a-zA-Z0-9_]+\}', en_val))
            val_placeholders = set(re.findall(r'\{[a-zA-Z0-9_]+\}', str(val)))
            if en_placeholders != val_placeholders:
                placeholder_mismatch.append((k, en_val, val))
                
            # Check english leakage
            str_val = str(val).strip()
            if str_val == en_val.strip() and en_val not in allowlist and len(en_val) > 3 and not en_val.isdigit():
                # Allow identical if it's just a brand name or acronym without alphabets
                if re.search(r'[a-zA-Z]', en_val):
                    english_leak.append(k)
                
        results[lang] = {
            'missing': missing,
            'english_leak': english_leak,
            'placeholder_mismatch': placeholder_mismatch
        }

    return results

if __name__ == '__main__':
    results = check_locales()
    
    total_issues = 0
    print("| Locale | Missing Keys | English Leaks | Placeholder Mismatches | Status |")
    print("|--------|--------------|---------------|------------------------|--------|")
    
    for lang, res in sorted(results.items()):
        m_count = len(res['missing'])
        e_count = len(res['english_leak'])
        p_count = len(res['placeholder_mismatch'])
        
        status = "Pass" if m_count == 0 and e_count == 0 and p_count == 0 else "Fail"
        total_issues += m_count + e_count + p_count
        print(f"| `{lang}` | {m_count} | {e_count} | {p_count} | {status} |")
        
    if total_issues > 0:
        print("\nSome locales failed validation. Run translation pipeline to fix.")
        sys.exit(1)
    else:
        print("\nAll 31 non-English locales passed localization checks!")
        sys.exit(0)
