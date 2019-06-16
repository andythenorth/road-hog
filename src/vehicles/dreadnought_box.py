from road_vehicle import BoxFeldbahnConsist
from base_platforms.feldbahn import DieselEngineFeldbahn2, OpenWagonFeldbahnGen2

consist = BoxFeldbahnConsist(id='dreadnought_box',
                       base_numeric_id=1100,
                       name='Dreadnought',
                       gen=2)

consist.add_unit(base_platform=DieselEngineFeldbahn2)

consist.add_unit(base_platform=OpenWagonFeldbahnGen2,
                 repeat=12)
