#!/usr/bin/env python3
"""Run from repository root: python bin/001_migrate_model_variant_naming.py"""
from pathlib import Path
import re

root = Path('src')

def change(file, old, new):
    path = root / file
    s = path.read_text()
    if s.count(old) != 1:
        raise RuntimeError(f'{file}: expected one match for {old[:45]!r}, got {s.count(old)}')
    path.write_text(s.replace(old, new))

c = 'road_vehicle/catalogue.py'
s = 'road_vehicle/schemas.py'
change(c, 'from dataclasses import dataclass, fields, replace', 'from dataclasses import dataclass, fields, replace\nfrom functools import cached_property\n\nfrom . import schemas')
change(c, '    def add_entries(self):', '''    @cached_property
    def model_id(self):
        return self.model_def.model_id

    @cached_property
    def schema_cls(self):
        return getattr(schemas, self.schema_name)

    @property
    def default_entry(self):
        return self[0]

    def is_default_model_variant(self, model_variant):
        return model_variant.catalogue_entry == self.default_entry

    def add_entries(self):''')
change(c, 'f"{self.model_def.model_id}_mv_{variant_counter}"', 'f"{self.model_id}_mv_{variant_counter}"')
change(c, '''        from . import schemas, units

        schema_cls = getattr(schemas, self.catalogue.schema_name)
        model_variant = schema_cls(producer=self, catalogue_entry=catalogue_entry)''', '''        from . import units

        model_variant = self.catalogue.schema_cls(producer=self, catalogue_entry=catalogue_entry)''')
change(s, 'import global_constants', 'from functools import cached_property\n\nimport global_constants')
change(s, '''        self.model_def = producer.catalogue.model_def
        self.roster_id = producer.catalogue.roster_id
        self.units = []
        self.id = catalogue_entry.model_variant_id''', '''        self.units = []''')
path = root / s
src = path.read_text()
a = src.index('    @property\n    def name_type_suffix(self):')
b = src.index('\n\nimport polar_fox', a)
new = '''    @property
    def catalogue(self):
        return self.catalogue_entry.catalogue

    @property
    def model_id(self):
        return self.catalogue.model_id

    @property
    def model_def(self):
        return self.catalogue.model_def

    @property
    def roster_id(self):
        return self.catalogue.roster_id

    @property
    def id(self):
        return self.catalogue_entry.model_variant_id

    @property
    def base_numeric_id(self):
        return self.model_def.base_numeric_id

    @property
    def is_default_model_variant(self):
        return self.catalogue.is_default_model_variant(self)

    @property
    def name(self):
        return self.model_def.name

    @property
    def str_name_suffix(self):
        if getattr(self, "_str_name_suffix", None) is not None:
            return self._str_name_suffix
        else:
            return None

    def get_name_parts(self, context):
        return ["STR_NAME_" + self.model_id.upper()]

    @cached_property
    def name_as_nml_prop(self):
        name_parts = self.get_name_parts(context="default_name")
        if len(name_parts) == 1:
            result = f"string({name_parts[0]})"
        else:
            result = f"string(STR_NAME_TWO_PARTS, string({name_parts[0]}), string({name_parts[1]}))"
        return result
'''
src = src[:a] + new + src[b:]
src = re.sub(r'^    name_suffix_vehicle_type = .*\n', '', src, flags=re.M)
src = re.sub(r'    @property\n    def name_type_suffix\(self\):\n        return "STR_NAME_SUFFIX_(?:BUS|PASSENGER_TRAM|COACH)"\n\n', '', src)
path.write_text(src)
change('roster.py', '"STR_NAME_" + model_def.model_id.upper()', '"STR_NAME_" + consist.catalogue.model_id.upper()')
print('Migration 001 applied')
