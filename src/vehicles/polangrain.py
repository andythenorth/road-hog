from road_vehicle import CoveredHopperHauler

consist = CoveredHopperHauler(id='polangrain',
                              base_numeric_id=790,
                              title='Polangrain [Covered Hopper Tram]',
                              tram_type='ELRL',
                              vehicle_life=40,
                              intro_date=1900)

consist.add_unit(capacity=30,
                 vehicle_length=8,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 repeat=2)

