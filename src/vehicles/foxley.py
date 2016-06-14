import global_constants
from road_vehicle import RVConsist, CourierCar

consist = RVConsist(vehicle_type = CourierCar,
                id = 'foxley',
                base_numeric_id = 190,
                title = 'Foxley [Courier Tram]',
                roadveh_flag_tram = True,
                replacement_id = '-none',
                power = 200, # custom HP
                vehicle_life = 40,
                intro_date = 1903)

consist.add_unit(weight = 10,
                capacity = 30,
                vehicle_length = 6,
                effects = ['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'])

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
