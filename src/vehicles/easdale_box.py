from road_vehicle import BoxFeldbahnConsist
from base_platforms.feldbahn import SteamEngineFeldbahnGen1A, WagonFeldbahnA

consist = BoxFeldbahnConsist(id='easdale_box',
                       base_numeric_id=620,
                       name='Easdale',
                       gen=1)

consist.add_unit(base_platform=SteamEngineFeldbahnGen1A)

consist.add_unit(base_platform=WagonFeldbahnA,
                 repeat=5)
