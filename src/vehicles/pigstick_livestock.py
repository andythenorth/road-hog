from road_vehicle import LivestockTruckConsist, DieselVehicleUnit

consist = LivestockTruckConsist(id='pigstick_livestock',
                         base_numeric_id=330,
                         name='Pigstick',
                           gen=3,
                         intro_date_offset=2)  # introduce later than gen epoch by design

consist.add_unit(type=DieselVehicleUnit,
                 vehicle_length=6)

consist.add_unit(base_platform=None,
                 vehicle_length=4)
