import global_constants
from road_vehicle import PaxHauler

consist = PaxHauler(id = 'ladycross',
                base_numeric_id = 0,
                title = 'Ladycross [Passenger Tram]',
                roadveh_flag_tram = True,
                replacement_id = '-none',
                power = 120,
                vehicle_life = 40,
                intro_date = 1860)

consist.add_unit(weight = 6,
                capacity = 0,
                vehicle_length = 3,
                effect_spawn_model = 'EFFECT_SPAWN_MODEL_STEAM',
                effects = ['EFFECT_SPRITE_STEAM, -2, 0, 14'])

consist.add_unit(weight = 6,
                capacity = 80,
                vehicle_length = 7)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
