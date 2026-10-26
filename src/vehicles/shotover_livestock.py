from road_vehicle import LivestockTramConsist

from road_vehicle.model_def import ModelDef



def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="LivestockTram",
        model_id="shotover_livestock",
        base_numeric_id=370,
        name="Shotover",
        gen=3,
        intro_year_offset=1,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(unit_cls_name="ElectricMotorTram4", repeat=2)

    result.append(model_def)
    return result
