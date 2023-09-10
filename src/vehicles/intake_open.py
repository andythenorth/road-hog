from road_vehicle import OpenFeldbahnConsist
from base_platforms.feldbahn import SteamEngineFeldbahnGen1A, WagonFeldbahnA


def main(roster_id):
    consist = OpenFeldbahnConsist(
        roster_id=roster_id, id="intake_open", base_numeric_id=730, name="Intake", gen=1
    )

    consist.add_unit(base_platform=SteamEngineFeldbahnGen1A)

    consist.add_unit(base_platform=WagonFeldbahnA, repeat=5)

    return consist
