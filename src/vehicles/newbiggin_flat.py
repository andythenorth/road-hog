from road_vehicle import FlatFeldbahnConsist

from road_vehicle.model_def import ModelDef



def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="FlatFeldbahn",
        model_id="newbiggin_flat",
        base_numeric_id=1110,
        name="Newbiggin",
        gen=2,
    )

    model_def.add_unit_def(unit_cls_name="SteamEngineFeldbahnGen2B")

    model_def.add_unit_def(unit_cls_name="WagonFeldbahnA", repeat=12)

    result.append(model_def)
    return result
