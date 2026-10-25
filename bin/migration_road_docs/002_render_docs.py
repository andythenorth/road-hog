"""Use the old sprite filename with the new model ID, only at the docs edge."""
from _common import ROOT, replace_once

path = ROOT / 'src/render_docs.py'
old = '''    vehicle_spritesheet = Image.open(
        os.path.join("generated", "graphics", consist.id + ".png")
    )
'''
new = '''    # CABBAGE Catalogue variants have new IDs, but the existing graphics pipeline
    # still writes the source sprite PNG under the original model ID.
    # Keep this at the docs boundary; do not rename sprites or change pipelines.
    sprite_file_id = (
        consist.model_def.model_id
        if hasattr(consist, "model_def")
        else consist.id
    )
    vehicle_spritesheet = Image.open(
        os.path.join("generated", "graphics", sprite_file_id + ".png")
    )
'''
replace_once(path,old,new)
