import global_constants
from road_vehicle import RVConsist, RefrigeratedHauler

consist = RVConsist(id = 'coldfall',
              base_numeric_id = 150,
              title = 'Coldfall [Reefer Truck]',
              replacement_id = '-none',
              semi_truck = True,
              vehicle_life = 40,
              intro_date = 2007)

consist.add_unit(RefrigeratedHauler(consist = consist,
                        weight = 17,
                        capacity = 20,
                        vehicle_length = 2,
                        semi_truck_shift_offset_jank = 3,
                        effects = ['EFFECT_SPRITE_DIESEL, -2, 1, 10'],
                        spriterow_num = 0))

consist.add_unit(RefrigeratedHauler(consist = consist,
                        weight = 10,
                        capacity = 20,
                        vehicle_length = 6,
                        spriterow_num = 1))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
