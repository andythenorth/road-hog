import global_constants
from road_vehicle import EngineConsist, DumpHauler

consist = EngineConsist(id = 'scrooby_top',
              base_numeric_id = 700,
              title = 'Scrooby Top [Dump Tram]',
              roadveh_flag_tram = True,
              replacement_id = '-none',
              power = 100,
              vehicle_life = 40,
              intro_date = 1870)

consist.add_unit(DumpHauler(consist = consist,
                        weight = 30,
                        capacity = 0,
                        vehicle_length = 6,
                        effect_spawn_model = 'EFFECT_SPAWN_MODEL_STEAM',
                        effects = ['EFFECT_SPRITE_STEAM, -3, 0, 12', 'EFFECT_SPRITE_STEAM, 1, 0, 12'],
                        spriterow_num = 0))

consist.add_unit(DumpHauler(consist = consist,
                        weight = 2,
                        capacity = 12,
                        vehicle_length = 3,
                        spriterow_num = 1), repeat=4)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
