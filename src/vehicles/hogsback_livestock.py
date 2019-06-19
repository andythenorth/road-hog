from road_vehicle import LivestockFeldbahnConsist
from base_platforms.feldbahn import DieselEngineFeldbahnGen3A, WagonFeldbahnA

consist = LivestockFeldbahnConsist(id='hogsback_livestock',
                       base_numeric_id=1210,
                       name='Hogsback',
                       gen=3)

consist.add_unit(base_platform=DieselEngineFeldbahnGen3A)

consist.add_unit(base_platform=WagonFeldbahnA,
                 repeat=5)
