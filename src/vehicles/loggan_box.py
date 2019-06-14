from road_vehicle import BoxFeldbahnConsist
from base_platforms.feldbahn import DieselEngineFeldbahn1, OpenWagonFeldbahnGen3

consist = BoxFeldbahnConsist(id='loggan_box',
                       base_numeric_id=1030,
                       name='Loggan',
                       gen=3)

consist.add_unit(base_platform=DieselEngineFeldbahn1)

consist.add_unit(base_platform=OpenWagonFeldbahnGen3,
                 repeat=5)
