import global_constants
from road_vehicle import RVConsist, CourierCar

consist = RVConsist(vehicle_type = CourierCar,
                id = 'littleduke',
                base_numeric_id = 270,
                title = 'Littleduke [Courier Truck]',
                replacement_id = '-none',
                power = 380,
                speed = 90,
                vehicle_life = 40,
                intro_date = 1998)

consist.add_unit(weight = 7,
                capacity = 25,
                vehicle_length = 6,
                visual_effect = 'VISUAL_EFFECT_DIESEL',
                spriterow_num = 0)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
