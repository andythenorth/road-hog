from road_vehicle import OpenFeldbahnConsist, SteamRoadVehicle
from base_platforms.feldbahn import SteamEngineFeldbahn1, OpenWagonFeldbahnGen2

consist = OpenFeldbahnConsist(id='bahn_steam_face_open',
                       base_numeric_id=970,
                       name='Bahn Steam Face',
                       vehicle_life=40,
                       gen=2)

consist.add_unit(base_platform=SteamEngineFeldbahn1)

consist.add_unit(base_platform=OpenWagonFeldbahnGen2,
                 repeat=3)
