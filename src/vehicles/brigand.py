import global_constants
from road_vehicle import SuppliesHauler
# equiv. Scammell Highwayman or Explorer with dolly low loader trailer - not huge

consist = SuppliesHauler(id = 'brigand',
                base_numeric_id = 540,
                title = 'Brigand [Supplies Truck]',
                power = 480,
                vehicle_life = 40,
                intro_date = 1953)

consist.add_unit(capacity = 0,
                vehicle_length = 6,
                visual_effect = 'VISUAL_EFFECT_DIESEL')

consist.add_unit(capacity = 45,
                vehicle_length = 7)

consist.add_unit(capacity = 0,
                vehicle_length = 6,
                visual_effect = 'VISUAL_EFFECT_DIESEL',
                unit_num_providing_spriterow_num = 0)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
