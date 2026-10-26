from road_vehicle import OpenTramConsist, ElectricVehicleUnit

from road_vehicle.model_def import ModelDef



def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="OpenTram",
        model_id="portland_open",
        base_numeric_id=860,
        name="Portland",
        gen=2,
    )

    model_def.add_unit_def(
        unit_cls_name="ElectricVehicleUnit",
        vehicle_length=8,
        cargo_length=3,
        repeat=2,
    )

    result.append(model_def)
    return result
