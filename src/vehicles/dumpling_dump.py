from road_vehicle import DumpFeldbahnConsist
from base_platforms.feldbahn import SteamEngineFeldbahnGen1A, WagonFeldbahnA


def main(roster_id):
    consist = DumpFeldbahnConsist(
        roster_id=roster_id,
        id="dumpling_dump",
        base_numeric_id=980,
        name="Dumpling",
        gen=1,
    )

    consist.add_unit(base_platform=SteamEngineFeldbahnGen1A)

    consist.add_unit(base_platform=WagonFeldbahnA, repeat=5)

    return consist
