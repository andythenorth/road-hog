import global_constants
from road_vehicle import CourierCar

consist = CourierCar(id = 'tin_hatch',
                base_numeric_id = 820,
                title = 'Tin Hatch [Courier Tram]',
                roadveh_flag_tram = True,
                replacement_id = '-none',
                power = 100, # custom power
                vehicle_life = 40,
                intro_date = 1860)

consist.add_unit(weight = 30,
                capacity = 0,
                vehicle_length = 3,
                effect_spawn_model = 'EFFECT_SPAWN_MODEL_STEAM',
                effects = ['EFFECT_SPRITE_STEAM, -3, 0, 12', 'EFFECT_SPRITE_STEAM, 1, 0, 12'])

consist.add_unit(weight = 3,
                capacity = 24,
                vehicle_length = 7)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
