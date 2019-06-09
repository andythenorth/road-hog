from road_vehicle import LivestockTruckConsist, DieselVehicleUnit

consist = LivestockTruckConsist(id='swineshead_livestock',
                         base_numeric_id=440,
                         name='Swineshead',
                           gen=4,
                         intro_date_offset=2)  # introduce later than gen epoch by design

consist.add_unit(type=DieselVehicleUnit,
                 vehicle_length=6)

consist.add_unit(vehicle_length=4)
