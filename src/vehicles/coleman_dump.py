from road_vehicle import DumpTruckConsist

from road_vehicle.model_def import ModelDef



def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="DumpTruck",
        model_id="coleman_dump",
        base_numeric_id=910,
        name="Coleman",
        gen=2,
        intro_year_offset=7,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(unit_cls_name="SteamCaboverSemiTractorTruckGen2A")

    model_def.add_unit_def(unit_cls_name="RoadVehicleUnit", vehicle_length=5)

    result.append(model_def)
    return result
