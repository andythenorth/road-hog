from road_vehicle import OpenTramConsist
from base_platforms.trams import SteamEngineTram1


def main(roster_id):
    consist = OpenTramConsist(
        roster_id=roster_id,
        id="buildwas_open",
        base_numeric_id=120,
        name="Buildwas",
        gen=1,
    )

    consist.add_unit(base_platform=SteamEngineTram1)

    consist.add_unit(
        base_platform=None,  # no base platform by design currently
        vehicle_length=4,
        cargo_length=4,
        repeat=3,
    )

    return consist
