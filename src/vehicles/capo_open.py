from road_vehicle import OpenTruckConsist

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(
        schema_name="OpenTruck",
        model_id="capo_open",
        base_numeric_id=680,
        name="Capo",
        gen=5,
    )

    model_def.add_unit_def(
        unit_cls_name="DieselCaboverRigidTruckGen5A"
    )

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit",
        vehicle_length=4,
        cargo_length=3,
    )

    return [model_def]
