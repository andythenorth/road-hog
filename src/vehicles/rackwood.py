from road_vehicle import FlatHauler

consist = FlatHauler(id='rackwood',
                        base_numeric_id=740,
                        title='Rackwood [Flatbed Tram]',
                        tram_type='ELRL',
                        vehicle_life=40,
                        intro_date=1900)

consist.add_unit(capacity=30,
                 vehicle_length=8,
                 cargo_length=3,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 repeat=2)
