import global_constants
from road_vehicle import RVConsist, PaxHauler

# for each generation, bus and coach variants have same power and intro date
# coaches lower weight, faster, lower capacity than equivalent bus

consist = RVConsist(id = 'thunder',
              base_numeric_id = 40,
              title = 'Thunder [Bus]',
              replacement_id = '-none',
              power = 160,
              speed = 45,
              vehicle_life = 40,
              intro_date = 1935)

consist.add_unit(PaxHauler(consist = consist,
                        weight = 12,
                        capacity = 50,
                        vehicle_length = 7,
                        visual_effect = 'VISUAL_EFFECT_DIESEL',
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
