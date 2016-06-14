import global_constants
from road_vehicle import RVConsist, PaxHauler

consist = RVConsist(vehicle_type = PaxHauler,
                id = 'twinhills',
                base_numeric_id = 70,
                title = 'Twinhills [Passenger Tram]',
                roadveh_flag_tram = True,
                replacement_id = '-none',
                power = 480,
                vehicle_life = 40,
                intro_date = 1990)

consist.add_unit(weight = 18,
                capacity = 80,
                vehicle_length = 7,
                effects = ['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'])

consist.add_unit(weight = 18,
                capacity = 80,
                vehicle_length = 5)

consist.add_unit(weight = 18,
                capacity = 80,
                vehicle_length = 7)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
