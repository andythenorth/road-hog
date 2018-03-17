from road_vehicle import OpenHauler

consist = OpenHauler(id='jinglepot',
                     base_numeric_id=240,
                     title='Jinglepot [Open Truck]',
                     vehicle_life=40,
                     intro_date=1910)

consist.add_unit(capacity=12,
                 vehicle_length=5,
                 cargo_length=3,
                 effect_spawn_model='EFFECT_SPAWN_MODEL_STEAM',
                 effects=['EFFECT_SPRITE_STEAM, -3, 0, 12'])

consist.add_unit(capacity=12,
                 vehicle_length=4,
                 cargo_length=4)

consist.add_model_variant(spritesheet_suffix=0)