from road_vehicle import RefrigeratedTruckConsist

from road_vehicle.model_def import ModelDef



def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="RefrigeratedTruck",
        model_id="fortiscue_refrigerated",
        base_numeric_id=180,
        name="Fortiscue",
        gen=4,
        intro_year_offset=4,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(
        unit_cls_name="DieselCaboverRigidTruckGen4B",
        always_use_same_spriterow=True,
    )

    model_def.add_unit_def(unit_cls_name="RoadVehicleUnit", vehicle_length=4)

    result.append(model_def)
    return result
