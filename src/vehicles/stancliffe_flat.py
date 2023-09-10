from road_vehicle import FlatbedTramConsist
from base_platforms.trams import ElectricMotorTram4


def main(roster_id):
    consist = FlatbedTramConsist(
        roster_id=roster_id,
        id="stancliffe_flat",
        base_numeric_id=410,
        name="Stancliffe",
        gen=3,
    )

    consist.add_unit(base_platform=ElectricMotorTram4, repeat=2)

    return consist
