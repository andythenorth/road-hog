from road_vehicle import CoveredHopperHauler

consist = CoveredHopperHauler(id='thurlbear',
                              base_numeric_id=460,
                              title='Thurlbear [Covered Hopper Tram]',
                              tram_type='ELRL',
                              vehicle_life=40,
                              intro_date=1940)

consist.add_unit(capacity=36,
                 vehicle_length=8,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 repeat=2)

