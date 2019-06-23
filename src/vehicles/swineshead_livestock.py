from road_vehicle import LivestockTruckConsist
from base_platforms.trucks import DieselCaboverRigidTruckGen4B

consist = LivestockTruckConsist(id='swineshead_livestock',
                         base_numeric_id=440,
                         name='Swineshead',
                         gen=4,
                         intro_date_offset=2)  # introduce later than gen epoch by design

consist.add_unit(base_platform=DieselCaboverRigidTruckGen4B,
                 always_use_same_spriterow = True) # !! because livestock gestalt only has one spriterow - could be done better??

consist.add_unit(base_platform=None,
                 vehicle_length=4)
