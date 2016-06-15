import global_constants
from road_vehicle import RVConsist, SuppliesHauler

consist = RVConsist(vehicle_type = SuppliesHauler,
                id = 'reaver',
                base_numeric_id = 550,
                title = 'Reaver [Supplies Truck]',
                replacement_id = '-none',
                power = 200, # custom power
                vehicle_life = 40,
                intro_date = 1875)

consist.add_unit(weight = 7,
                capacity = 0,
                vehicle_length = 4,
                effect_spawn_model = 'EFFECT_SPAWN_MODEL_STEAM',
                effects = ['EFFECT_SPRITE_STEAM, -5, 0, 12'])

consist.add_unit(weight = 7,
                capacity = 45,
                vehicle_length = 7)

consist.add_unit(weight = 7,
                capacity = 0,
                vehicle_length = 4,
                effect_spawn_model = 'EFFECT_SPAWN_MODEL_STEAM',
                effects = ['EFFECT_SPRITE_STEAM, -5, 0, 12'],
                unit_num_providing_spriterow_num = 0)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
