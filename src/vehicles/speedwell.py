import global_constants
from road_vehicle import EngineConsist, BoxHauler

consist = EngineConsist(id = 'speedwell',
              base_numeric_id = 400,
              title = 'Speedwell [Box Truck]',
              replacement_id = '-none',
              power = 450,
              vehicle_life = 40,
              intro_date = 1985)

consist.add_unit(BoxHauler(consist = consist,
                        weight = 7,
                        capacity = 0,
                        vehicle_length = 2,
                        semi_truck_shift_offset_jank = 2,
                        effects = ['EFFECT_SPRITE_DIESEL, -2, 1, 10'],
                        spriterow_num = 0))

consist.add_unit(BoxHauler(consist = consist,
                        weight = 8,
                        capacity = 40,
                        vehicle_length = 6,
                        spriterow_num = 1))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
