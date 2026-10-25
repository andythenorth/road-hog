"""Port the roster's language name lookup for ModelDef vehicles.

CABBAGE Keep the legacy path while old Road Hog vehicle modules are still in use.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FILE = ROOT / 'src/roster.py'
OLD = '''        for consist in self.consists_in_buy_menu_order:
            if consist._name is not None:
                lang_strings["STR_NAME_" + consist.id.upper()] = consist._name
'''
NEW = '''        for consist in self.consists_in_buy_menu_order:
            # Road Hog legacy vehicles own _name and id. New catalogue vehicles
            # get their name and base model ID from ModelDef instead.
            # CABBAGE Keep both paths until the old vehicle definitions are ported.
            model_def = getattr(consist, "model_def", None)
            if model_def is not None:
                name = model_def.name
                model_id = model_def.model_id
            else:
                name = consist._name
                model_id = consist.id
            if name is not None:
                lang_strings["STR_NAME_" + model_id.upper()] = name
'''
s = FILE.read_text()
if s.count(OLD) == 1:
    FILE.write_text(s.replace(OLD, NEW))
    print('PASS: roster language names read from ModelDef for new vehicles')
elif s.count(NEW) == 1:
    print('UNCHANGED: roster language seam already ported')
else:
    raise SystemExit('Unexpected roster language code; refusing to change it')
