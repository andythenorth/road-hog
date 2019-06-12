from road_vehicle import DumpFeldbahnConsist
from base_platforms.feldbahn import SteamEngineFeldbahn2, OpenWagonFeldbahnGen3

consist = DumpFeldbahnConsist(id='dugout_dump',
                       base_numeric_id=1010,
                       name='Dugout',
                       gen=2)

consist.add_unit(base_platform=SteamEngineFeldbahn2)

consist.add_unit(base_platform=OpenWagonFeldbahnGen3,
                 repeat=3)
