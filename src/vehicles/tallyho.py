import global_constants
from road_vehicle import RVConsist, CourierCar

consist = RVConsist(vehicle_type = CourierCar,
                id = 'tallyho',
                base_numeric_id = 450,
                title = 'Tallyho [Courier Truck]',
                replacement_id = '-none',
                power = 90,
                vehicle_life = 40,
                intro_date = 1909)

consist.add_unit(weight = 3,
                capacity = 15,
                capacity_mail = 30,
                vehicle_length = 6,
                visual_effect = 'VISUAL_EFFECT_DIESEL',
                spriterow_num = 0)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
