from road_vehicle import BoxTramConsist
from base_platforms.trams import ElectricMotorTram3


def main(roster_id):
    consist = BoxTramConsist(
        roster_id=roster_id,
        id="rakeway_box",
        base_numeric_id=870,
        name="Rakeway",
        gen=2,
    )

    consist.add_unit(base_platform=ElectricMotorTram3, repeat=2)

    return consist
