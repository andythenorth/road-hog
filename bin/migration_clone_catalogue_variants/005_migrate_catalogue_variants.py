#!/usr/bin/env python3
"""Step 005: run from the Road Hog repository root."""
from pathlib import Path
import ast

root = Path("src")
catalogue = root / "road_vehicle/catalogue.py"
schemas = root / "road_vehicle/schemas.py"
roster = root / "roster.py"
livery = root / "road_vehicle/livery.py"
changes = {}

def change(path, before, after):
    source = changes.get(path, path.read_text())
    if source.count(before) != 1:
        raise RuntimeError(f"{path}: expected exactly one match: {before[:65]!r}")
    changes[path] = source.replace(before, after)

if livery.exists():
    raise RuntimeError("Livery module already exists; review before applying")

change(catalogue, "from .model_def import UnitDef",
       "from .model_def import UnitDef\nfrom .livery import LiveryDef")
change(catalogue, "    unit_numeric_ids: list[int]",
       "    unit_numeric_ids: list[int]\n    livery_def: LiveryDef")
change(catalogue, "    def add_entries(self):", '''    @property
    def livery_defs(self):
        # Full Iron Horse supplier and livery-group resolution are deferred.
        definitions = getattr(self.model_def, "liveries", None)
        if definitions is None:
            definitions = getattr(self.schema_cls, "liveries", None)
        if definitions is None:
            return [LiveryDef("DEFAULT")]
        if not definitions or not all(isinstance(item, LiveryDef) for item in definitions):
            raise ValueError(f"{self.model_id}: expected nonempty LiveryDef list")
        return definitions

    def add_entries(self):''')
change(catalogue, "for variant_counter in range(1):",
       "for variant_counter, livery_def in enumerate(self.livery_defs):")
change(catalogue, "self, model_variant_id, unit_variant_ids, unit_numeric_ids",
       "self, model_variant_id, unit_variant_ids, unit_numeric_ids, livery_def")
change(schemas, "    @property\n    def catalogue(self):", '''    @property
    def livery_def(self):
        return self.catalogue_entry.livery_def

    @property
    def catalogue(self):''')
change(roster, "        self.consists = []",
       "        self.consists = []\n        self.model_variants_by_catalogue = {}")
change(roster, "                self.consists.extend(catalogue.produce(entry) for entry in catalogue)",
       '''                model_variants = [catalogue.produce(entry) for entry in catalogue]
                self.model_variants_by_catalogue[catalogue.model_id] = model_variants
                self.consists.extend(model_variants)''')
for path, source in changes.items():
    ast.parse(source, filename=str(path))
for path, source in changes.items():
    path.write_text(source)
livery.write_text('''from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class LiveryDef:
    livery_name: str
    colour_set_names: List = field(default_factory=list)
    docs_image_input_cc: Optional[List] = None
    is_freight_wagon_livery: Optional[bool] = False
    purchase_swatch_colour_set_names: List = field(default_factory=list)
    proxy_livery_for_badge_display_and_filter: Optional[str] = None
    has_predrawn_badge_sprite: Optional[bool] = False
    relative_spriterow_num: Optional[int] = None
    remap_to_cc: Optional[str] = None
    use_weathering: Optional[bool] = False

    @property
    def purchase_swatch(self):
        if not self.is_freight_wagon_livery:
            return None
        if self.purchase_swatch_colour_set_names:
            return self.purchase_swatch_colour_set_names
        return list(set(self.colour_set_names))

    @property
    def display_and_filter_name(self):
        return self.proxy_livery_for_badge_display_and_filter or self.livery_name

    @property
    def display_and_filter_name_badge_label(self):
        return f"livery/iron_horse/{self.display_and_filter_name.lower()}"

    @property
    def internal_name_badge_label(self):
        return f"_ih_livery_def/internal_livery_name/{self.livery_name.lower()}"

    @property
    def weathering_badge_label(self):
        return f"_ih_livery_def/use_weathering/{self.use_weathering}"
''')
print("Step 005 applied")
