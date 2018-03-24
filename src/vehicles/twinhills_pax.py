from road_vehicle import PaxHauler, ElectricRoadVehicle

consist = PaxHauler(id='twinhills_pax',
                    base_numeric_id=70,
                    name='Twinhills',
                    tram_type='ELRL',
                    vehicle_life=40,
                    intro_date=1990)

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=70,
                 vehicle_length=8,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 repeat=2)
