import global_constants
from road_vehicle import OpenHauler

consist = OpenHauler(id = 'buildwas',
                base_numeric_id = 120,
                title = 'Buildwas [Open Tram]',
                roadveh_flag_tram = True,
                replacement_id = '-none',
                vehicle_life = 40,
                intro_date = 1860)

consist.add_unit(weight = 12,
                capacity = 0,
                vehicle_length = 3,
                effect_spawn_model = 'EFFECT_SPAWN_MODEL_STEAM',
                effects = ['EFFECT_SPRITE_STEAM, -2, 0, 14'])

consist.add_unit(weight = 4,
                capacity = 24,
                vehicle_length = 4,
                repeat=2)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
