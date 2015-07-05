import global_constants
from road_vehicle import EngineConsist, PaxExpressHauler

consist = EngineConsist(id = 'big_sky',
              base_numeric_id = 620,
              title = 'Big Sky [Coach]',
              replacement_id = '-none',
              power = 220,
              speed_dibble = 'speedy',
              vehicle_life = 40,
              intro_date = 1999)

consist.add_unit(PaxExpressHauler(consist = consist,
                        weight = 20,
                        capacity = 40, # coaches never need high capacity
                        vehicle_length = 7,
                        visual_effect = 'VISUAL_EFFECT_DIESEL',
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
