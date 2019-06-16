from road_vehicle import OpenFeldbahnConsist
from base_platforms.feldbahn import SteamEngineFeldbahnGen2B, WagonFeldbahnA

consist = OpenFeldbahnConsist(id='imperial_open',
                       base_numeric_id=1090,
                       name='Imperial',
                       gen=2)

consist.add_unit(base_platform=SteamEngineFeldbahnGen2B)


consist.add_unit(base_platform=WagonFeldbahnA,
                 repeat=12)
