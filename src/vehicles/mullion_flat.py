from road_vehicle import FlatFeldbahnConsist
from base_platforms.feldbahn import SteamEngineFeldbahnGen1A, WagonFeldbahnA

consist = FlatFeldbahnConsist(id='mullion_flat',
                       base_numeric_id=1040,
                       name='Mullion',
                       gen=1)

consist.add_unit(base_platform=SteamEngineFeldbahnGen1A)

consist.add_unit(base_platform=WagonFeldbahnA,
                 repeat=5)
