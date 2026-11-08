"""Read model names and IDs in docs, while old consists still work."""
from _common import ROOT, replace_once

path = ROOT / 'src/doc_helper.py'
old = '''    def unpack_name_string(self, consist):
        substrings = consist.name.split("string(")
        name = consist._name
        type_suffix = self.lang_strings[substrings[3][0:-3]]
        power_suffix = self.lang_strings[substrings[4][0:-2]]
'''
new = '''    def unpack_name_string(self, consist):
        substrings = consist.name.split("string(")
        # CABBAGE New schema has ModelDef; legacy Consist stores the name in _name.
        # Keep the original translated suffix handling. Do not guess English names.
        name = (
            consist.model_def.name
            if hasattr(consist, "model_def")
            else consist._name
        )
        type_suffix = self.lang_strings[substrings[3][0:-3]]
        power_suffix = self.lang_strings[substrings[4][0:-2]]
'''
replace_once(path, old, new)
old2 = '''    def get_base_numeric_id(self, consist):
        return consist.base_numeric_id
'''
new2 = '''    def get_base_numeric_id(self, consist):
        # Catalogue owns IDs for new models. This is the base ID for docs sorting.
        return (
            consist.model_def.base_numeric_id
            if hasattr(consist, "model_def")
            else consist.base_numeric_id
        )
'''
replace_once(path, old2, new2)
