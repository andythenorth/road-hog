import global_constants
from road_vehicle import DumpHauler

consist = DumpHauler(id = 'gravelhead',
                base_numeric_id = 580,
                title = 'Gravelhead [Dump Truck]',
                power = 130,
                vehicle_life = 40,
                intro_date = 1920)

consist.add_unit(capacity = 12,
                vehicle_length = 6,
                effect_spawn_model = 'EFFECT_SPAWN_MODEL_STEAM',
                effects = ['EFFECT_SPRITE_STEAM, -3, 0, 12'])

consist.add_unit(capacity = 12,
                vehicle_length = 5)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0,
                       graphics_processor=consist.graphics_processors[1])
