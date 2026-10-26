from road_vehicle import PaxLocalTramConsist

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="PaxLocalTram",
        model_id="ladycross_pax",
        base_numeric_id=0,
        name="Ladycross",
        gen=1,
    )

    model_def.add_unit_def(unit_cls_name="SteamEngineTram2")

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit",
        vehicle_length=4,
        repeat=3,
    )

    result.append(model_def)
    return result
