import global_constants
from road_vehicle import EngineConsist, GeneralCargoHauler

consist = EngineConsist(id = 'littleduke',
              base_numeric_id = 180,
              title = 'Littleduke [General Cargo Truck]',
              replacement_id = '-none',
              power = 380,
              speed = 75,
              buy_cost = 69,
              fixed_run_cost_factor = 3.5,
              fuel_run_cost_factor = 1.0,
              vehicle_life = 40,
              intro_date = 1998,
              graphics_status = '')

consist.add_unit(GeneralCargoHauler(consist = consist,
                        weight = 7,
                        capacity_freight = 25,
                        vehicle_length = 7,
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
