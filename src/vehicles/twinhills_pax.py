from road_vehicle import PaxLocalTramConsist, ElectricVehicleUnit

from road_vehicle.model_def import ModelDef



def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="PaxLocalTram",
        model_id="twinhills_pax",
        base_numeric_id=70,
        name="Twinhills",
        gen=5,
    )

    model_def.add_unit_def(
        unit_cls_name="ElectricVehicleUnit",
        vehicle_length=8,
        repeat=2,
    )

    result.append(model_def)
    return result
