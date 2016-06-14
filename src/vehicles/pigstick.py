import global_constants
from road_vehicle import RVConsist, LivestockHauler

consist = RVConsist(vehicle_type = LivestockHauler,
                id = 'pigstick',
                base_numeric_id = 330,
                title = 'Pigstick [Livestock Truck]',
                replacement_id = '-none',
                vehicle_life = 40,
                intro_date = 1941)

consist.add_unit(weight = 10,
                capacity = 15,
                vehicle_length = 6,
                visual_effect = 'VISUAL_EFFECT_DIESEL')

consist.add_unit(weight = 10,
                capacity = 15,
                vehicle_length = 5)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
