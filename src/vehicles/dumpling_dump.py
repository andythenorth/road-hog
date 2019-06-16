from road_vehicle import DumpFeldbahnConsist
from base_platforms.feldbahn import SteamEngineFeldbahn1, OpenWagonFeldbahnGen1

consist = DumpFeldbahnConsist(id='dumpling_dump',
                       base_numeric_id=980,
                       name='Dumpling',
                       gen=1)

consist.add_unit(base_platform=SteamEngineFeldbahn1)

consist.add_unit(base_platform=OpenWagonFeldbahnGen1,
                 repeat=5)