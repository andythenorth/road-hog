from road_vehicle import RefrigeratedTramConsist, ElectricRoadVehicle

consist = RefrigeratedTramConsist(id='sparkford_refrigerated',
                           base_numeric_id=390,
                           name='Sparkford',
                              vehicle_life=40,
                           gen=3,
                           intro_date_offset=10)  # introduce later than gen epoch by design

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=36,
                 vehicle_length=8,
                 repeat=2)
