import global_constants
from road_vehicle import FlatBedHauler

consist = FlatBedHauler(id = 'rackwood',
                base_numeric_id = 740,
                title = 'Rackwood [Flatbed Tram]',
                roadveh_flag_tram = True,
                replacement_id = '-none',
                vehicle_life = 40,
                intro_date = 1900)

consist.add_unit(weight = 20,
                capacity = 0,
                vehicle_length = 3,
                effects = ['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'])

consist.add_unit(weight = 5,
                capacity = 24,
                vehicle_length = 4,
                repeat = 3)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
