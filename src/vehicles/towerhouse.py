import global_constants
from road_vehicle import FlatBedHauler

consist = FlatBedHauler(id = 'towerhouse',
                base_numeric_id = 650,
                title = 'Towerhouse [Flatbed Truck]',
                replacement_id = '-none',
                semi_truck_so_redistribute_capacity = True,
                vehicle_life = 40,
                intro_date = 1968)

consist.add_unit(weight = 7,
                vehicle_length = 2,
                semi_truck_shift_offset_jank = 2,
                visual_effect = 'VISUAL_EFFECT_DIESEL',
                always_use_same_spriterow = True)

consist.add_unit(weight = 5,
                capacity = 40,
                vehicle_length = 7)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0,
                       graphics_processor=consist.graphics_processors[0])
