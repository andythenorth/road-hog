import global_constants
from road_vehicle import RVConsist, OpenHauler

consist = RVConsist(id = 'yeoman',
              base_numeric_id = 170,
              title = 'Yeoman [Open Truck]',
              replacement_id = '-none',
              semi_truck = True,
              vehicle_life = 40,
              intro_date = 1968)

consist.add_unit(OpenHauler(consist = consist,
                        weight = 7,
                        vehicle_length = 2,
                        semi_truck_shift_offset_jank = 2,
                        visual_effect = 'VISUAL_EFFECT_DIESEL',
                        spriterow_num = 0))

consist.add_unit(OpenHauler(consist = consist,
                        weight = 5,
                        capacity = 40,
                        vehicle_length = 6,
                        spriterow_num = 1))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
