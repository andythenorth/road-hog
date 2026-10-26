from road_vehicle import MailTramConsist, ElectricVehicleUnit

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="MailTram",
        model_id="singing_river_mail",
        base_numeric_id=850,
        name="Singing River",
        power=600,
        gen=5,
    )

    model_def.add_unit_def(
        unit_cls_name="ElectricVehicleUnit",
        vehicle_length=8,
        effects=["EFFECT_SPRITE_ELECTRIC, 0, 0, 10"],
    )

    result.append(model_def)
    return result
