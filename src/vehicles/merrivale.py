import global_constants
from road_vehicle import RVConsist, RefrigeratedHauler

consist = RVConsist(id = 'merrivale',
              base_numeric_id = 300,
              title = 'Merrivale [Reefer Truck]',
              replacement_id = '-none',
              power = 250,
              vehicle_life = 40,
              intro_date = 1949)

consist.add_unit(RefrigeratedHauler(consist = consist,
                        weight = 15,
                        capacity = 15,
                        vehicle_length = 6,
                        visual_effect = 'VISUAL_EFFECT_DIESEL',
                        spriterow_num = 0))

consist.add_unit(RefrigeratedHauler(consist = consist,
                        weight = 8,
                        capacity = 15,
                        vehicle_length = 4,
                        spriterow_num = 1))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
