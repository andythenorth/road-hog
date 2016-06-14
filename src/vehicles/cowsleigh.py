import global_constants
from road_vehicle import RVConsist, LivestockHauler

consist = RVConsist(vehicle_type = LivestockHauler,
                id = 'cowsleigh',
                base_numeric_id = 900,
                title = 'Cowsleigh [Livestock Truck]',
                replacement_id = '-none',
                vehicle_life = 40,
                intro_date = 1911)

consist.add_unit(weight = 10,
                capacity = 0,
                vehicle_length = 4,
                effect_spawn_model = 'EFFECT_SPAWN_MODEL_STEAM',
                effects = ['EFFECT_SPRITE_STEAM, -5, 0, 12'])

consist.add_unit(weight = 8,
                capacity = 12,
                vehicle_length = 5,
                repeat = 2)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
