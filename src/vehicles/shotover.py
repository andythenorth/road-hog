import global_constants
from road_vehicle import EngineConsist, LivestockHauler

consist = EngineConsist(id = 'shotover',
              base_numeric_id = 300,
              title = 'Shotover [Livestock Tram]',
              roadveh_flag_tram = True,
              str_type_info = 'COASTER',
              replacement_id = '-none',
              power = 120,
              speed = 35,
              buy_cost = 69,
              fixed_run_cost_factor = 3.5,
              fuel_run_cost_factor = 1.0,
              vehicle_life = 40,
              intro_date = 1959,
              graphics_status = '')

consist.add_unit(LivestockHauler(consist = consist,
                        weight = 12,
                        capacity_freight = 20,
                        vehicle_length = 7,
                        spriterow_num = 0), repeat = 2)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
