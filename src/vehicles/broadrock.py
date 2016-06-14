import global_constants
from road_vehicle import RVConsist, DumpHauler

consist = RVConsist(vehicle_type = DumpHauler,
                id = 'broadrock',
                base_numeric_id = 100,
                title = 'Broadrock [Mining Truck]',
                replacement_id = '-none',
                power = 400,
                semi_truck_so_redistribute_capacity = True,
                speed = 40, # dibbled up above RL for game balance
                type_base_running_cost_points = 20, # dibble running costs for game balance
                vehicle_life = 40,
                intro_date = 1947)

consist.add_unit(weight = 35,
                capacity = 0,
                vehicle_length = 2,
                semi_truck_shift_offset_jank = 3,
                effects = ['EFFECT_SPRITE_AIRCRAFT_BREAKDOWN_SMOKE, -2, 1, 10', 'EFFECT_SPRITE_AIRCRAFT_BREAKDOWN_SMOKE, -2, -1, 10'],
                always_use_same_spriterow = True)

consist.add_unit(weight = 0, # put the weight on the truck to compensate for lack of TE when loaded
                capacity = 55, # much bigger is not much better here
                vehicle_length = 6)

graphics_processors = consist.get_graphics_processors(template='broadrock_template.png',
                                                      copy_block_top_offsets = [40],
                                                      paste_top_offset = 40)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0,
                       graphics_processor=graphics_processors[0])

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=1,
                       graphics_processor=graphics_processors[1])
