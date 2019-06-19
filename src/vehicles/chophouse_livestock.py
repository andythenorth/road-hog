from road_vehicle import LivestockFeldbahnConsist
from base_platforms.feldbahn import SteamEngineFeldbahnGen2B, WagonFeldbahnA

consist = LivestockFeldbahnConsist(id='chophouse_livestock',
                       base_numeric_id=1190,
                       name='Chophouse',
                       gen=2)

consist.add_unit(base_platform=SteamEngineFeldbahnGen2B)

consist.add_unit(base_platform=WagonFeldbahnA,
                 repeat=12)
