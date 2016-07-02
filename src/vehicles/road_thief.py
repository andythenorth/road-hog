import global_constants
from road_vehicle import SuppliesHauler
# 4 axle machinery hauler, with 4 axle lowbed or drag trailer, (not huge)

consist = SuppliesHauler(id = 'road_thief',
                base_numeric_id = 560,
                title = 'Road Thief [Supplies Truck]',
                replacement_id = '-none',
                power = 650,
                vehicle_life = 40,
                intro_date = 1989)

consist.add_unit(weight = 20,
                capacity = 0,
                vehicle_length = 7,
                visual_effect = 'VISUAL_EFFECT_DIESEL')

consist.add_unit(weight = 20,
                capacity = 45,
                vehicle_length = 7)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
