from road_vehicle import FlatFeldbahnConsist
from base_platforms.feldbahn import SteamEngineFeldbahnGen2B, WagonFeldbahnA

consist = FlatFeldbahnConsist(id='newbiggin_flat',
                       base_numeric_id=1110,
                       name='Newbiggin',
                       gen=2)

consist.add_unit(base_platform=SteamEngineFeldbahnGen2B)

consist.add_unit(base_platform=WagonFeldbahnA,
                 repeat=12)
