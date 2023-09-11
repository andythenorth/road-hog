from road_vehicle import FlatbedTruckConsist
from base_platforms.trucks import SteamCaboverRigidTruckGen2A


def main(roster_id):
    consist = FlatbedTruckConsist(
        roster_id=roster_id,
        id="chainburn_flat",
        base_numeric_id=630,
        name="Chainburn",
        gen=2,
    )

    consist.add_unit(base_platform=SteamCaboverRigidTruckGen2A)

    consist.add_unit(base_platform=None, vehicle_length=4, cargo_length=4)

    return consist
