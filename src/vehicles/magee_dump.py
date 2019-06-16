from road_vehicle import DumpFeldbahnConsist
from base_platforms.feldbahn import DieselEngineFeldbahnGen3B, WagonFeldbahnA

consist = DumpFeldbahnConsist(id='magee_dump',
                       base_numeric_id=1020,
                       name='Magee',
                       gen=3)

consist.add_unit(base_platform=DieselEngineFeldbahnGen3B)

consist.add_unit(base_platform=WagonFeldbahnA,
                 repeat=12) # 12 * 3 = 36, then +4 for engine = 40, 2.5 tiles,  integer tile lengths  are not needed for RVs
