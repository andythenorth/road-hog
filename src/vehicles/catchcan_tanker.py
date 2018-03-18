from road_vehicle import Tanker

consist = Tanker(id='catchcan',
                 base_numeric_id=810,
                 title='Catchcan [Tanker Tram]',
                 tram_type='ELRL',
                 vehicle_life=40,
                 intro_date=1902)

consist.add_unit(capacity=30,
                 vehicle_length=8,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 repeat=2)
