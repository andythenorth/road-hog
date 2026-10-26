from road_vehicle import PaxExpressCoachConsist, DieselVehicleUnit

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.

# for each generation, bus and coach variants have same power and intro date
# coaches faster, lower capacity than equivalent bus


def main(roster_id):
    model_def = ModelDef(
        schema_name="PaxExpressCoach",
        model_id="oxleas_pax_express",
        base_numeric_id=610,
        name="Oxleas",
        power=240,
        speed=75,
        gen=4,
        intro_year_offset=-4,
    )  # introduce earlier than gen epoch by design

    model_def.add_unit_def(
        
        unit_cls_name="DieselVehicleUnit",
        vehicle_length=7,
    )

    return [model_def]
