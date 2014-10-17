import global_constants
from road_vehicle import EngineConsist, FoundryHauler

consist = EngineConsist(id = 'steeraway',
              base_numeric_id = 420,
              title = 'Steeraway [Foundry Hauler]',
              replacement_id = '-none',
              power = 500,
              speed = 37,
              vehicle_life = 40,
              intro_date = 1985)

consist.add_unit(FoundryHauler(consist = consist,
                        weight = 35,
                        capacity = 100,
                        vehicle_length = 7,
                        visual_effect = 'VISUAL_EFFECT_DIESEL',
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
