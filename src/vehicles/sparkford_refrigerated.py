from road_vehicle import RefrigeratedTram, ElectricRoadVehicle

consist = RefrigeratedTram(id='sparkford_refrigerated',
                           base_numeric_id=390,
                           name='Sparkford',
                           tram_type='ELRL',
                           vehicle_life=40,
                           gen=3,
                           intro_date_offset=10)  # introduce later than gen epoch by design

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=36,
                 vehicle_length=8,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 repeat=2)
