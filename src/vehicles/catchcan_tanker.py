from road_vehicle import TankerTramConsist

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(
        schema_name="TankerTram",
        model_id="catchcan_tanker",
        base_numeric_id=810,
        name="Catchcan",
        gen=2,
        intro_year_offset=2,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(
        unit_cls_name="ElectricMotorTram3", repeat=2
    )

    return [model_def]
