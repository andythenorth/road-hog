from road_vehicle import FlatFeldbahnConsist
from base_platforms.feldbahn import DieselEngineFeldbahn2, OpenWagonFeldbahnGen3

consist = FlatFeldbahnConsist(id='dora_flat',
                       base_numeric_id=1070,
                       name='Dora',
                       gen=3)

consist.add_unit(base_platform=DieselEngineFeldbahn2)

consist.add_unit(base_platform=OpenWagonFeldbahnGen3,
                 repeat=12)
