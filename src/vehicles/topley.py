import global_constants
from road_vehicle import RVConsist, PaxHauler

# for each generation, bus and coach variants have same power and intro date
# coaches lower weight, faster, lower capacity than equivalent bus

consist = RVConsist(id = 'topley',
              base_numeric_id = 60,
              title = 'Topley [Bus]',
              replacement_id = '-none',
              power = 360,
              speed = 55,
              vehicle_life = 40,
              intro_date = 1990)

consist.add_unit(PaxHauler(consist = consist,
                        weight = 16,
                        capacity = 90,
                        vehicle_length = 7,
                        visual_effect = 'VISUAL_EFFECT_DIESEL',
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
