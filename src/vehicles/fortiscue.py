import global_constants
from road_vehicle import EngineConsist, RefrigeratedHauler

consist = EngineConsist(id = 'fortiscue',
              base_numeric_id = 180,
              title = 'Fortiscue [Reefer Truck]',
              replacement_id = '-none',
              power = 450,
              vehicle_life = 40,
              intro_date = 1970)

consist.add_unit(RefrigeratedHauler(consist = consist,
                        weight = 17,
                        capacity = 20,
                        vehicle_length = 7,
                        visual_effect = 'VISUAL_EFFECT_DIESEL',
                        spriterow_num = 0))

consist.add_unit(RefrigeratedHauler(consist = consist,
                        weight = 10,
                        capacity = 20,
                        vehicle_length = 4,
                        spriterow_num = 1))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
