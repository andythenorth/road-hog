from road_vehicle import TankerTruckConsist
from base_platforms.trucks import DieselConventionalCabSemiTractorTruckGen3A


def main(roster_id):
    consist = TankerTruckConsist(
        roster_id=roster_id,
        id="greenscoe_tanker",
        base_numeric_id=210,
        name="Greenscoe",
        gen=3,
        intro_date_offset=3,
    )  # introduce later than gen epoch by design

    consist.add_unit(base_platform=DieselConventionalCabSemiTractorTruckGen3A)

    consist.add_unit(base_platform=None, vehicle_length=5)

    return consist
