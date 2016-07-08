import global_constants
from road_vehicle import FlatBedHauler

consist = FlatBedHauler(id = 'stakebeck',
                base_numeric_id = 750,
                title = 'Stakebeck [Flatbed Tram]',
                roadveh_flag_tram = True,
                replacement_id = '-none',
                vehicle_life = 40,
                intro_date = 1860)

consist.add_unit(weight = 20,
                capacity = 0,
                vehicle_length = 3,
                effect_spawn_model = 'EFFECT_SPAWN_MODEL_STEAM',
                effects = ['EFFECT_SPRITE_STEAM, -2, 0, 14'],
                always_use_same_spriterow = True)

consist.add_unit(weight = 5,
                capacity = 24,
                vehicle_length = 4,
                repeat = 2)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0,
                       graphics_processor=consist.graphics_processors[0])
