from road_vehicle import PaxHauler

consist = PaxHauler(id='newbold',
                    base_numeric_id=30,
                    title='Newbold [Passenger Tram]',
                    tram_type='ELRL',
                    vehicle_life=40,
                    intro_date=1932)

consist.add_unit(capacity=50,
                 vehicle_length=8,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 12'],
                 repeat=2)

consist.add_model_variant(spritesheet_suffix=0)
