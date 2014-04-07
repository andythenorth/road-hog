import global_constants
from road_vehicle import EngineConsist, PaxHauler

consist = EngineConsist(id = 'fairlop',
              base_numeric_id = 10,
              title = 'Fairlop [Passenger Tram]',
              roadveh_flag_tram = True,
              replacement_id = '-none',
              power = 120,
              speed = 35,
              buy_cost = 69,
              fixed_run_cost_factor = 3.5,
              fuel_run_cost_factor = 1.0,
              vehicle_life = 40,
              intro_date = 1905,
              graphics_status = '')

consist.add_unit(PaxHauler(consist = consist,
                        weight = 12,
                        capacity_pax = 40,
                        vehicle_length = 7,
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)