from road_vehicle import OpenTramConsist, ElectricVehicleUnit

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(
        schema_name="OpenTram",
        model_id="portland_open",
        base_numeric_id=860,
        name="Portland",
        gen=2,
    )

    model_def.add_unit_def(
        
        unit_cls_name="ElectricVehicleUnit",
        vehicle_length=8,
        cargo_length=3,
        repeat=2,
    )

    return [model_def]
