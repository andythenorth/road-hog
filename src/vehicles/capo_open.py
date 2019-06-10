from road_vehicle import OpenTruckConsist
from base_platforms.trucks import DieselCaboverRigidTruckGen5A

consist = OpenTruckConsist(id='capo_open',
                    base_numeric_id=680,
                    name='Capo',
                    gen=5)

consist.add_unit(base_platform=DieselCaboverRigidTruckGen5A)

consist.add_unit(base_platform=None,
                 vehicle_length=4,
                 cargo_length=3)
