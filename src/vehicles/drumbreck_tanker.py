from road_vehicle import TankerTramConsist

from road_vehicle.model_def import ModelDef



def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="TankerTram",
        model_id="drumbreck_tanker",
        base_numeric_id=800,
        name="Drumbreck",
        gen=1,
        intro_year_offset=4,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(unit_cls_name="SteamEngineTram1")

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit",
        vehicle_length=4,
        repeat=3,
    )

    result.append(model_def)
    return result
