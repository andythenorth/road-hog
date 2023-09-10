from road_vehicle import FlatFeldbahnConsist
from base_platforms.feldbahn import DieselEngineFeldbahnGen3A, WagonFeldbahnA


def main(roster_id):
    consist = FlatFeldbahnConsist(
        roster_id=roster_id, id="kedge_flat", base_numeric_id=1060, name="Kedge", gen=3
    )

    consist.add_unit(base_platform=DieselEngineFeldbahnGen3A)

    consist.add_unit(base_platform=WagonFeldbahnA, repeat=5)

    return consist
