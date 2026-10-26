from road_vehicle.model_def import ModelDef


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="BoxTruck",
        model_id="easywheal_box",
        base_numeric_id=160,
        name="Easywheal",
        gen=3,
    )

    model_def.add_unit_def(
        unit_cls_name="DieselConventionalCabSemiTractorTruckGen3A",
    )

    model_def.add_unit_def(unit_cls_name="RoadVehicleUnit", vehicle_length=5)

    result.append(model_def)
    return result
