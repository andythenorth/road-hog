import global_constants
from road_vehicle import RVConsist, BulkPowderHauler

consist = RVConsist(id = 'mcdowell',
              base_numeric_id = 280,
              title = 'McDowell [Covered Hopper Truck]',
              replacement_id = '-none',
              semi_truck = True,
              vehicle_life = 40,
              intro_date = 2007)

consist.add_unit(BulkPowderHauler(consist = consist,
                        weight = 8,
                        capacity = 0,
                        vehicle_length = 2,
                        semi_truck_shift_offset_jank = 2,
                        effects = ['EFFECT_SPRITE_DIESEL, -2, 1, 10'],
                        spriterow_num = 0))

consist.add_unit(BulkPowderHauler(consist = consist,
                        weight = 8,
                        capacity = 40,
                        vehicle_length = 8,
                        spriterow_num = 1))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
