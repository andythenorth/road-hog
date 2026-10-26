from road_vehicle import TankerFeldbahnConsist

from road_vehicle.model_def import ModelDef



def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="TankerFeldbahn",
        model_id="irvine_tanker",
        base_numeric_id=1130,
        name="Irvine",
        gen=3,
    )

    model_def.add_unit_def(unit_cls_name="SteamEngineFeldbahnGen2B")

    model_def.add_unit_def(unit_cls_name="WagonFeldbahnA", repeat=12)

    result.append(model_def)
    return result
