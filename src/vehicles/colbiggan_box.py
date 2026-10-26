from road_vehicle import BoxTramConsist

from road_vehicle.model_def import ModelDef



def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="BoxTram",
        model_id="colbiggan_box",
        base_numeric_id=880,
        name="Colbiggan",
        gen=3,
    )

    model_def.add_unit_def(unit_cls_name="ElectricMotorTram4", repeat=2)

    result.append(model_def)
    return result
