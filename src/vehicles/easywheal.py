import global_constants
from road_vehicle import RVConsist, BoxHauler

consist = RVConsist(id = 'easywheal',
              base_numeric_id = 160,
              title = 'Easywheal [Box Truck]',
              replacement_id = '-none',
              vehicle_life = 40,
              intro_date = 1939)

consist.add_unit(BoxHauler(consist = consist,
                        weight = 12,
                        capacity = 15,
                        vehicle_length = 6,
                        visual_effect = 'VISUAL_EFFECT_DIESEL',
                        spriterow_num = 0))

consist.add_unit(BoxHauler(consist = consist,
                        weight = 5,
                        capacity = 15,
                        vehicle_length = 4,
                        spriterow_num = 1))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
