import global_constants
from road_vehicle import RVConsist, OpenHauler

consist = RVConsist(vehicle_type = OpenHauler,
                id = 'jinglepot',
                base_numeric_id = 240,
                title = 'Jinglepot [Open Truck]',
                replacement_id = '-none',
                vehicle_life = 40,
                intro_date = 1910)

consist.add_unit(weight = 10,
                capacity = 12,
                vehicle_length = 5,
                effect_spawn_model = 'EFFECT_SPAWN_MODEL_STEAM',
                effects = ['EFFECT_SPRITE_STEAM, -3, 0, 12'],
                spriterow_num = 0)

consist.add_unit(weight = 5,
                capacity = 12,
                vehicle_length = 4,
                spriterow_num = 1)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
