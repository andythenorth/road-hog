import global_constants
from road_vehicle import EngineConsist, Tanker

consist = EngineConsist(id = 'greenscoe',
              base_numeric_id = 210,
              title = 'Greenscoe [Tanker Truck]',
              replacement_id = '-none',
              power = 150,
              speed_dibble = 'plodding', # tankers are hazardous, apply speed penalty
              vehicle_life = 40,
              intro_date = 1943)

consist.add_unit(Tanker(consist = consist,
                        weight = 7,
                        capacity = 0,
                        vehicle_length = 2,
                        semi_truck_shift_offset_jank = 2,
                        effects = ['EFFECT_SPRITE_DIESEL, -3, 1, 10'],
                        spriterow_num = 0))

consist.add_unit(Tanker(consist = consist,
                        weight = 7,
                        capacity = 30,
                        vehicle_length = 5,
                        spriterow_num = 1))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
