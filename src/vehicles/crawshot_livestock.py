from road_vehicle import LivestockFeldbahnConsist
from base_platforms.feldbahn import SteamEngineFeldbahnGen1A, WagonFeldbahnA

consist = LivestockFeldbahnConsist(id='crawshot_livestock',
                       base_numeric_id=1200,
                       name='Crawshot',
                       gen=1)

consist.add_unit(base_platform=SteamEngineFeldbahnGen1A)

consist.add_unit(base_platform=WagonFeldbahnA,
                 repeat=5)
