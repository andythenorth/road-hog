from road_vehicle import EdiblesTankerTruckConsist
from base_platforms.trucks import SteamCaboverRigidTruckGen2A


def main(roster_id):
    consist = EdiblesTankerTruckConsist(
        roster_id=roster_id,
        id="flow_edge_edibles_tanker",
        base_numeric_id=930,
        name="Flow Edge",
        gen=2,
        intro_date_offset=2,
    )  # introduce later than gen epoch by design

    consist.add_unit(base_platform=SteamCaboverRigidTruckGen2A)

    consist.add_unit(base_platform=None, vehicle_length=4)

    return consist
