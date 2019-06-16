from road_vehicle import FlatFeldbahnConsist
from base_platforms.feldbahn import SteamEngineFeldbahnGen2A, WagonFeldbahnA

consist = FlatFeldbahnConsist(id='stawell_flat',
                       base_numeric_id=1050,
                       name='Stawell',
                       gen=2)

consist.add_unit(base_platform=SteamEngineFeldbahnGen2A)

consist.add_unit(base_platform=WagonFeldbahnA,
                 repeat=5)
