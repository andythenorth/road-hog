from road_vehicle import EdiblesTankerTramConsist
from base_platforms.trams import ElectricMotorTram3


def main(roster_id):
    consist = EdiblesTankerTramConsist(
        roster_id=roster_id,
        id="poptop_edibles_tanker",
        base_numeric_id=780,
        name="Poptop",
        gen=2,
        intro_date_offset=6,
    )  # introduce later than gen epoch by design

    consist.add_unit(base_platform=ElectricMotorTram3, repeat=2)

    return consist
