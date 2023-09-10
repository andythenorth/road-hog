from road_vehicle import FruitVegTramConsist
from base_platforms.trams import ElectricMotorTram4


def main(roster_id):
    consist = FruitVegTramConsist(
        roster_id=roster_id,
        id="nutbrook_fruit_veg",
        base_numeric_id=960,
        name="Nutbrook",
        gen=3,
    )

    consist.add_unit(base_platform=ElectricMotorTram4, repeat=2)

    return consist
