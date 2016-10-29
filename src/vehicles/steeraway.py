import global_constants
from road_vehicle import FoundryHauler

consist = FoundryHauler(id = 'steeraway',
                base_numeric_id = 520,
                title = 'Steeraway [Foundry Hauler]',
                power = 500,
                speed = 45,
                vehicle_life = 80,
                intro_date = 1960)

consist.add_unit(capacity = 0,
                vehicle_length = 6,
                visual_effect = 'VISUAL_EFFECT_DIESEL')

consist.add_unit(capacity = 50,
                vehicle_length = 7,
                repeat=2)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
