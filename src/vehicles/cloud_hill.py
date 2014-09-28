import global_constants
from road_vehicle import EngineConsist, Tanker

consist = EngineConsist(id = 'cloud_hill',
              base_numeric_id = 410,
              title = 'Cloud Hill [Tanker Truck]',
              replacement_id = '-none',
              power = 550,
              vehicle_life = 40,
              intro_date = 1993)

consist.add_unit(Tanker(consist = consist,
                        weight = 8,
                        capacity = 0,
                        vehicle_length = 7,
                        visual_effect = 'VISUAL_EFFECT_DIESEL',
                        spriterow_num = 0))

consist.add_unit(Tanker(consist = consist,
                        weight = 10,
                        capacity = 45,
                        vehicle_length = 7,
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
