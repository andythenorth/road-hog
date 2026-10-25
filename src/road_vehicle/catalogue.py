"""Road-specific catalogue core; adapted from Iron Horse src/train/catalogue.py.

Excluded train-only methods are preserved in iron_horse_reference/catalogue.py:
livery_defs, engine/wagon/clone quackers, track and formation methods.
No livery variants in this stage. ID allocation follows Catalogue.add_entries.
"""

from dataclasses import dataclass


@dataclass
class CatalogueEntry:
    catalogue: "Catalogue"
    model_variant_id: str
    unit_variant_ids: list[str]
    unit_numeric_ids: list[int]

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

    def add_entries(self):
        # Iron Horse's original per-variant/per-unit ID rule; a single default variant.
        for variant_counter in range(1):
            model_variant_id = f"{self.model_def.model_id}_mv_{variant_counter}"
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
                    self, model_variant_id, unit_variant_ids, unit_numeric_ids
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
        from . import schemas, units

        schema_cls = getattr(schemas, self.catalogue.schema_name)
        model_variant = schema_cls(producer=self, catalogue_entry=catalogue_entry)
        for counter, unit_def in enumerate(self.catalogue.model_def.unit_defs):
            # CABBAGE Keep old platform override order, including the legacy `type` field.
            # Resolve once per UnitDef; repeated physical units reuse the same object.
            from dataclasses import replace

            resolved_def = unit_def
            platform = None
            if unit_def.base_platform is not None:
                platform = unit_def.base_platform()
                configured = platform.configure_unit_args(
                    **{
                        key: value
                        for key, value in vars(unit_def).items()
                        if key != "base_platform"
                    }
                )
                platform_unit_type = configured.pop("type", None)
                configured.pop("base_platform", None)
                if platform_unit_type is not None:
                    configured["unit_cls_name"] = platform_unit_type.__name__
                resolved_def = replace(unit_def, **configured)
            unit_cls = getattr(units, resolved_def.unit_cls_name)
            unit = unit_cls(
                model_variant=model_variant,
                unit_def=resolved_def,
                id=catalogue_entry.unit_variant_ids[counter],
                numeric_id=catalogue_entry.unit_numeric_ids[counter],
            )
            if platform is not None:
                unit.base_platform = platform
            for _ in range(unit_def.repeat):
                model_variant.units.append(unit)
        return model_variant
