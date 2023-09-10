from road_vehicle import RefrigeratedTruckConsist
from base_platforms.trucks import DieselCaboverSemiTractorTruckGen5A


def main(roster_id):
    consist = RefrigeratedTruckConsist(
        roster_id=roster_id,
        id="coldfall_refrigerated",
        base_numeric_id=150,
        name="Coldfall",
        gen=5,
        intro_date_offset=1,
    )  # introduce later than gen epoch by design

    consist.add_unit(base_platform=DieselCaboverSemiTractorTruckGen5A)

    consist.add_unit(base_platform=None, vehicle_length=8)

    return consist
