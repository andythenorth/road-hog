from road_vehicle import OpenTramConsist

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(
        schema_name="OpenTram",
        model_id="buildwas_open",
        base_numeric_id=120,
        name="Buildwas",
        gen=1,
    )

    model_def.add_unit_def(
        unit_cls_name="SteamEngineTram1"
    )

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit",
        
        vehicle_length=4,
        cargo_length=4,
        repeat=3,
    )

    return [model_def]
