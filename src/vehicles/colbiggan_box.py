from road_vehicle import BoxTramConsist
from base_platforms.trams import ElectricMotorTram4


def main(roster_id):
    consist = BoxTramConsist(
        roster_id=roster_id,
        id="colbiggan_box",
        base_numeric_id=880,
        name="Colbiggan",
        gen=3,
    )

    consist.add_unit(base_platform=ElectricMotorTram4, repeat=2)

    return consist
