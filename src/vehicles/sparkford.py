import global_constants
from road_vehicle import RefrigeratedHauler

consist = RefrigeratedHauler(id = 'sparkford',
                base_numeric_id = 390,
                title = 'Sparkford [Reefer Tram]',
                roadveh_flag_tram = True,
                replacement_id = '-none',
                vehicle_life = 40,
                intro_date = 1955)

consist.add_unit(weight = 14,
                capacity = 48,
                vehicle_length = 8,
                effects = ['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                repeat = 2)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
