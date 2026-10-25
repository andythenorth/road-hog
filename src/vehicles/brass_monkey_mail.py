from road_vehicle import MailTruckConsist, DieselVehicleUnit

from road_vehicle.model_def import ModelDef
# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(schema_name='MailTruck', 
        model_id="brass_monkey_mail",
        base_numeric_id=570,
        name="Brass Monkey",
        power=140,
        speed=55,
        gen=3,
        intro_year_offset=1,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(
        base_platform=None,  # mail trucks have no base platform by design currently
        unit_cls_name='DieselVehicleUnit',
        vehicle_length=6,
    )

    return [model_def]
