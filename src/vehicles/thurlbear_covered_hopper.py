from road_vehicle import CoveredHopperHauler, ElectricRoadVehicle

consist = CoveredHopperHauler(id='thurlbear_covered_hopper',
                              base_numeric_id=460,
                              name='Thurlbear',
                              tram_type='ELRL',
                              vehicle_life=40,
                              gen=4,
                              intro_date=1940)

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=36,
                 vehicle_length=8,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 repeat=2)
