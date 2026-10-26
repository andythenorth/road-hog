from road_vehicle import BoxTruckConsist

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(
        schema_name="BoxTruck",
        model_id="quickset_box",
        base_numeric_id=350,
        name="Quickset",
        gen=4,
    )

    model_def.add_unit_def(
        unit_cls_name="DieselConventionalCabSemiTractorTruckGen4A",
    )

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit", vehicle_length=7
    )

    return [model_def]
