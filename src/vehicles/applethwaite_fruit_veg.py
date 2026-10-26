from road_vehicle import FruitVegTramConsist

from road_vehicle.model_def import ModelDef



def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="FruitVegTram",
        model_id="applethwaite_fruit_veg",
        base_numeric_id=940,
        name="Applethwaite",
        gen=2,
        intro_year_offset=1,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(unit_cls_name="ElectricMotorTram1", repeat=2)

    result.append(model_def)
    return result
