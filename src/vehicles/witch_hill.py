import global_constants
from road_vehicle import DumpHauler

consist = DumpHauler(id = 'witch_hill',
                base_numeric_id = 500,
                title = 'Witch Hill [Mining Truck]',
                power = 900,
                speed = 50, # dibbled up above RL for game balance
                type_base_running_cost_points = 30, # dibble running costs for game balance
                vehicle_life = 40,
                intro_date = 2007)

consist.add_unit(capacity = 85, # much bigger is not much better here
                vehicle_length = 7,
                effects = ['EFFECT_SPRITE_AIRCRAFT_BREAKDOWN_SMOKE, -2, 1, 10', 'EFFECT_SPRITE_AIRCRAFT_BREAKDOWN_SMOKE, -2, -1, 10'])

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0,
                       graphics_processor=consist.graphics_processors[0])

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=1,
                       graphics_processor=consist.graphics_processors[1])
