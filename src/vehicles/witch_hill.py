import global_constants
import graphics_processor.utils as graphics_utils
from road_vehicle import RVConsist, MiningHauler

graphics_processors = graphics_utils.get_mining_hauler_processors(template='witch_hill_template.png',
                                              copy_block_top_offsets = [10],
                                              paste_top_offset = 10)

consist = RVConsist(id = 'witch_hill',
              base_numeric_id = 500,
              title = 'Witch Hill [Mining Truck]',
              replacement_id = '-none',
              power = 1200,
              speed = 55, # dibbled up above RL for game balance
              type_base_running_cost_points = 30, # dibble running costs for game balance
              vehicle_life = 40,
              intro_date = 1989)

consist.add_unit(MiningHauler(consist = consist,
                        weight = 60,
                        capacity = 120,
                        vehicle_length = 7,
                        effects = ['EFFECT_SPRITE_DIESEL, -3, 0, 13'],
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0,
                       graphics_processor=graphics_processors[0])
