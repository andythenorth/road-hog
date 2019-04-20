from road_vehicle import MetalHauler, DieselRoadVehicle

consist = MetalHauler(id='steeraway_metal',
                      base_numeric_id=520,
                      name='Steeraway',
                      road_type='HAUL',
                      power=500,
                      speed=45,
                      vehicle_life=80,
                      gen=4,
                      intro_date=1960)

consist.add_unit(type=DieselRoadVehicle,
                 capacity=0,
                 vehicle_length=6)

consist.add_unit(capacity=50,
                 vehicle_length=7,
                 repeat=2)
