import global_constants
from road_vehicle import RVConsist, PaxHauler

consist = RVConsist(vehicle_type = PaxHauler,
                id = 'newbold',
                base_numeric_id = 30,
                title = 'Newbold [Passenger Tram]',
                roadveh_flag_tram = True,
                replacement_id = '-none',
                power = 240,
                vehicle_life = 40,
                intro_date = 1932)

consist.add_unit(weight = 16,
                capacity = 80,
                vehicle_length = 7,
                effects = ['EFFECT_SPRITE_ELECTRIC, 0, 0, 12'],
                spriterow_num = 0,
                repeat=2)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
