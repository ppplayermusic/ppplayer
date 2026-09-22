import os
import json
import sys
import re

ARB_DIR = "app/lib/l10n"
TEMPLATE_FILE = "app_en.arb"

def check_duplicates(ordered_pairs):
    d = {}
    for k, v in ordered_pairs:
        if k in d:
            raise ValueError(f"Duplicate key found: {k}")
        d[k] = v
    return d

def main():
    template_path = os.path.join(ARB_DIR, TEMPLATE_FILE)
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template_data = json.load(f, object_pairs_hook=check_duplicates)
    except Exception as e:
        print(f"Error parsing {TEMPLATE_FILE}: {e}")
        sys.exit(1)
        
    template_keys = set(k for k in template_data.keys() if not k.startswith('@'))
    
    # Exceptions that are always same across languages
    allowed_identical = {"appTitle", "titleSubtitle", "api", "github", "PPPlayer"}
    
    has_error = False
    
    for filename in sorted(os.listdir(ARB_DIR)):
        if not filename.endswith('.arb') or filename == TEMPLATE_FILE:
            continue
            
        locale = filename.replace('app_', '').replace('.arb', '')
        filepath = os.path.join(ARB_DIR, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f, object_pairs_hook=check_duplicates)
        except Exception as e:
            print(f"--- {locale.upper()} ---")
            print(f"  Parse Error: {e}")
            has_error = True
            continue
            
        keys = set(k for k in data.keys() if not k.startswith('@'))
        
        missing = template_keys - keys
        obsolete = keys - template_keys
        empty = [k for k in keys if data[k] == ""]
        
        identical = []
        for k in keys.intersection(template_keys):
            if k not in allowed_identical and data[k] == template_data[k]:
                identical.append(k)
                
        # placeholders mismatch: Check if the required placeholders defined in template's @key are present in string
        placeholder_issues = []
        for k in keys.intersection(template_keys):
            meta = template_data.get(f"@{k}", {})
            placeholders = meta.get("placeholders", {})
            
            # Simple check: if there are placeholders, ensure their names appear in the translated string
            # Also ensure the localized metadata defines the same placeholders
            loc_meta = data.get(f"@{k}", {})
            loc_placeholders = loc_meta.get("placeholders", {})
            
            # Check metadata definition matches
            if set(placeholders.keys()) != set(loc_placeholders.keys()):
                placeholder_issues.append((k, "Meta mismatch", set(placeholders.keys()), set(loc_placeholders.keys())))
                continue
                
            # Check string contains required placeholders
            for ph in placeholders.keys():
                if f"{{{ph}" not in data[k] and f"{{{ph}," not in data[k] and f"{{{ph} " not in data[k]:
                    placeholder_issues.append((k, f"Missing {{{ph}}} in string"))
            
            # Check string does not contain unexpected placeholders
            # Find all top-level placeholders like {name} or {count, plural, ...}
            found_placeholders = re.findall(r'\{([a-zA-Z0-9_]+)[,\}]', data[k])
            for found in found_placeholders:
                if found not in placeholders.keys():
                    placeholder_issues.append((k, f"Unexpected placeholder {{{found}}} in string not defined in metadata"))

                
        if missing or empty or placeholder_issues:
            has_error = True
            
        print(f"--- {locale.upper()} ---")
        if missing: print(f"  Missing: {len(missing)} {list(missing)[:5]}...")
        if obsolete: print(f"  Obsolete: {len(obsolete)}")
        if empty: print(f"  Empty: {len(empty)}")
        if identical: print(f"  Identical (suspected fallback): {len(identical)}")
        if placeholder_issues: 
            print(f"  Placeholder Mismatch: {len(placeholder_issues)}")
            for i in placeholder_issues[:3]: print(f"    {i}")

    if has_error:
        print("Validation FAILED.")
        sys.exit(1)
    else:
        print("Validation PASSED.")
        sys.exit(0)

if __name__ == '__main__':
    main()
