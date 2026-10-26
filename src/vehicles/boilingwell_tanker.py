from road_vehicle import TankerTruckConsist

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="TankerTruck",
        model_id="boilingwell_tanker",
        base_numeric_id=920,
        name="Boilingwell",
        gen=2,
        intro_year_offset=5,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(unit_cls_name="SteamCaboverSemiTractorTruckGen2A")

    model_def.add_unit_def(unit_cls_name="RoadVehicleUnit", vehicle_length=5)

    result.append(model_def)
    return result
