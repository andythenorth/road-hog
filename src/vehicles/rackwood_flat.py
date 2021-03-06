from road_vehicle import FlatHauler, ElectricRoadVehicle

consist = FlatHauler(id='rackwood_flat',
                        base_numeric_id=740,
                        name='Rackwood',
                        tram_type='ELRL',
                        vehicle_life=40,
                        intro_date=1900)

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=30,
                 vehicle_length=8,
                 cargo_length=3,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 repeat=2)
