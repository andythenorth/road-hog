from road_vehicle import LivestockTruckConsist, DieselRoadVehicle

consist = LivestockTruckConsist(id='pigstick_livestock',
                         base_numeric_id=330,
                         name='Pigstick',
                         vehicle_life=40,
                         gen=3,
                         intro_date_offset=2)  # introduce later than gen epoch by design

consist.add_unit(type=DieselRoadVehicle,
                 capacity=20,
                 vehicle_length=6)

consist.add_unit(capacity=10,
                 vehicle_length=4)
