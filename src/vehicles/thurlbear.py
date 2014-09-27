import global_constants
from road_vehicle import EngineConsist, BulkPowderHauler

consist = EngineConsist(id = 'thurlbear',
              base_numeric_id = 980,
              title = 'Thurlbear [Covered Hopper Tram]',
              roadveh_flag_tram = True,
              replacement_id = '-none',
              power = 250,
              vehicle_life = 40,
              intro_date = 1958)

consist.add_unit(BulkPowderHauler(consist = consist,
                        weight = 7,
                        capacity_freight = 0,
                        vehicle_length = 7,
                        visual_effect = 'VISUAL_EFFECT_DIESEL',
                        spriterow_num = 0))

consist.add_unit(BulkPowderHauler(consist = consist,
                        weight = 8,
                        capacity_freight = 40,
                        vehicle_length = 7,
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
