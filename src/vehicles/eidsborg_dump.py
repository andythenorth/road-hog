from road_vehicle import DumpFeldbahnConsist
from base_platforms.feldbahn import DieselEngineFeldbahnGen3A, WagonFeldbahnA


def main(roster_id):
    consist = DumpFeldbahnConsist(
        roster_id=roster_id,
        id="eidsborg_dump",
        base_numeric_id=140,
        name="Eidsborg",
        gen=3,
    )

    consist.add_unit(base_platform=DieselEngineFeldbahnGen3A)

    consist.add_unit(base_platform=WagonFeldbahnA, repeat=5)

    return consist
