from road_vehicle import SuppliesCakeConsist, DieselVehicleUnit

from road_vehicle.model_def import ModelDef


# equiv. Scammell Highwayman or Explorer with dolly low loader trailer - not huge


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="SuppliesCake",
        model_id="brigand_supplies",
        base_numeric_id=540,
        name="Brigand",
        power=480,
        gen=3,
    )

    model_def.add_unit_def(
        unit_cls_name="DieselVehicleUnit",
        capacity=0,
        vehicle_length=6,
        always_use_same_spriterow=True,
    )

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit",
        # capacity=45,
        vehicle_length=7,
    )

    model_def.add_unit_def(
        unit_cls_name="DieselVehicleUnit",
        capacity=0,
        vehicle_length=6,
        # CABBAGE unit_num_providing_spriterow_num=0,
        always_use_same_spriterow=True,
    )

    result.append(model_def)
    return result
