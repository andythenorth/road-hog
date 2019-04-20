from road_vehicle import RefrigeratedHauler, ElectricRoadVehicle

consist = RefrigeratedHauler(id='winterfold_refrigerated',
                             base_numeric_id=770,
                             name='Winterfold',
                             tram_type='ELRL',
                             vehicle_life=40,
                             gen=2,
                             intro_date_offset=10)  # introduce later than gen epoch by design

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=30,
                 vehicle_length=8,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 repeat=2)
