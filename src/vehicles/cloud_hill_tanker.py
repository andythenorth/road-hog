from road_vehicle import TankerTruckConsist
from base_platforms.trucks import DieselCaboverSemiTractorTruckGen5A


def main(roster_id):
    consist = TankerTruckConsist(
        roster_id=roster_id,
        id="cloud_hill_tanker",
        base_numeric_id=130,
        name="Cloud Hill",
        gen=5,
        intro_date_offset=4,
    )  # introduce later than gen epoch by design

    consist.add_unit(base_platform=DieselCaboverSemiTractorTruckGen5A)

    consist.add_unit(base_platform=None, vehicle_length=7)

    return consist
