import global_constants
from road_vehicle import RVConsist, PaxExpressHauler

# for each generation, bus and coach variants have same power and intro date
# coaches lower weight, faster, lower capacity than equivalent bus

consist = RVConsist(vehicle_type = PaxExpressHauler,
                id = 'acton',
                base_numeric_id = 600,
                title = 'Acton [Coach]',
                replacement_id = '-none',
                power = 360,
                speed = 90,
                vehicle_life = 40,
                intro_date = 1990)

consist.add_unit(weight = 10,
                capacity = 40, # coaches never need high capacity
                vehicle_length = 7,
                visual_effect = 'VISUAL_EFFECT_DIESEL',
                spriterow_num = 0)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
