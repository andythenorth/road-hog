from road_vehicle import PaxHauler, ElectricRoadVehicle

consist = PaxHauler(id='northbeach_pax',
                    base_numeric_id=690,
                    name='Northbeach',
                    tram_type='ELRL',
                    vehicle_life=40,
                    intro_date=1961)

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=60,
                 vehicle_length=8,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 12'],
                 repeat=2)
