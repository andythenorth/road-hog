import global_constants
from road_vehicle import EngineConsist, Tanker

consist = EngineConsist(id = 'drumbreck',
              base_numeric_id = 800,
              title = 'Drumbreck [Tanker Tram]',
              roadveh_flag_tram = True,
              replacement_id = '-none',
              power = 100,
              vehicle_life = 40,
              intro_date = 1870)

consist.add_unit(Tanker(consist = consist,
                        weight = 10,
                        capacity = 16,
                        vehicle_length = 6,
                        effects = ['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                        spriterow_num = 0))

consist.add_unit(Tanker(consist = consist,
                        weight = 5,
                        capacity = 16,
                        vehicle_length = 4,
                        spriterow_num = 1))

consist.add_unit(Tanker(consist = consist,
                        weight = 10,
                        capacity = 16,
                        vehicle_length = 6,
                        effects = ['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                        spriterow_num = 2))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)