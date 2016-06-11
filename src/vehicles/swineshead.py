import global_constants
from road_vehicle import RVConsist, LivestockHauler

consist = RVConsist(id = 'swineshead',
              base_numeric_id = 440,
              title = 'Swineshead [Livestock Truck]',
              replacement_id = '-none',
              vehicle_life = 40,
              intro_date = 1970)

consist.add_unit(LivestockHauler(consist = consist,
                        weight = 10,
                        capacity = 25,
                        vehicle_length = 6,
                        visual_effect = 'VISUAL_EFFECT_DIESEL',
                        spriterow_num = 0))

consist.add_unit(LivestockHauler(consist = consist,
                        weight = 10,
                        capacity = 15,
                        vehicle_length = 4,
                        spriterow_num = 1))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
