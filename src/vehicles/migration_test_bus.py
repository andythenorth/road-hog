"""One existing-equivalent vehicle for testing the migration factory path.

Retain the original Leyburn IDs and graphics lookup until the new framework
is wired up. This definition is deliberately in Road Hog's legacy format.
"""

from road_vehicle import PaxLocalBusConsist, DieselVehicleUnit


def main(roster_id):
    consist = PaxLocalBusConsist(
        roster_id=roster_id,
        id="leyburn_pax",
        base_numeric_id=20,
        name="Leyburn",
        power=100,
        speed=40,
        gen=2,
        intro_date_offset=-1,
    )
    consist.add_unit(
        base_platform=None,
        type=DieselVehicleUnit,
        vehicle_length=7,
    )
    return consist
