from road_vehicle import DumpFeldbahnConsist
from base_platforms.feldbahn import SteamEngineFeldbahnGen1A, WagonFeldbahnA

consist = DumpFeldbahnConsist(id='dugout_dump',
                       base_numeric_id=1010,
                       name='Dugout',
                       gen=2)

consist.add_unit(base_platform=SteamEngineFeldbahnGen1A)

consist.add_unit(base_platform=WagonFeldbahnA,
                 repeat=5)
