from road_vehicle import LivestockTruckConsist, DieselVehicleUnit

from road_vehicle.model_def import ModelDef



def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="LivestockTruck",
        model_id="pigstick_livestock",
        base_numeric_id=330,
        name="Pigstick",
        gen=3,
        intro_year_offset=2,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(
        unit_cls_name="DieselVehicleUnit",
        vehicle_length=6,
        always_use_same_spriterow=True,
    )  # !! because livestock gestalt only has one spriterow - could be done better??

    model_def.add_unit_def(unit_cls_name="RoadVehicleUnit", vehicle_length=4)

    result.append(model_def)
    return result
