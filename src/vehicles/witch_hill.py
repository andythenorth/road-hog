import global_constants
import graphics_processor.utils as graphics_utils
from road_vehicle import RVConsist, DumpHauler

graphics_processors = graphics_utils.get_composited_cargo_processors(template='witch_hill_template.png',
                                              copy_block_top_offsets = [10],
                                              paste_top_offset = 40)

consist = RVConsist(vehicle_type = DumpHauler,
                id = 'witch_hill',
                base_numeric_id = 500,
                title = 'Witch Hill [Mining Truck]',
                replacement_id = '-none',
                power = 900,
                speed = 50, # dibbled up above RL for game balance
                type_base_running_cost_points = 30, # dibble running costs for game balance
                vehicle_life = 40,
                intro_date = 2007)

consist.add_unit(weight = 60,
                capacity = 85, # much bigger is not much better here
                vehicle_length = 7,
                effects = ['EFFECT_SPRITE_AIRCRAFT_BREAKDOWN_SMOKE, -2, 1, 10', 'EFFECT_SPRITE_AIRCRAFT_BREAKDOWN_SMOKE, -2, -1, 10'],
                spriterow_num = 0)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0,
                       graphics_processor=graphics_processors[0])

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=1,
                       graphics_processor=graphics_processors[1])
