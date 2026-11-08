#!/usr/bin/env python3
"""Validate supplier delivery and two-variant catalogue resolution."""
import sys
from pathlib import Path
from types import SimpleNamespace
sys.path.insert(0, str(Path("src").resolve()))
sys.argv = [sys.argv[0], "-gn", "road-hog"]
from road_vehicle.livery import LiverySupplier, livery_supplier
from road_vehicle.catalogue import Catalogue

supplier = LiverySupplier()
supplier.add_livery("TEST", use_weathering=True)
assert supplier.deliver("TEST", 2).relative_spriterow_num == 2
assert supplier.deliver("TEST_NO_WEATHERING", 3).use_weathering is False
assert livery_supplier.deliver("DEFAULT", 0).livery_name == "DEFAULT"

livery_supplier.add_livery("VALIDATE_A")
livery_supplier.add_livery("VALIDATE_B")
model = SimpleNamespace(model_id="validate_006", schema_name="RoadVehicleBase",
    base_numeric_id=20000, unit_defs=[object()], liveries=["VALIDATE_A", "VALIDATE_B"])
catalogue = Catalogue(model, roster_id="validation")
assert catalogue.livery_names_in_catalogue_order == ["VALIDATE_A", "VALIDATE_B"]
assert [e.unit_numeric_ids for e in catalogue] == [[20000], [20001]]
print("Step 006 validation passed")
