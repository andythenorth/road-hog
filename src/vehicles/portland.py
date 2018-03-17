from road_vehicle import OpenHauler

consist = OpenHauler(id='portland',
                     base_numeric_id=860,
                     title='Portland [Open Tram]',
                     tram_type='ELRL',
                     vehicle_life=40,
                     intro_date=1900,)

consist.add_unit(capacity=30,
                 vehicle_length=8,
                 cargo_length=3,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 repeat=2)

consist.add_model_variant(spritesheet_suffix=0)