#!/usr/bin/env python3
"""Run from the Road Hog repository root."""
from pathlib import Path

path = Path('src/doc_helper.py')
old = '''    def unpack_name_string(self, consist):
        substrings = consist.name.split("string(")
        name = consist.model_def.name
        type_suffix = self.lang_strings[substrings[3][:-2]]
        return {
            "full_name": name + " " + type_suffix,
            "name": name,
            "type_suffix": type_suffix,
        }
'''
new = '''    def unpack_name_string(self, consist):
        name_parts = consist.get_name_parts(context="default_name")
        translated_parts = [self.lang_strings[key] for key in name_parts]
        return {
            "full_name": " ".join(translated_parts),
            "name": translated_parts[0],
            "type_suffix": " ".join(translated_parts[1:]),
        }
'''
source = path.read_text()
if source.count(old) != 1:
    raise RuntimeError(f'{path}: expected original unpack_name_string() exactly once')
path.write_text(source.replace(old, new))
print(f'Updated {path}')
