from road_vehicle import FlatHauler, ElectricRoadVehicle

consist = FlatHauler(id='stancliffe_flat',
                        base_numeric_id=410,
                        name='Stancliffe',
                        tram_type='ELRL',
                        vehicle_life=40,
                     gen=4,
                     intro_date=1940)

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=36,
                 vehicle_length=8,
                 cargo_length=3,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 repeat=2)
