from road_vehicle import Tanker, ElectricRoadVehicle

consist = Tanker(id='catchcan_tanker',
                 base_numeric_id=810,
                 name='Catchcan',
                 tram_type='ELRL',
                 vehicle_life=40,
                 intro_date=1902)

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=30,
                 vehicle_length=8,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 repeat=2)
