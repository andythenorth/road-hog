import global_constants
from road_vehicle import EngineConsist, Tanker

consist = EngineConsist(id = 'oylbarral',
              base_numeric_id = 320,
              title = 'Oylbarral [Tanker Tram]',
              roadveh_flag_tram = True,
              replacement_id = '-none',
              power = 200,
              vehicle_life = 40,
              intro_date = 1905)

consist.add_unit(Tanker(consist = consist,
                        weight = 10,
                        capacity = 15,
                        vehicle_length = 6,
                        effects = ['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                        spriterow_num = 0))

consist.add_unit(Tanker(consist = consist,
                        weight = 5,
                        capacity = 15,
                        vehicle_length = 5,
                        spriterow_num = 1), repeat=1)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
