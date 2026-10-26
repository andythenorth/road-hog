from road_vehicle.model_def import ModelDef


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="DumpTram",
        model_id="nettlebridge_dump",
        base_numeric_id=310,
        name="Nettlebridge",
        gen=3,
        intro_year_offset=4,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(
        unit_cls_name="ElectricVehicleUnit",
        capacity=0,
        vehicle_length=4,
        always_use_same_spriterow=True,
    )

    model_def.add_unit_def(
        unit_cls_name="ElectricTrailerUnit",
        vehicle_length=6,
        repeat=2,
    )

    result.append(model_def)
    return result
