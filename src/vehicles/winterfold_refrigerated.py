from road_vehicle import RefrigeratedTramConsist, ElectricVehicleUnit

consist = RefrigeratedTramConsist(id='winterfold_refrigerated',
                           base_numeric_id=770,
                           name='Winterfold',
                           gen=2,
                           intro_date_offset=10)  # introduce later than gen epoch by design

consist.add_unit(base_platform=None, # no base platform by design currently
                 type=ElectricVehicleUnit,
                 vehicle_length=8,
                 repeat=2)
