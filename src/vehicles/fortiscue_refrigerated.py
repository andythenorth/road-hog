from road_vehicle import RefrigeratedTruckConsist, DieselVehicleUnit
from base_platforms.trucks import DieselCaboverRigidTruckGen4B

consist = RefrigeratedTruckConsist(id='fortiscue_refrigerated',
                            base_numeric_id=180,
                            name='Fortiscue',
                              gen=4,
                            intro_date_offset=4)  # introduce later than gen epoch by design

consist.add_unit(base_platform=DieselCaboverRigidTruckGen4B)

consist.add_unit(base_platform=None,
                 vehicle_length=4)
