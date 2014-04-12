import global_constants
from road_vehicle import EngineConsist, PaxHauler

consist = EngineConsist(id = 'moota',
              base_numeric_id = 50,
              title = 'Moota [Bus]',
              replacement_id = '-none',
              power = 220,
              speed = 75,
              vehicle_life = 40,
              intro_date = 1968,
              graphics_status = '')

consist.add_unit(PaxHauler(consist = consist,
                        weight = 20,
                        capacity_pax = 50,
                        vehicle_length = 7,
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
