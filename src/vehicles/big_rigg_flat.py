from road_vehicle import FlatbedTruckConsist
from base_platforms.trucks import DieselCaboverRigidTruckGen5A


def main(roster_id):
    consist = FlatbedTruckConsist(
        roster_id=roster_id,
        id="big_rigg_flat",
        base_numeric_id=660,
        name="Big Rigg",
        gen=5,
    )

    consist.add_unit(base_platform=DieselCaboverRigidTruckGen5A)

    consist.add_unit(base_platform=None, vehicle_length=4, cargo_length=4)

    return consist
