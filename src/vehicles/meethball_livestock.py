from road_vehicle import LivestockFeldbahnConsist
from base_platforms.feldbahn import SteamEngineFeldbahnGen2A, WagonFeldbahnA

consist = LivestockFeldbahnConsist(id='meethball_livestock',
                       base_numeric_id=1220,
                       name='Meethball',
                       gen=2)

consist.add_unit(base_platform=SteamEngineFeldbahnGen2A)

consist.add_unit(base_platform=WagonFeldbahnA,
                 repeat=5)
