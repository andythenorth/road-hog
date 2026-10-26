from road_vehicle import SuppliesCakeConsist, DieselVehicleUnit

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(
        schema_name="SuppliesCake",
        model_id="road_thief_supplies",
        base_numeric_id=560,
        name="Road Thief",
        power=720,
        gen=4,
    )

    model_def.add_unit_def(
        
        unit_cls_name="DieselVehicleUnit",
        capacity=0,
        vehicle_length=7,
        always_use_same_spriterow=True,
    )

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit",
        
        # capacity=45,
        vehicle_length=7,
    )

    return [model_def]
