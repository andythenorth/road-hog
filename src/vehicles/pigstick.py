import global_constants
from road_vehicle import EngineConsist, LivestockHauler

consist = EngineConsist(id = 'pigstick',
              base_numeric_id = 310,
              title = 'Pigstick [Livestock Truck]',
              replacement_id = '-none',
              power = 180,
              speed = 50,
              buy_cost = 69,
              fixed_run_cost_factor = 3.5,
              fuel_run_cost_factor = 1.0,
              vehicle_life = 40,
              intro_date = 1943,
              graphics_status = '')

consist.add_unit(LivestockHauler(consist = consist,
                        weight = 10,
                        capacity_freight = 12,
                        vehicle_length = 7,
                        spriterow_num = 0))

consist.add_unit(LivestockHauler(consist = consist,
                        weight = 10,
                        capacity_freight = 12,
                        vehicle_length = 7,
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
