from road_vehicle import FlatbedTramConsist

from road_vehicle.model_def import ModelDef



def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="FlatbedTram",
        model_id="rackwood_flat",
        base_numeric_id=740,
        name="Rackwood",
        gen=2,
    )

    model_def.add_unit_def(unit_cls_name="ElectricMotorTram2", repeat=2)

    result.append(model_def)
    return result
