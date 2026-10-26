from road_vehicle import OpenTruckConsist

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="OpenTruck",
        model_id="wastelander_open",
        base_numeric_id=1010,
        name="Wastelander",
        roadveh_flag_tram=True,
        power=90,
        gen=4,
        intro_date=1870,
    )

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit", capacity=0, vehicle_length=4
    )

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit", capacity=10, vehicle_length=3, repeat=2
    )

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit", capacity=10, vehicle_length=3
    )

    result.append(model_def)
    return result
