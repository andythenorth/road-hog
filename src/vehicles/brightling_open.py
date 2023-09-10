from road_vehicle import OpenTramConsist, ElectricVehicleUnit


def main(roster_id):
    consist = OpenTramConsist(
        roster_id=roster_id,
        id="brightling_open",
        base_numeric_id=90,
        name="Brightling",
        gen=3,
    )

    consist.add_unit(
        base_platform=None,  # no base platform by design currently
        type=ElectricVehicleUnit,
        capacity=0,
        vehicle_length=4,
        always_use_same_spriterow=True,
    )

    consist.add_unit(
        base_platform=None,  # no base platform by design currently
        vehicle_length=6,
        cargo_length=3,
        repeat=2,
    )

    return consist
