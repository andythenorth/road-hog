from road_vehicle import EdiblesTankerTruckConsist
from base_platforms.trucks import DieselCaboverRigidTruckGen5A


def main(roster_id):
    consist = EdiblesTankerTruckConsist(
        roster_id=roster_id,
        id="silvertop_edibles_tanker",
        base_numeric_id=380,
        name="Silvertop",
        gen=5,
        intro_date_offset=4,
    )  # introduce later than gen epoch by design

    consist.add_unit(base_platform=DieselCaboverRigidTruckGen5A)

    consist.add_unit(base_platform=None, vehicle_length=4)

    return consist
