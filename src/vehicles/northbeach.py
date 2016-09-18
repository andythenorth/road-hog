import global_constants
from road_vehicle import PaxHauler

consist = PaxHauler(id = 'northbeach',
                base_numeric_id = 690,
                title = 'Northbeach [Passenger Tram]',
                roadveh_flag_tram = True,
                replacement_id = '-none',
                power = 360,
                vehicle_life = 40,
                intro_date = 1961)

consist.add_unit(weight = 20,
                capacity = 100,
                vehicle_length = 6,
                effects = ['EFFECT_SPRITE_ELECTRIC, 0, 0, 12'],
                repeat = 2)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
