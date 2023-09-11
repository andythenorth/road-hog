from road_vehicle import FlatbedTramConsist
from base_platforms.trams import ElectricMotorTram2


def main(roster_id):
    consist = FlatbedTramConsist(
        roster_id=roster_id,
        id="rackwood_flat",
        base_numeric_id=740,
        name="Rackwood",
        gen=2,
    )

    consist.add_unit(base_platform=ElectricMotorTram2, repeat=2)

    return consist
