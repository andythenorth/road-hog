from road_vehicle import FruitVegFeldbahnConsist
from base_platforms.feldbahn import SteamEngineFeldbahnGen2B, WagonFeldbahnA


def main(roster_id):
    consist = FruitVegFeldbahnConsist(
        roster_id=roster_id,
        id="greenleaf_fruit_veg",
        base_numeric_id=1230,
        name="Greenleaf",
        gen=2,
    )

    consist.add_unit(base_platform=SteamEngineFeldbahnGen2B)

    consist.add_unit(base_platform=WagonFeldbahnA, repeat=12)

    return consist
