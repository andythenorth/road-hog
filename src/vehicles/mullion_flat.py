from road_vehicle import FlatFeldbahnConsist

from road_vehicle.model_def import ModelDef



def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="FlatFeldbahn",
        model_id="mullion_flat",
        base_numeric_id=1040,
        name="Mullion",
        gen=1,
    )

    model_def.add_unit_def(unit_cls_name="SteamEngineFeldbahnGen1A")

    model_def.add_unit_def(unit_cls_name="WagonFeldbahnA", repeat=5)

    result.append(model_def)
    return result
