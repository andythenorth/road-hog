from road_vehicle import OpenFeldbahnConsist
from base_platforms.feldbahn import SteamEngineFeldbahn1, OpenWagonFeldbahnGen1

consist = OpenFeldbahnConsist(id='intake_open',
                       base_numeric_id=730,
                       name='Intake',
                       gen=1)

consist.add_unit(base_platform=SteamEngineFeldbahn1)


consist.add_unit(base_platform=OpenWagonFeldbahnGen1,
                 repeat=3)
