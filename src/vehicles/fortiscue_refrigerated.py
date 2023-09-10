from road_vehicle import RefrigeratedTruckConsist
from base_platforms.trucks import DieselCaboverRigidTruckGen4B


def main(roster_id):
    consist = RefrigeratedTruckConsist(
        roster_id=roster_id,
        id="fortiscue_refrigerated",
        base_numeric_id=180,
        name="Fortiscue",
        gen=4,
        intro_date_offset=4,
    )  # introduce later than gen epoch by design

    consist.add_unit(
        base_platform=DieselCaboverRigidTruckGen4B, always_use_same_spriterow=True
    )

    consist.add_unit(base_platform=None, vehicle_length=4)

    return consist
