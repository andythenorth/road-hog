from road_vehicle import TankerFeldbahnConsist

from road_vehicle.model_def import ModelDef



def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="TankerFeldbahn",
        model_id="dry_fork_tanker",
        base_numeric_id=1150,
        name="Dry Fork",
        gen=3,
    )

    model_def.add_unit_def(unit_cls_name="DieselEngineFeldbahnGen3A")

    model_def.add_unit_def(unit_cls_name="WagonFeldbahnA", repeat=5)

    result.append(model_def)
    return result
