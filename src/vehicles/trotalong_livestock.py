from road_vehicle import LivestockTramConsist

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="LivestockTram",
        model_id="trotalong_livestock",
        base_numeric_id=720,
        name="Trotalong",
        gen=2,
        intro_year_offset=1,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(unit_cls_name="ElectricMotorTram1", repeat=2)

    result.append(model_def)
    return result
