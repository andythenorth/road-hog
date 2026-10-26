from road_vehicle import DumpTruckConsist, DieselVehicleUnit

from road_vehicle.model_def import ModelDef



def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="DumpTruck",
        model_id="honister_dump",
        base_numeric_id=230,
        name="Honister",
        gen=3,
        intro_year_offset=7,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(
        unit_cls_name="DieselVehicleUnit",
        vehicle_length=5,
        effects=["EFFECT_SPRITE_DIESEL, -2, 1, 10"],
    )

    model_def.add_unit_def(unit_cls_name="RoadVehicleUnit", vehicle_length=4)

    result.append(model_def)
    return result
