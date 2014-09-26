import global_constants
from road_vehicle import EngineConsist, LogHauler

consist = EngineConsist(id = 'knockdown',
              base_numeric_id = 430,
              title = 'Knockdown [Logging Truck]',
              replacement_id = '-none',
              power = 250,
              vehicle_life = 40,
              intro_date = 1962)

consist.add_unit(LogHauler(consist = consist,
                        weight = 12,
                        capacity_freight = 20,
                        vehicle_length = 7,
                        visual_effect = 'VISUAL_EFFECT_DIESEL',
                        spriterow_num = 0))

consist.add_unit(LogHauler(consist = consist,
                        weight = 7,
                        capacity_freight = 25,
                        vehicle_length = 7,
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
