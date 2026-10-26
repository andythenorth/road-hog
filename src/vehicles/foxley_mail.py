from road_vehicle import MailTramConsist, ElectricVehicleUnit

from road_vehicle.model_def import ModelDef



def main(roster_id):
    result = []

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
        unit_cls_name="ElectricVehicleUnit",
        vehicle_length=4,
        repeat=2,
    )

    result.append(model_def)
    return result
