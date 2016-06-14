import global_constants
from road_vehicle import RVConsist, PaxExpressHauler

# for each generation, bus and coach variants have same power and intro date
# coaches lower weight, faster, lower capacity than equivalent bus

consist = RVConsist(vehicle_type = PaxExpressHauler,
                id = 'glenmore',
                base_numeric_id = 50,
                title = 'Glenmore [Coach]',
                replacement_id = '-none',
                power = 160,
                speed = 55,
                vehicle_life = 40,
                intro_date = 1935)

consist.add_unit(weight = 8,
                capacity = 30,
                vehicle_length = 7,
                visual_effect = 'VISUAL_EFFECT_DIESEL')

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
