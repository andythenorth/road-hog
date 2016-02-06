import global_constants
from road_vehicle import RVConsist, RefrigeratedHauler

consist = RVConsist(id = 'fortiscue',
              base_numeric_id = 180,
              title = 'Fortiscue [Reefer Truck]',
              replacement_id = '-none',
              power = 450,
              semi_truck = True,
              vehicle_life = 40,
              intro_date = 1978)

consist.add_unit(RefrigeratedHauler(consist = consist,
                        weight = 17,
                        capacity = 0,
                        vehicle_length = 2,
                        semi_truck_shift_offset_jank = 2,
                        effects = ['EFFECT_SPRITE_DIESEL, -2, 1, 10'],
                        spriterow_num = 0))

consist.add_unit(RefrigeratedHauler(consist = consist,
                        weight = 10,
                        capacity = 40,
                        vehicle_length = 6,
                        spriterow_num = 1))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
