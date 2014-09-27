import global_constants
from road_vehicle import EngineConsist, PaxHauler

consist = EngineConsist(id = 'ladycross',
              base_numeric_id = 0,
              title = 'Ladycross [Passenger Tram]',
              roadveh_flag_tram = True,
              replacement_id = '-none',
              power = 100,
              vehicle_life = 40,
              intro_date = 1860)

consist.add_unit(PaxHauler(consist = consist,
                        weight = 6,
                        capacity_pax = 0,
                        vehicle_length = 3,
                        visual_effect = 'VISUAL_EFFECT_STEAM',
                        spriterow_num = 0))

consist.add_unit(PaxHauler(consist = consist,
                        weight = 4,
                        capacity_pax = 30,
                        vehicle_length = 5,
                        spriterow_num = 1))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
