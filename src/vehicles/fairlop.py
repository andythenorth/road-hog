import global_constants
from road_vehicle import EngineConsist, PaxHauler

consist = EngineConsist(id = 'fairlop',
              base_numeric_id = 10,
              title = 'Fairlop [Passenger Tram]',
              roadveh_flag_tram = True,
              replacement_id = '-none',
              power = 120,
              vehicle_life = 40,
              intro_date = 1905)

consist.add_unit(PaxHauler(consist = consist,
                        weight = 12,
                        capacity_pax = 40,
                        vehicle_length = 7,
                        visual_effect = 'VISUAL_EFFECT_ELECTRIC',
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
