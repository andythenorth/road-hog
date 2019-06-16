from road_vehicle import BoxFeldbahnConsist
from base_platforms.feldbahn import SteamEngineFeldbahnGen2A, WagonFeldbahnA

consist = BoxFeldbahnConsist(id='ingleby_box',
                       base_numeric_id=1000,
                       name='Ingleby',
                       gen=2)

consist.add_unit(base_platform=SteamEngineFeldbahnGen2A)

consist.add_unit(base_platform=WagonFeldbahnA,
                 repeat=5)
