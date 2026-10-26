from road_vehicle.model_def import ModelDef


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="EdiblesTankerTruck",
        model_id="flow_edge_edibles_tanker",
        base_numeric_id=930,
        name="Flow Edge",
        gen=2,
        intro_year_offset=2,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(unit_cls_name="SteamCaboverRigidTruckGen2A")

    model_def.add_unit_def(unit_cls_name="RoadVehicleUnit", vehicle_length=4)

    result.append(model_def)
    return result
