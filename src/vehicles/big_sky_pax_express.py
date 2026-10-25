from road_vehicle import PaxExpressCoachConsist, DieselVehicleUnit

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.

# !! unused ??
# for each generation, bus and coach variants have same power and intro date
# coaches faster, lower capacity than equivalent bus


def main(roster_id):
    model_def = ModelDef(
        schema_name="PaxExpressCoach",
        model_id="big_sky_pax_express",
        base_numeric_id=620,
        name="Big Sky",
        power=220,
        speed=90,
        gen=4,
        intro_date=1990,
    )

    model_def.add_unit_def(
        base_platform=None,  # coaches have no base platform by design currently
        unit_cls_name="DieselVehicleUnit",
        vehicle_length=7,
    )

    return [model_def]
