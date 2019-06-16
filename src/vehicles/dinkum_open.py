from road_vehicle import OpenFeldbahnConsist
from base_platforms.feldbahn import DieselEngineFeldbahnGen3B, WagonFeldbahnA

consist = OpenFeldbahnConsist(id='dinkum_open',
                       base_numeric_id=990,
                       name='Dinkum',
                       gen=3)

consist.add_unit(base_platform=DieselEngineFeldbahnGen3B)


consist.add_unit(base_platform=WagonFeldbahnA,
                 repeat=12)
