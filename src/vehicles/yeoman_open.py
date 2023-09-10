from road_vehicle import OpenTruckConsist
from base_platforms.trucks import DieselConventionalCabSemiTractorTruckGen4A


def main(roster_id):
    consist = OpenTruckConsist(
        roster_id=roster_id, id="yeoman_open", base_numeric_id=170, name="Yeoman", gen=4
    )

    consist.add_unit(base_platform=DieselConventionalCabSemiTractorTruckGen4A)

    consist.add_unit(base_platform=None, vehicle_length=7, cargo_length=7)

    return consist
