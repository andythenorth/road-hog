from road_vehicle import TankerFeldbahnConsist
from base_platforms.feldbahn import SteamEngineFeldbahnGen2A, WagonFeldbahnA


def main(roster_id):
    consist = TankerFeldbahnConsist(
        roster_id=roster_id,
        id="hopping_pipe_tanker",
        base_numeric_id=1140,
        name="Hopping Pipe",
        gen=2,
    )

    consist.add_unit(base_platform=SteamEngineFeldbahnGen2A)

    consist.add_unit(base_platform=WagonFeldbahnA, repeat=5)

    return consist
