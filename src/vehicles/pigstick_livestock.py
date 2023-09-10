from road_vehicle import LivestockTruckConsist, DieselVehicleUnit


def main(roster_id):
    consist = LivestockTruckConsist(
        roster_id=roster_id,
        id="pigstick_livestock",
        base_numeric_id=330,
        name="Pigstick",
        gen=3,
        intro_date_offset=2,
    )  # introduce later than gen epoch by design

    consist.add_unit(
        base_platform=None,  # only one instance of this one currently
        type=DieselVehicleUnit,
        vehicle_length=6,
        always_use_same_spriterow=True,
    )  # !! because livestock gestalt only has one spriterow - could be done better??

    consist.add_unit(base_platform=None, vehicle_length=4)

    return consist
