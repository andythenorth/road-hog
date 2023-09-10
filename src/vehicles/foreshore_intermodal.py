from road_vehicle import IntermodalHaulerConsist


def main(roster_id):
    consist = IntermodalHaulerConsist(
        roster_id=roster_id,
        id="foreshore",
        base_numeric_id=970,
        name="Foreshore",
        power=950,
        gen=4,
        intro_date=1959,
    )

    consist.add_unit(vehicle_length=7)  # capacity=50,

    return consist
