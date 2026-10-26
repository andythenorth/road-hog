from road_vehicle import CoveredHopperTramConsist

from road_vehicle.model_def import ModelDef



def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="CoveredHopperTram",
        model_id="polangrain_covered_hopper",
        base_numeric_id=790,
        name="Polangrain",
        gen=2,
    )

    model_def.add_unit_def(unit_cls_name="ElectricMotorTram2", repeat=2)

    result.append(model_def)
    return result
