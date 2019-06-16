from road_vehicle import DumpFeldbahnConsist
from base_platforms.feldbahn import SteamEngineFeldbahn1, OpenWagonFeldbahnGen2

consist = DumpFeldbahnConsist(id='dugout_dump',
                       base_numeric_id=1010,
                       name='Dugout',
                       gen=2)

consist.add_unit(base_platform=SteamEngineFeldbahn1)

consist.add_unit(base_platform=OpenWagonFeldbahnGen2,
                 repeat=5)
