from road_vehicle import PaxLocalTramConsist, ElectricVehicleUnit

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(
        schema_name="PaxLocalTram",
        model_id="fairlop_pax",
        base_numeric_id=10,
        name="Fairlop",
        gen=2,
        intro_year_offset=3,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(
        
        unit_cls_name="ElectricVehicleUnit",
        vehicle_length=6,
        effects=["EFFECT_SPRITE_ELECTRIC, 0, 0, 12"],
    )

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit",
        
        vehicle_length=5,
        repeat=2,
    )

    return [model_def]
