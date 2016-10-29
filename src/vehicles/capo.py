import global_constants
from road_vehicle import OpenHauler

consist = OpenHauler(id = 'capo',
                base_numeric_id = 680,
                title = 'Capo [Open Truck]',
                replacement_id = '-none',
                vehicle_life = 40,
                intro_date = 1997)

consist.add_unit(capacity = 20,
                vehicle_length = 5,
                cargo_length = 3,
                effects = ['EFFECT_SPRITE_DIESEL, -2, 1, 10'])

consist.add_unit(capacity = 20,
                vehicle_length = 4,
                cargo_length = 3)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0,
                       graphics_processor=consist.graphics_processors[0])
