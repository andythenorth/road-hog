"""Road-specific catalogue core; adapted from Iron Horse src/train/catalogue.py.

Excluded train-only methods are preserved in iron_horse_reference/catalogue.py:
livery_defs, engine/wagon/clone quackers, track and formation methods.
No livery variants in this stage. ID allocation follows Catalogue.add_entries.
"""

from dataclasses import dataclass, fields, replace
from functools import cached_property

from . import schemas

from .model_def import UnitDef
from .livery import LiveryDef, livery_supplier


@dataclass
class CatalogueEntry:
    catalogue: "Catalogue"
    model_variant_id: str
    unit_variant_ids: list[str]
    unit_numeric_ids: list[int]
    livery_def: LiveryDef

    @property
    def index(self):
        return self.catalogue.index(self)


class Catalogue(list):
    def __init__(self, model_def, roster_id, roster_id_providing_module=None):
        super().__init__()
        self.model_def = model_def
        self.schema_name = model_def.schema_name
        self.roster_id = roster_id
        self.roster_id_providing_module = roster_id_providing_module
        self.producer = ModelVariantProducer(self)
        self.add_entries()

    @cached_property
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

    @property
    def livery_defs(self):
        # Iron Horse precedence: model group, schema group, model liveries, schema liveries.
        model_def = self.model_def
        schema_cls = self.schema_cls
        roster_module = self.roster_id_providing_module

        if getattr(model_def, "livery_group_name", None) is not None:
            livery_group_name = model_def.livery_group_name
        elif hasattr(schema_cls, "livery_group_name"):
            livery_group_name = schema_cls.livery_group_name
        else:
            livery_group_name = None

        if livery_group_name is not None:
            if roster_module is None:
                raise ValueError(f"{self.model_id}: livery group requires roster module")
            result = [
                livery_supplier.deliver(livery_name, relative_spriterow_num=index)
                for livery_name, index in roster_module.pax_mail_livery_groups[livery_group_name]
            ]
        elif getattr(model_def, "liveries", None) is not None:
            result = [
                livery_supplier.deliver(name, relative_spriterow_num=index)
                for index, name in enumerate(model_def.liveries)
            ]
        elif hasattr(schema_cls, "liveries"):
            result = [
                livery_supplier.deliver(name, relative_spriterow_num=index)
                for index, name in enumerate(schema_cls.liveries)
            ]
        else:
            # Road Hog's step 005 compatibility: implicit single default variant.
            result = [livery_supplier.deliver("DEFAULT", relative_spriterow_num=0)]

        if not result:
            raise ValueError(f"no liveries found for {self.model_id}")
        return result

    @property
    def livery_names_in_catalogue_order(self):
        return [livery.livery_name for livery in self.livery_defs]

    def add_entries(self):
        for variant_counter, livery_def in enumerate(self.livery_defs):
            model_variant_id = f"{self.model_id}_mv_{variant_counter}"
            unit_variant_ids = [
                f"{model_variant_id}_unit_{i}"
                for i, _ in enumerate(self.model_def.unit_defs)
            ]
            numeric_id_offset = self.model_def.base_numeric_id + (
                variant_counter * len(self.model_def.unit_defs)
            )
            unit_numeric_ids = [
                numeric_id_offset + i for i, _ in enumerate(self.model_def.unit_defs)
            ]
            self.append(
                CatalogueEntry(
                    self, model_variant_id, unit_variant_ids, unit_numeric_ids, livery_def
                )
            )
        if not self or not self.model_def.unit_defs:
            raise ValueError("Model must have at least one unit definition")

    def produce(self, catalogue_entry):
        return self.producer._produce(catalogue_entry)


class ModelVariantProducer:
    def __init__(self, catalogue):
        self.catalogue = catalogue

    def _produce(self, catalogue_entry=None):
        if catalogue_entry is None:
            raise ValueError("catalogue_entry is required")
        from . import units

        model_variant = self.catalogue.schema_cls(producer=self, catalogue_entry=catalogue_entry)
        for counter, unit_def in enumerate(self.catalogue.model_def.unit_defs):
            unit_cls = getattr(units, unit_def.unit_cls_name)
            # UnitDef properties come from either the Unit class or the model declaration.
            # Class-provided properties take precedence where both specify a value.
            if unit_cls.provisions_unit_def:
                unit_def = replace(
                    unit_def,
                    **{
                        field.name: getattr(unit_cls, f"_{field.name}")
                        for field in fields(UnitDef)
                        if field.name not in ("unit_cls_name", "repeat")
                        and hasattr(unit_cls, f"_{field.name}")
                    },
                )
            unit = unit_cls(
                model_variant=model_variant,
                unit_def=unit_def,
                id=catalogue_entry.unit_variant_ids[counter],
                numeric_id=catalogue_entry.unit_numeric_ids[counter],
            )
            for _ in range(unit_def.repeat):
                model_variant.units.append(unit)
        return model_variant
