from road_vehicle.model_def import ModelDef


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="EdiblesTankerTruck",
        model_id="silvertop_edibles_tanker",
        base_numeric_id=380,
        name="Silvertop",
        gen=5,
        intro_year_offset=4,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(unit_cls_name="DieselCaboverRigidTruckGen5A")

    model_def.add_unit_def(unit_cls_name="RoadVehicleUnit", vehicle_length=4)

    result.append(model_def)
    return result
