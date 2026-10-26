from road_vehicle import CoveredHopperTramConsist

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(
        schema_name="CoveredHopperTram",
        model_id="thurlbear_covered_hopper",
        base_numeric_id=460,
        name="Thurlbear",
        gen=3,
    )

    model_def.add_unit_def(
        unit_cls_name="ElectricMotorTram4", repeat=2
    )

    return [model_def]
