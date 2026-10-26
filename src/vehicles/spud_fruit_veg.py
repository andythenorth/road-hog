from road_vehicle import FruitVegFeldbahnConsist

from road_vehicle.model_def import ModelDef



def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="FruitVegFeldbahn",
        model_id="spud_fruit_veg",
        base_numeric_id=1260,
        name="Spud",
        gen=3,
    )

    model_def.add_unit_def(unit_cls_name="DieselEngineFeldbahnGen3A")

    model_def.add_unit_def(unit_cls_name="WagonFeldbahnA", repeat=5)

    result.append(model_def)
    return result
