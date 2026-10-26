from road_vehicle import EdiblesTankerTramConsist

from road_vehicle.model_def import ModelDef



def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="EdiblesTankerTram",
        model_id="bottlebrook_edibles_tanker",
        base_numeric_id=510,
        name="Bottlebrook",
        gen=3,
        intro_year_offset=6,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(unit_cls_name="ElectricMotorTram4", repeat=2)

    result.append(model_def)
    return result
