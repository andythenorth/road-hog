import global_constants
from road_vehicle import RVConsist, PaxHauler

# for each generation, bus and coach variants have same power and intro date
# coaches lower weight, faster, lower capacity than equivalent bus

consist = RVConsist(vehicle_type = PaxHauler,
                id = 'highgate',
                base_numeric_id = 590,
                title = 'Highgate [Bus]',
                replacement_id = '-none',
                power = 240,
                speed = 50,
                vehicle_life = 40,
                intro_date = 1964)

consist.add_unit(weight = 14,
                capacity = 70,
                vehicle_length = 7,
                visual_effect = 'VISUAL_EFFECT_DIESEL',
                spriterow_num = 0)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
