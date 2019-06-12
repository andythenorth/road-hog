from road_vehicle import DumpFeldbahnConsist
from base_platforms.feldbahn import DieselEngineFeldbahn1, OpenWagonFeldbahnGen3

consist = DumpFeldbahnConsist(id='eidsborg_dump',
                       base_numeric_id=140,
                       name='Eidsborg',
                       gen=3)

consist.add_unit(base_platform=DieselEngineFeldbahn1)

consist.add_unit(base_platform=OpenWagonFeldbahnGen3,
                 repeat=3)
