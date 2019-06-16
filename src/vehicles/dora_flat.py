from road_vehicle import FlatFeldbahnConsist
from base_platforms.feldbahn import DieselEngineFeldbahnGen3B, WagonFeldbahnA

consist = FlatFeldbahnConsist(id='dora_flat',
                       base_numeric_id=1070,
                       name='Dora',
                       gen=3)

consist.add_unit(base_platform=DieselEngineFeldbahnGen3B)

consist.add_unit(base_platform=WagonFeldbahnA,
                 repeat=12)
