from road_vehicle import OpenFeldbahnConsist
from base_platforms.feldbahn import SteamEngineFeldbahnGen1A, WagonFeldbahnA

consist = OpenFeldbahnConsist(id='intake_open',
                       base_numeric_id=730,
                       name='Intake',
                       gen=1)

consist.add_unit(base_platform=SteamEngineFeldbahnGen1A)


consist.add_unit(base_platform=WagonFeldbahnA,
                 repeat=5)
