import global_constants
from road_vehicle import Tanker

consist = Tanker(id = 'meriden',
                base_numeric_id = 290,
                title = 'Meriden [Tanker Truck]',
                replacement_id = '-none',
                semi_truck_so_redistribute_capacity = True,
                vehicle_life = 40,
                intro_date = 1974)

consist.add_unit(weight = 7,
                capacity = 0,
                vehicle_length = 2,
                semi_truck_shift_offset_jank = 2,
                effects = ['EFFECT_SPRITE_DIESEL, -3, 1, 10'],
                always_use_same_spriterow = True)

consist.add_unit(weight = 8,
                capacity = 40,
                vehicle_length = 7)

consist.add_model_variant(intro_date=0,
                          end_date=global_constants.max_game_date,
                          spritesheet_suffix=0,
                          graphics_processor=consist.graphics_processors[0])
