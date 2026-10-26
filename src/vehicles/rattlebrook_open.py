from road_vehicle import OpenTruckConsist

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="OpenTruck",
        model_id="rattlebrook_open",
        base_numeric_id=670,
        name="Rattlebrook",
        gen=3,
    )

    model_def.add_unit_def(unit_cls_name="DieselCaboverRigidTruckGen3A")

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit",
        vehicle_length=4,
        cargo_length=4,
    )

    result.append(model_def)
    return result
