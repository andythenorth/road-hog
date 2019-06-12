from road_vehicle import DumpFeldbahnConsist
from base_platforms.feldbahn import DieselEngineFeldbahn2, OpenWagonFeldbahnGen3

consist = DumpFeldbahnConsist(id='magee_dump',
                       base_numeric_id=1020,
                       name='Magee',
                       gen=4)

consist.add_unit(base_platform=DieselEngineFeldbahn2)

consist.add_unit(base_platform=OpenWagonFeldbahnGen3,
                 repeat=3)
