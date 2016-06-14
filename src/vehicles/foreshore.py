import global_constants
from road_vehicle import RVConsist, IntermodalHauler

consist = RVConsist(vehicle_type = IntermodalHauler,
                id = 'foreshore',
                base_numeric_id = 170,
                title = 'Foreshore [Intermodal Hauler]',
                replacement_id = '-none',
                power = 950,
                vehicle_life = 40,
                intro_date = 1959)

consist.add_unit(weight = 50,
                capacity = 50,
                vehicle_length = 7,
                visual_effect = 'VISUAL_EFFECT_DIESEL')

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
