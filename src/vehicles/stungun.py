import global_constants
from road_vehicle import EngineConsist, LivestockHauler

consist = EngineConsist(id = 'stungun',
              base_numeric_id = 430,
              title = 'Stungun [Livestock Truck]',
              replacement_id = '-none',
              power = 400,
              vehicle_life = 40,
              intro_date = 1999)

consist.add_unit(LivestockHauler(consist = consist,
                        weight = 8,
                        capacity = 0,
                        vehicle_length = 2,
                        semi_truck_shift_offset_jank = 2,
                        effects = ['EFFECT_SPRITE_DIESEL, -2, 1, 10'],
                        spriterow_num = 0))

consist.add_unit(LivestockHauler(consist = consist,
                        weight = 14,
                        capacity = 40,
                        vehicle_length = 7,
                        spriterow_num = 1))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
