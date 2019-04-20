from road_vehicle import BoxHauler, ElectricRoadVehicle

consist = BoxHauler(id='rakeway_box',
                    base_numeric_id=870,
                    name='Rakeway',
                    tram_type='ELRL',
                    vehicle_life=40,
                    gen=2)

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=30,
                 vehicle_length=8,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 repeat=2)
