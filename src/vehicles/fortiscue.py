import global_constants
from road_vehicle import RefrigeratedHauler

consist = RefrigeratedHauler(id = 'fortiscue',
                base_numeric_id = 180,
                title = 'Fortiscue [Reefer Truck]',
                replacement_id = '-none',
                vehicle_life = 40,
                intro_date = 1972)

consist.add_unit(capacity = 25,
                vehicle_length = 6,
                visual_effect = 'VISUAL_EFFECT_DIESEL')

consist.add_unit(capacity = 15,
                vehicle_length = 4)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
