import global_constants
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

consist.add_model_variant(intro_date=0,
                          end_date=global_constants.max_game_date,
                          spritesheet_suffix=0,
                          graphics_processor=consist.graphics_processors[0])
