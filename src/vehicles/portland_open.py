from road_vehicle import OpenTram, ElectricRoadVehicle

consist = OpenTram(id='portland_open',
                   base_numeric_id=860,
                   name='Portland',
                   tram_type='ELRL',
                   vehicle_life=40,
                   gen=2)

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=30,
                 vehicle_length=8,
                 cargo_length=3,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 repeat=2)
