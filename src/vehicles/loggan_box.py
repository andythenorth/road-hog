from road_vehicle import BoxFeldbahnConsist

from road_vehicle.model_def import ModelDef



def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="BoxFeldbahn",
        model_id="loggan_box",
        base_numeric_id=1030,
        name="Loggan",
        gen=3,
    )

    model_def.add_unit_def(unit_cls_name="DieselEngineFeldbahnGen3B")

    model_def.add_unit_def(unit_cls_name="WagonFeldbahnA", repeat=12)

    result.append(model_def)
    return result
