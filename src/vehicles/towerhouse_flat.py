from road_vehicle import FlatbedTruckConsist

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="FlatbedTruck",
        model_id="towerhouse_flat",
        base_numeric_id=650,
        name="Towerhouse",
        gen=4,
    )

    model_def.add_unit_def(
        unit_cls_name="DieselConventionalCabSemiTractorTruckGen4A",
    )

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit",
        vehicle_length=7,
        cargo_length=4,
    )  # some cargo overlap eh?

    result.append(model_def)
    return result
