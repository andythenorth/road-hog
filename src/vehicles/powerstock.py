import global_constants
from road_vehicle import EngineConsist, BulkFarmHauler

consist = EngineConsist(id = 'powerstock',
              base_numeric_id = 340,
              title = 'Powerstock [Farm Bulk Truck]',
              replacement_id = '-none',
              power = 650,
              vehicle_life = 40,
              intro_date = 1983)

consist.add_unit(BulkFarmHauler(consist = consist,
                        weight = 8,
                        capacity = 0,
                        vehicle_length = 2,
                        semi_truck_shift_offset_jank = 2,
                        effects = ['EFFECT_SPRITE_DIESEL, -2, 1, 10'],
                        spriterow_num = 0))

consist.add_unit(BulkFarmHauler(consist = consist,
                        weight = 8,
                        capacity = 40,
                        vehicle_length = 5,
                        spriterow_num = 1))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
