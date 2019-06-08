from road_vehicle import LivestockTruckConsist, DieselVehicleUnit

consist = LivestockTruckConsist(id='swineshead_livestock',
                         base_numeric_id=440,
                         name='Swineshead',
                         vehicle_life=40,
                         gen=4,
                         intro_date_offset=2)  # introduce later than gen epoch by design

consist.add_unit(type=DieselVehicleUnit,
                 capacity=25,
                 vehicle_length=6)

consist.add_unit(capacity=15,
                 vehicle_length=4)
