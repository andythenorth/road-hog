from road_vehicle import DumpFeldbahnConsist

from road_vehicle.model_def import ModelDef



def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="DumpFeldbahn",
        model_id="eidsborg_dump",
        base_numeric_id=140,
        name="Eidsborg",
        gen=3,
    )

    model_def.add_unit_def(unit_cls_name="DieselEngineFeldbahnGen3A")

    model_def.add_unit_def(unit_cls_name="WagonFeldbahnA", repeat=5)

    result.append(model_def)
    return result
