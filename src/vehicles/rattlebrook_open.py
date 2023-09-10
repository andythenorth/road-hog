from road_vehicle import OpenTruckConsist
from base_platforms.trucks import DieselCaboverRigidTruckGen3A


def main(roster_id):
    consist = OpenTruckConsist(
        roster_id=roster_id,
        id="rattlebrook_open",
        base_numeric_id=670,
        name="Rattlebrook",
        gen=3,
    )

    consist.add_unit(base_platform=DieselCaboverRigidTruckGen3A)

    consist.add_unit(
        base_platform=None,
        vehicle_length=4,
        cargo_length=4,
    )

    return consist
