from road_vehicle import OpenTruckConsist
from base_platforms.trucks import SteamCaboverRigidTruckGen2A

consist = OpenTruckConsist(id='jinglepot_open',
                    base_numeric_id=240,
                    name='Jinglepot',
                    gen=2)

consist.add_unit(base_platform=SteamCaboverRigidTruckGen2A)

consist.add_unit(base_platform=None,
                 vehicle_length=4,
                 cargo_length=4)
