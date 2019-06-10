from road_vehicle import FlatbedTruckConsist, DieselVehicleUnit
from base_platforms.trucks import DieselCaboverRigidTruckGen3A

consist = FlatbedTruckConsist(id='windergill_flat',
                       base_numeric_id=640,
                       name='Windergill',
                       gen=3)

consist.add_unit(base_platform=DieselCaboverRigidTruckGen3A)

consist.add_unit(base_platform=None,
                 vehicle_length=4,
                 cargo_length=4)
