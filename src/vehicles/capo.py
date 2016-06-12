import global_constants
from road_vehicle import RVConsist, OpenHauler

consist = RVConsist(vehicle_type = OpenHauler,
                id = 'capo',
                base_numeric_id = 680,
                title = 'Capo [Open Truck]',
                replacement_id = '-none',
                vehicle_life = 40,
                intro_date = 1997)

consist.add_unit(weight = 10,
                capacity = 20,
                vehicle_length = 5,
                effects = ['EFFECT_SPRITE_DIESEL, -2, 1, 10'],
                spriterow_num = 0)

consist.add_unit(weight = 5,
                capacity = 20,
                vehicle_length = 4,
                spriterow_num = 1)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
