import global_constants
from road_vehicle import PaxHauler

# for each generation, bus and coach variants have same power and intro date
# coaches faster, lower capacity than equivalent bus

consist = PaxHauler(id='thunder',
                    base_numeric_id=40,
                    title='Thunder [Bus]',
                    power=160,
                    speed=45,
                    vehicle_life=40,
                    intro_date=1935)

consist.add_unit(capacity=50,
                 vehicle_length=7,
                 visual_effect='VISUAL_EFFECT_DIESEL')

consist.add_model_variant(intro_date=0,
                          end_date=global_constants.max_game_date,
                          spritesheet_suffix=0)
