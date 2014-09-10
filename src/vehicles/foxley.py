import global_constants
from road_vehicle import EngineConsist, CourierTruck

consist = EngineConsist(id = 'foxley',
              base_numeric_id = 470,
              title = 'Foxley [Courier Tram]',
              roadveh_flag_tram = True,
              replacement_id = '-none',
              power = 100,
              speed = 35,
              vehicle_life = 40,
              intro_date = 1905)

consist.add_unit(CourierTruck(consist = consist,
                        weight = 10,
                        capacity_freight = 20,
                        capacity_mail = 40,
                        vehicle_length = 7,
                        visual_effect = 'VISUAL_EFFECT_ELECTRIC',
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
