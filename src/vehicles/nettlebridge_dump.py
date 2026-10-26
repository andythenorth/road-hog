from road_vehicle import DumpTramConsist, ElectricVehicleUnit

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(
        schema_name="DumpTram",
        model_id="nettlebridge_dump",
        base_numeric_id=310,
        name="Nettlebridge",
        gen=3,
        intro_year_offset=4,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(
        
        unit_cls_name="ElectricVehicleUnit",
        capacity=0,
        vehicle_length=4,
        always_use_same_spriterow=True,
    )

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit",
        
        vehicle_length=6,
        repeat=2,
    )

    return [model_def]
