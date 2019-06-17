from road_vehicle import TankerFeldbahnConsist
from base_platforms.feldbahn import DieselEngineFeldbahnGen3B, WagonFeldbahnA

consist = TankerFeldbahnConsist(id='redoil_tanker',
                       base_numeric_id=1120,
                       name='Redoil',
                       gen=3)

consist.add_unit(base_platform=DieselEngineFeldbahnGen3B)

consist.add_unit(base_platform=WagonFeldbahnA,
                 repeat=12)
