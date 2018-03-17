import global_constants
from road_vehicle import DumpHauler

consist = DumpHauler(id='scrooby_top',
                     base_numeric_id=700,
                     title='Scrooby Top [Dump Tram]',
                     tram_type='RAIL',
                     vehicle_life=40,
                     intro_date=1870)

consist.add_unit(capacity=0,
                 vehicle_length=4,
                 effect_spawn_model='EFFECT_SPAWN_MODEL_STEAM',
                 effects=['EFFECT_SPRITE_STEAM, -3, 0, 12',
                          'EFFECT_SPRITE_STEAM, 1, 0, 12'],
                 always_use_same_spriterow=True)

consist.add_unit(capacity=12,
                 vehicle_length=3,
                 repeat=4)

consist.add_model_variant(spritesheet_suffix=0)