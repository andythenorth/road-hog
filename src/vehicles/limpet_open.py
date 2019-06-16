from road_vehicle import OpenFeldbahnConsist
from base_platforms.feldbahn import SteamEngineFeldbahn1, OpenWagonFeldbahnGen2

consist = OpenFeldbahnConsist(id='limpet_open',
                       base_numeric_id=220,
                       name='Limpet',
                       gen=2)

consist.add_unit(base_platform=SteamEngineFeldbahn1)


consist.add_unit(base_platform=OpenWagonFeldbahnGen2,
                 repeat=5)