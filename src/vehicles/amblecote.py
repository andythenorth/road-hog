import global_constants
from road_vehicle import BoxHauler

consist = BoxHauler(id = 'amblecote',
                    base_numeric_id = 80,
                    title = 'Amblecote [Box Tram]',
                    tram_type = 'TRAM',
                    vehicle_life = 40,
                    intro_date = 1860)

consist.add_unit(capacity = 0,
                 vehicle_length = 4,
                 effect_spawn_model = 'EFFECT_SPAWN_MODEL_STEAM',
                 effects = ['EFFECT_SPRITE_STEAM, -2, 0, 14'])

consist.add_unit(capacity = 16,
                 vehicle_length = 4,
                 repeat = 3)

consist.add_model_variant(intro_date=0,
                          end_date=global_constants.max_game_date,
                          spritesheet_suffix=0)
