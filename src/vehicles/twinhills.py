import global_constants
from road_vehicle import PaxHauler

consist = PaxHauler(id = 'twinhills',
                base_numeric_id = 70,
                title = 'Twinhills [Passenger Tram]',
                roadveh_flag_tram = True,
                replacement_id = '-none',
                vehicle_life = 40,
                intro_date = 1990)

consist.add_unit(capacity = 70,
                vehicle_length = 8,
                effects = ['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                repeat = 2)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
