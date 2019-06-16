from road_vehicle import BoxFeldbahnConsist
from base_platforms.feldbahn import DieselEngineFeldbahnGen3B, WagonFeldbahnA

consist = BoxFeldbahnConsist(id='loggan_box',
                       base_numeric_id=1030,
                       name='Loggan',
                       gen=3)

consist.add_unit(base_platform=DieselEngineFeldbahnGen3B)

consist.add_unit(base_platform=WagonFeldbahnA,
                 repeat=12)
