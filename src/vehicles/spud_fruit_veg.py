from road_vehicle import FruitVegFeldbahnConsist
from base_platforms.feldbahn import DieselEngineFeldbahnGen3A, WagonFeldbahnA


def main(roster_id):
    consist = FruitVegFeldbahnConsist(
        roster_id=roster_id,
        id="spud_fruit_veg",
        base_numeric_id=1260,
        name="Spud",
        gen=3,
    )

    consist.add_unit(base_platform=DieselEngineFeldbahnGen3A)

    consist.add_unit(base_platform=WagonFeldbahnA, repeat=5)

    return consist
