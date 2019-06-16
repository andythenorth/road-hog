from road_vehicle import DumpFeldbahnConsist
from base_platforms.feldbahn import DieselEngineFeldbahn2, OpenWagonFeldbahnGen2

consist = DumpFeldbahnConsist(id='jumbo_dump',
                       base_numeric_id=1080,
                       name='Jumbo',
                       gen=2)

consist.add_unit(base_platform=DieselEngineFeldbahn2)

consist.add_unit(base_platform=OpenWagonFeldbahnGen2,
                 repeat=12) # 12 * 3 = 36, then +4 for engine = 40, 2.5 tiles,  integer tile lengths  are not needed for RVs
