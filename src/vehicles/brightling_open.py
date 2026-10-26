from road_vehicle import OpenTramConsist, ElectricVehicleUnit

from road_vehicle.model_def import ModelDef



def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="OpenTram",
        model_id="brightling_open",
        base_numeric_id=90,
        name="Brightling",
        gen=3,
    )

    model_def.add_unit_def(
        unit_cls_name="ElectricVehicleUnit",
        capacity=0,
        vehicle_length=4,
        always_use_same_spriterow=True,
    )

    model_def.add_unit_def(
        unit_cls_name="ElectricTrailerUnit",
        vehicle_length=6,
        cargo_length=3,
        repeat=2,
    )

    result.append(model_def)
    return result
