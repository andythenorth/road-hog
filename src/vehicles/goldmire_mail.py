from road_vehicle import MailTruckConsist, DieselVehicleUnit

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(
        schema_name="MailTruck",
        model_id="goldmire_mail",
        base_numeric_id=200,
        name="Goldmire",
        power=250,  # custom power
        speed=75,
        gen=4,
        intro_year_offset=1,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(
        
        unit_cls_name="DieselVehicleUnit",
        vehicle_length=6,
    )

    return [model_def]
