import global_constants
from road_vehicle import DumpHauler

consist = DumpHauler(id = 'scrooby_top',
                base_numeric_id = 700,
                title = 'Scrooby Top [Dump Tram]',
                roadveh_flag_tram = True,
                replacement_id = '-none',
                vehicle_life = 40,
                intro_date = 1870)

consist.add_unit(weight = 30,
                capacity = 0,
                vehicle_length = 6,
                effect_spawn_model = 'EFFECT_SPAWN_MODEL_STEAM',
                effects = ['EFFECT_SPRITE_STEAM, -3, 0, 12', 'EFFECT_SPRITE_STEAM, 1, 0, 12'],
                always_use_same_spriterow = True)

consist.add_unit(weight = 2,
                capacity = 12,
                vehicle_length = 3,
                repeat = 4)

graphics_processors = consist.get_graphics_processors(paste_top_offset = 40)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0,
                       graphics_processor=graphics_processors[0])
