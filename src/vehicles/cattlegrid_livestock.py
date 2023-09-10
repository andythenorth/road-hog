from road_vehicle import LivestockFeldbahnConsist
from base_platforms.feldbahn import DieselEngineFeldbahnGen3B, WagonFeldbahnA


def main(roster_id):
    consist = LivestockFeldbahnConsist(
        roster_id=roster_id,
        id="cattlegrid_livestock",
        base_numeric_id=1170,
        name="Cattlegrid",
        gen=3,
    )

    consist.add_unit(base_platform=DieselEngineFeldbahnGen3B)

    consist.add_unit(base_platform=WagonFeldbahnA, repeat=12)

    return consist
