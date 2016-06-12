import global_constants
import graphics_processor.utils as graphics_utils
from road_vehicle import RVConsist, DumpHauler

consist = RVConsist(vehicle_type = DumpHauler,
                id = 'coleman',
                base_numeric_id = 910,
                title = 'Coleman [Dump Truck]',
                replacement_id = '-none',
                power = 130,
                semi_truck_so_redistribute_capacity = True,
                vehicle_life = 40,
                intro_date = 1920)

consist.add_unit(weight = 6,
                capacity = 0,
                vehicle_length = 2,
                semi_truck_shift_offset_jank = 2,
                effect_spawn_model = 'EFFECT_SPAWN_MODEL_STEAM',
                effects = ['EFFECT_SPRITE_STEAM, -3, 0, 12'],
                always_use_same_spriterow = True,
                spriterow_num = 0)

consist.add_unit(weight = 6,
                capacity = 24,
                vehicle_length = 5,
                spriterow_adjust = {'multiplier': 0, 'offset': 1})

graphics_processors = consist.get_graphics_processors(template='coleman_template.png',
                                                      copy_block_top_offsets = [40],
                                                      paste_top_offset = 40)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0,
                       graphics_processor=graphics_processors[0])
