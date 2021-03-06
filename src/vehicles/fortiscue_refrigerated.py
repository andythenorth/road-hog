from road_vehicle import RefrigeratedHauler, DieselRoadVehicle

consist = RefrigeratedHauler(id='fortiscue_refrigerated',
                             base_numeric_id=180,
                             name='Fortiscue',
                             vehicle_life=40,
                             intro_date=1972)

consist.add_unit(type=DieselRoadVehicle,
                 capacity=25,
                 vehicle_length=6)

consist.add_unit(capacity=15,
                 vehicle_length=4)
