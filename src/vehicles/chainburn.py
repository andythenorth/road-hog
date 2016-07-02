import global_constants
from road_vehicle import RVConsist, FlatBedHauler

consist = RVConsist(vehicle_type = FlatBedHauler,
                id = 'chainburn',
                base_numeric_id = 630,
                title = 'Chainburn [Flatbed Truck]',
                replacement_id = '-none',
                vehicle_life = 40,
                intro_date = 1910)

consist.add_unit(weight = 10,
                capacity = 12,
                vehicle_length = 5,
                effect_spawn_model = 'EFFECT_SPAWN_MODEL_STEAM',
                effects = ['EFFECT_SPRITE_STEAM, -3, 0, 12'])

consist.add_unit(weight = 5,
                capacity = 12,
                vehicle_length = 4)
"""
!! turned off whilst refactoring
graphics_processors = consist.get_graphics_processors(copy_block_top_offsets = [10, 100],
                                                      paste_top_offset = 10)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0,
                       graphics_processor=graphics_processors[0])
"""

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
