from road_vehicle import FruitVegTramConsist

from road_vehicle.model_def import ModelDef



def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="FruitVegTram",
        model_id="plumley_fruit_veg",
        base_numeric_id=950,
        name="Plumley",
        gen=1,
        intro_year_offset=1,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(unit_cls_name="SteamEngineTram1")

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit",
        vehicle_length=4,
        repeat=3,
    )

    result.append(model_def)
    return result
