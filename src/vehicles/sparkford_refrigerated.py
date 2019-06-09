from road_vehicle import RefrigeratedTramConsist, ElectricVehicleUnit

consist = RefrigeratedTramConsist(id='sparkford_refrigerated',
                           base_numeric_id=390,
                           name='Sparkford',
                               gen=3,
                           intro_date_offset=10)  # introduce later than gen epoch by design

consist.add_unit(type=ElectricVehicleUnit,
                 vehicle_length=8,
                 repeat=2)
