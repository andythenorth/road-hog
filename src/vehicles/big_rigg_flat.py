from road_vehicle import FlatbedTruckConsist

from road_vehicle.model_def import ModelDef



def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="FlatbedTruck",
        model_id="big_rigg_flat",
        base_numeric_id=660,
        name="Big Rigg",
        gen=5,
    )

    model_def.add_unit_def(unit_cls_name="DieselCaboverRigidTruckGen5A")

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit",
        vehicle_length=4,
        cargo_length=4,
    )

    result.append(model_def)
    return result
