#!/usr/bin/env python3
"""Check two catalogue entries without changing production declarations."""
import sys
from pathlib import Path
from types import SimpleNamespace
sys.path.insert(0, str(Path("src").resolve()))
from road_vehicle.catalogue import Catalogue
from road_vehicle.livery import LiveryDef

model = SimpleNamespace(
    model_id="variant_validation",
    schema_name="RoadVehicleBase",
    base_numeric_id=20000,
    unit_defs=[SimpleNamespace(), SimpleNamespace()],
    liveries=[LiveryDef("FIRST"), LiveryDef("SECOND")],
)
catalogue = Catalogue(model, roster_id="validation")
assert len(catalogue) == 2
assert [entry.model_variant_id for entry in catalogue] == [
    "variant_validation_mv_0", "variant_validation_mv_1"
]
assert [entry.unit_numeric_ids for entry in catalogue] == [
    [20000, 20001], [20002, 20003]
]
assert [entry.livery_def.livery_name for entry in catalogue] == [
    "FIRST", "SECOND"
]
assert catalogue.default_entry is catalogue[0]
print("Step 005 catalogue variant validation passed")
