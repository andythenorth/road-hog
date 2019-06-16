from road_vehicle import OpenFeldbahnConsist
from base_platforms.feldbahn import DieselEngineFeldbahn2, OpenWagonFeldbahnGen3

consist = OpenFeldbahnConsist(id='dinkum_open',
                       base_numeric_id=990,
                       name='Dinkum',
                       gen=3)

consist.add_unit(base_platform=DieselEngineFeldbahn2)


consist.add_unit(base_platform=OpenWagonFeldbahnGen3,
                 repeat=12)
