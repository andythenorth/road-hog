from road_vehicle import DumpTruckConsist
from base_platforms.trucks import SteamCaboverSemiTractorTruckGen2A


def main(roster_id):
    consist = DumpTruckConsist(
        roster_id=roster_id,
        id="coleman_dump",
        base_numeric_id=910,
        name="Coleman",
        gen=2,
        intro_date_offset=7,
    )  # introduce later than gen epoch by design

    consist.add_unit(base_platform=SteamCaboverSemiTractorTruckGen2A)

    consist.add_unit(base_platform=None, vehicle_length=5)

    return consist
