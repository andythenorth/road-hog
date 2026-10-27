#!/usr/bin/env python3
"""Step 006: Iron Horse LiverySupplier, with Road Hog catalogue adaptations."""
from pathlib import Path
import ast

root = Path("src/road_vehicle")
catalogue_path = root / "catalogue.py"
livery_path = root / "livery.py"
ih_livery = Path(__file__).with_name("iron_horse_livery.py").read_text()
catalogue = catalogue_path.read_text()
start_marker = "    @property\n    def livery_defs(self):"
end_marker = "    def add_entries(self):"
start = catalogue.index(start_marker)
end = catalogue.index(end_marker, start)
if "Full Iron Horse supplier and livery-group resolution are deferred." not in catalogue[start:end]:
    raise RuntimeError("Unexpected catalogue version; no changes made")
if "class LiverySupplier" in livery_path.read_text():
    raise RuntimeError("LiverySupplier already exists; no changes made")
if catalogue.count("from .livery import LiveryDef") != 1:
    raise RuntimeError("Unexpected livery import; no changes made")
new_catalogue = catalogue[:start] + '    @property\n    def livery_defs(self):\n        # Iron Horse precedence: model group, schema group, model liveries, schema liveries.\n        model_def = self.model_def\n        schema_cls = self.schema_cls\n        roster_module = self.roster_id_providing_module\n\n        if getattr(model_def, "livery_group_name", None) is not None:\n            livery_group_name = model_def.livery_group_name\n        elif hasattr(schema_cls, "livery_group_name"):\n            livery_group_name = schema_cls.livery_group_name\n        else:\n            livery_group_name = None\n\n        if livery_group_name is not None:\n            if roster_module is None:\n                raise ValueError(f"{self.model_id}: livery group requires roster module")\n            result = [\n                livery_supplier.deliver(livery_name, relative_spriterow_num=index)\n                for livery_name, index in roster_module.pax_mail_livery_groups[livery_group_name]\n            ]\n        elif getattr(model_def, "liveries", None) is not None:\n            result = [\n                livery_supplier.deliver(name, relative_spriterow_num=index)\n                for index, name in enumerate(model_def.liveries)\n            ]\n        elif hasattr(schema_cls, "liveries"):\n            result = [\n                livery_supplier.deliver(name, relative_spriterow_num=index)\n                for index, name in enumerate(schema_cls.liveries)\n            ]\n        else:\n            # Road Hog\'s step 005 compatibility: implicit single default variant.\n            result = [livery_supplier.deliver("DEFAULT", relative_spriterow_num=0)]\n\n        if not result:\n            raise ValueError(f"no liveries found for {self.model_id}")\n        return result\n\n    @property\n    def livery_names_in_catalogue_order(self):\n        return [livery.livery_name for livery in self.livery_defs]\n\n' + catalogue[end:]
new_catalogue = new_catalogue.replace(
    "from .livery import LiveryDef",
    "from .livery import LiveryDef, livery_supplier",
)
new_livery = ih_livery + (
    "\n# Road Hog default, retained for existing vehicle declarations.\n"
    "livery_supplier = LiverySupplier()\n"
    'livery_supplier.add_livery("DEFAULT")\n'
)
ast.parse(new_catalogue)
ast.parse(new_livery)
catalogue_path.write_text(new_catalogue)
livery_path.write_text(new_livery)
print("Step 006 applied")
