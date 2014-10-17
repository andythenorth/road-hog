import global_constants
from road_vehicle import EngineConsist, FoundryHauler

consist = EngineConsist(id = 'stancliffe',
              base_numeric_id = 350,
              title = 'Stancliffe [Foundry Tram]',
              roadveh_flag_tram = True,
              replacement_id = '-none',
              power = 250,
              vehicle_life = 40,
              intro_date = 1900)

consist.add_unit(FoundryHauler(consist = consist,
                        weight = 20,
                        capacity = 2,
                        vehicle_length = 3,
                        effects = ['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                        spriterow_num = 0))

consist.add_unit(FoundryHauler(consist = consist,
                        weight = 5,
                        capacity = 12,
                        vehicle_length = 4,
                        spriterow_num = 1), repeat = 4)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
