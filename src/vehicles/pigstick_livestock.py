from road_vehicle import LivestockHauler, DieselRoadVehicle

consist = LivestockHauler(id='pigstick_livestock',
                          base_numeric_id=330,
                          name='Pigstick',
                          vehicle_life=40,
                          intro_date=1941)

consist.add_unit(type=DieselRoadVehicle,
                 capacity=20,
                 vehicle_length=6)

consist.add_unit(capacity=10,
                 vehicle_length=4)
