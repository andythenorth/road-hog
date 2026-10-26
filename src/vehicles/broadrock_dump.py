from road_vehicle.model_def import ModelDef


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="DumpHEQS",
        model_id="broadrock_dump",
        base_numeric_id=100,
        name="Broadrock",
        power=400,
        speed=40,  # dibbled up above RL for game balance
        # CABBAGE type_base_running_cost_points=20,  # dibble running costs for game balance
        gen=3,
        intro_year_offset=-3,
    )  # introduce earlier than gen epoch by design

    model_def.add_unit_def(
        unit_cls_name="DieselConventionalCabSemiTractorHaulerGen3A",
    )

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit",
        vehicle_length=6,
    )

    result.append(model_def)
    return result
