from road_vehicle import SuppliesCakeConsist, DieselVehicleUnit


def main(roster_id):
    consist = SuppliesCakeConsist(
        roster_id=roster_id,
        id="road_thief_supplies",
        base_numeric_id=560,
        name="Road Thief",
        power=720,
        gen=4,
    )

    consist.add_unit(
        base_platform=None,  # no base platform by design currently
        type=DieselVehicleUnit,
        capacity=0,
        vehicle_length=7,
        always_use_same_spriterow=True,
    )

    consist.add_unit(
        base_platform=None,  # no base platform by design currently
        # capacity=45,
        vehicle_length=7,
    )

    return consist
