import global_constants
from road_vehicle import EngineConsist, PaxHauler

consist = EngineConsist(id = 'newbold',
              base_numeric_id = 30,
              title = 'Newbold [Passenger Tram]',
              roadveh_flag_tram = True,
              replacement_id = '-none',
              power = 160,
              vehicle_life = 40,
              intro_date = 1932)

consist.add_unit(PaxHauler(consist = consist,
                        weight = 20,
                        capacity = 80,
                        vehicle_length = 7,
                        effects = ['EFFECT_SPRITE_ELECTRIC, 0, 0, 12'],
                        spriterow_num = 0), repeat=2)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
