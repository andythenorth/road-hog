from road_vehicle import BoxTruckConsist
from base_platforms.trucks import DieselCaboverSemiTractorTruckGen5A


def main(roster_id):
    consist = BoxTruckConsist(
        roster_id=roster_id,
        id="speedwell_box",
        base_numeric_id=400,
        name="Speedwell",
        gen=5,
    )

    consist.add_unit(base_platform=DieselCaboverSemiTractorTruckGen5A)

    consist.add_unit(base_platform=None, vehicle_length=7)

    return consist
