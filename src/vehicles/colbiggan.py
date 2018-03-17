from road_vehicle import BoxHauler

consist = BoxHauler(id='colbiggan',
                    base_numeric_id=880,
                    title='Colbiggan [Box Tram]',
                    tram_type='ELRL',
                    vehicle_life=40,
                    intro_date=1940)

consist.add_unit(capacity=36,
                 vehicle_length=8,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 repeat=2)

consist.add_model_variant(spritesheet_suffix=0)
