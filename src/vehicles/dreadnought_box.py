from road_vehicle import BoxFeldbahnConsist
from base_platforms.feldbahn import SteamEngineFeldbahnGen2B, WagonFeldbahnA

consist = BoxFeldbahnConsist(id='dreadnought_box',
                       base_numeric_id=1100,
                       name='Dreadnought',
                       gen=2)

consist.add_unit(base_platform=SteamEngineFeldbahnGen2B)

consist.add_unit(base_platform=WagonFeldbahnA,
                 repeat=12)
