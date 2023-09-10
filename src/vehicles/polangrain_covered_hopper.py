from road_vehicle import CoveredHopperTramConsist
from base_platforms.trams import ElectricMotorTram2


def main(roster_id):
    consist = CoveredHopperTramConsist(
        roster_id=roster_id,
        id="polangrain_covered_hopper",
        base_numeric_id=790,
        name="Polangrain",
        gen=2,
    )

    consist.add_unit(base_platform=ElectricMotorTram2, repeat=2)

    return consist
