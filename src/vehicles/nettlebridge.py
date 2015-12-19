import global_constants
import graphics_processor.utils as graphics_utils
from road_vehicle import RVConsist, DumpHauler

graphics_processors = graphics_utils.get_bulk_cargo_processors(template='nettlebridge_template.png',
                                              copy_block_top_offsets = [10],
                                              paste_top_offset = 10)

consist = RVConsist(id = 'nettlebridge',
              base_numeric_id = 310,
              title = 'Nettlebridge [Dump Tram]',
              roadveh_flag_tram = True,
              replacement_id = '-none',
              power = 300,
              vehicle_life = 40,
              intro_date = 1944)

consist.add_unit(DumpHauler(consist = consist,
                        weight = 12,
                        capacity = 48,
                        vehicle_length = 8,
                        effects = ['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                        spriterow_num = 0), repeat=2)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0,
                       graphics_processor=graphics_processors[0])
