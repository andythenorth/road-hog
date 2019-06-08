from road_vehicle import RefrigeratedTramConsist, ElectricVehicleUnit

consist = RefrigeratedTramConsist(id='winterfold_refrigerated',
                           base_numeric_id=770,
                           name='Winterfold',
                              vehicle_life=40,
                           gen=2,
                           intro_date_offset=10)  # introduce later than gen epoch by design

consist.add_unit(type=ElectricVehicleUnit,
                 capacity=30,
                 vehicle_length=8,
                 repeat=2)
