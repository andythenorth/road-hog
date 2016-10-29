import global_constants
from road_vehicle import PaxExpressHauler

# for each generation, bus and coach variants have same power and intro date
# coaches faster, lower capacity than equivalent bus

consist = PaxExpressHauler(id = 'big_sky',
                base_numeric_id = 620,
                title = 'Big Sky [Coach]',
                power = 220,
                speed = 90,
                vehicle_life = 40,
                intro_date = 1990)

consist.add_unit(capacity = 40, # coaches never need high capacity
                vehicle_length = 7,
                visual_effect = 'VISUAL_EFFECT_DIESEL')

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
