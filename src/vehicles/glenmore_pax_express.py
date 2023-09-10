from road_vehicle import PaxExpressCoachConsist, DieselVehicleUnit

# for each generation, bus and coach variants have same power and intro date
# coaches faster, lower capacity than equivalent bus


def main(roster_id):
    consist = PaxExpressCoachConsist(
        roster_id=roster_id,
        id="glenmore_pax_express",
        base_numeric_id=50,
        name="Glenmore",
        power=160,
        speed=55,
        gen=3,
        intro_date_offset=-4,
    )  # introduce earlier than gen epoch by design

    consist.add_unit(
        base_platform=None,  # coaches have no base platform by design currently
        type=DieselVehicleUnit,
        vehicle_length=7,
    )

    return consist
