from road_vehicle import FruitVegFeldbahnConsist
from base_platforms.feldbahn import DieselEngineFeldbahnGen3B, WagonFeldbahnA

consist = FruitVegFeldbahnConsist(id='redbeet_fruit_veg',
                       base_numeric_id=1250,
                       name='Redbeet',
                       gen=3)

consist.add_unit(base_platform=DieselEngineFeldbahnGen3B)

consist.add_unit(base_platform=WagonFeldbahnA,
                 repeat=12)
