from road_vehicle import DumpTruckConsist, DieselVehicleUnit


def main(roster_id):
    consist = DumpTruckConsist(
        roster_id=roster_id,
        id="honister_dump",
        base_numeric_id=230,
        name="Honister",
        gen=3,
        intro_date_offset=7,
    )  # introduce later than gen epoch by design

    consist.add_unit(
        base_platform=None,  # only one instance of this one currently
        type=DieselVehicleUnit,
        vehicle_length=5,
        effects=["EFFECT_SPRITE_DIESEL, -2, 1, 10"],
    )

    consist.add_unit(base_platform=None, vehicle_length=4)

    return consist
