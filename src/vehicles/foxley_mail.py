from road_vehicle import MailTramConsist, ElectricVehicleUnit

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(
        schema_name="MailTram",
        model_id="foxley_mail",
        base_numeric_id=190,
        name="Foxley",
        power=240,  # custom HP
        gen=2,
        intro_year_offset=3,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(
        base_platform=None,  # mail trams have no base platform by design currently
        unit_cls_name="ElectricVehicleUnit",
        vehicle_length=4,
        repeat=2,
    )

    return [model_def]
