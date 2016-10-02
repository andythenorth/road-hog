import global_constants
from road_vehicle import PaxHauler

# for each generation, bus and coach variants have same power and intro date
# coaches lower weight, faster, lower capacity than equivalent bus

consist = PaxHauler(id = 'topley',
                base_numeric_id = 60,
                title = 'Topley [Bus]',
                replacement_id = '-none',
                power = 360,
                speed = 55,
                vehicle_life = 40,
                intro_date = 1990)

consist.add_unit(weight = 16,
                capacity = 72,
                vehicle_length = 7,
                visual_effect = 'VISUAL_EFFECT_DIESEL')

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
