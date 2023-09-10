from road_vehicle import EdiblesTankerTruckConsist
from base_platforms.trucks import DieselCaboverRigidTruckGen4A


def main(roster_id):
    consist = EdiblesTankerTruckConsist(
        roster_id=roster_id,
        id="waterperry_edibles_tanker",
        base_numeric_id=470,
        name="Waterperry",
        gen=4,
        intro_date_offset=4,
    )  # introduce later than gen epoch by design

    consist.add_unit(base_platform=DieselCaboverRigidTruckGen4A)

    consist.add_unit(base_platform=None, vehicle_length=4)

    return consist
