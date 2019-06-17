from road_vehicle import TankerFeldbahnConsist
from base_platforms.feldbahn import SteamEngineFeldbahnGen1A, WagonFeldbahnA

consist = TankerFeldbahnConsist(id='tankard_tanker',
                       base_numeric_id=1160,
                       name='Tankard',
                       gen=1)

consist.add_unit(base_platform=SteamEngineFeldbahnGen1A)

consist.add_unit(base_platform=WagonFeldbahnA,
                 repeat=5)
