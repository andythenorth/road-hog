import global_constants
from road_vehicle import EngineConsist, BulkPowderHauler

consist = EngineConsist(id = 'thurlbear',
              base_numeric_id = 460,
              title = 'Thurlbear [Covered Hopper Tram]',
              roadveh_flag_tram = True,
              replacement_id = '-none',
              power = 200,
              vehicle_life = 40,
              intro_date = 1903)

consist.add_unit(BulkPowderHauler(consist = consist,
                        weight = 12,
                        capacity = 30,
                        vehicle_length = 7,
                        effects = ['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
