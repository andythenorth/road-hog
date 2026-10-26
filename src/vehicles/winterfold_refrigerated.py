from road_vehicle import RefrigeratedTramConsist, ElectricVehicleUnit

from road_vehicle.model_def import ModelDef



def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="RefrigeratedTram",
        model_id="winterfold_refrigerated",
        base_numeric_id=770,
        name="Winterfold",
        gen=2,
        intro_year_offset=10,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(
        unit_cls_name="ElectricVehicleUnit",
        vehicle_length=8,
        repeat=2,
    )

    result.append(model_def)
    return result
