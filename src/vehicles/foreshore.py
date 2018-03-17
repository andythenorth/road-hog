from road_vehicle import IntermodalHauler

consist = IntermodalHauler(id='foreshore',
                           base_numeric_id=170,
                           title='Foreshore [Intermodal Hauler]',
                           power=950,
                           vehicle_life=40,
                           intro_date=1959)

consist.add_unit(capacity=50,
                 vehicle_length=7,
                 visual_effect='VISUAL_EFFECT_DIESEL')

consist.add_model_variant(spritesheet_suffix=0)
