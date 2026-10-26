from road_vehicle import PaxExpressCoachConsist, DieselVehicleUnit

from road_vehicle.model_def import ModelDef


# !! unused ??
# for each generation, bus and coach variants have same power and intro date
# coaches faster, lower capacity than equivalent bus


def main(roster_id):
    result = []

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
        unit_cls_name="DieselVehicleUnit",
        vehicle_length=7,
    )

    result.append(model_def)
    return result
