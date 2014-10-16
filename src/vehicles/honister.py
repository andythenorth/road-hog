import global_constants
from road_vehicle import EngineConsist, BulkFarmHauler

consist = EngineConsist(id = 'honister',
              base_numeric_id = 220,
              title = 'Honister [Farm Bulk Truck]',
              replacement_id = '-none',
              power = 180,
              vehicle_life = 40,
              intro_date = 1943)

consist.add_unit(BulkFarmHauler(consist = consist,
                        weight = 6,
                        capacity = 0,
                        vehicle_length = 2,
                        semi_truck_shift_offset_jank = 2,
                        visual_effect = 'VISUAL_EFFECT_DIESEL',
                        spriterow_num = 0))

consist.add_unit(BulkFarmHauler(consist = consist,
                        weight = 6,
                        capacity = 35,
                        vehicle_length = 5,
                        spriterow_num = 1))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
