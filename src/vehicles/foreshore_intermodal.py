from road_vehicle import IntermodalHauler

consist = IntermodalHauler(id='foreshore',
                           base_numeric_id=970,
                           name='Foreshore',
                           power=950,
                           vehicle_life=40,
                           gen=4,
                           intro_date=1959)

consist.add_unit(capacity=50,
                 vehicle_length=7)
