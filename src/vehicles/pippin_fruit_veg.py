from road_vehicle import FruitVegFeldbahnConsist
from base_platforms.feldbahn import SteamEngineFeldbahnGen1A, WagonFeldbahnA

consist = FruitVegFeldbahnConsist(id='pippin_fruit_veg',
                       base_numeric_id=1240,
                       name='Pippin',
                       gen=1)

consist.add_unit(base_platform=SteamEngineFeldbahnGen1A)

consist.add_unit(base_platform=WagonFeldbahnA,
                 repeat=5)
