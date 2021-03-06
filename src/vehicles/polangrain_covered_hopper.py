from road_vehicle import CoveredHopperHauler, ElectricRoadVehicle

consist = CoveredHopperHauler(id='polangrain_covered_hopper',
                              base_numeric_id=790,
                              name='Polangrain',
                              tram_type='ELRL',
                              vehicle_life=40,
                              intro_date=1900)

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=30,
                 vehicle_length=8,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 repeat=2)
