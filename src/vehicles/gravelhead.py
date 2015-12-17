import global_constants
import graphics_processor.utils as graphics_utils
from road_vehicle import RVConsist, MiningHauler

graphics_processors = graphics_utils.get_mining_hauler_processors(template='gravelhead_template.png',
                                              copy_block_top_offsets = [10, 100],
                                              paste_top_offset = 10)

consist = RVConsist(id = 'gravelhead',
              base_numeric_id = 580,
              title = 'Gravelhead [Mining Truck]',
              replacement_id = '-none',
              power = 130,
              vehicle_life = 40,
              intro_date = 1930)

consist.add_unit(MiningHauler(consist = consist,
                        weight = 10,
                        capacity = 25,
                        vehicle_length = 6,
                        effect_spawn_model = 'EFFECT_SPAWN_MODEL_STEAM',
                        effects = ['EFFECT_SPRITE_STEAM, -3, 0, 12'],
                        spriterow_num = 0))

consist.add_unit(MiningHauler(consist = consist,
                        weight = 5,
                        capacity = 25,
                        vehicle_length = 5,
                        spriterow_adjust = {'multiplier': 2, 'offset': 1}))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0,
                       graphics_processor=graphics_processors[1])
