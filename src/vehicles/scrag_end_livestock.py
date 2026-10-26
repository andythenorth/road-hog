from road_vehicle import LivestockTramConsist

from road_vehicle.model_def import ModelDef



def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="LivestockTram",
        model_id="scrag_end_livestock",
        base_numeric_id=710,
        name="Scrag End",
        gen=1,
    )

    model_def.add_unit_def(unit_cls_name="SteamEngineTram1")

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit",
        vehicle_length=4,
        repeat=3,
    )

    result.append(model_def)
    return result
