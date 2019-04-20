from road_vehicle import RefrigeratedTruck, DieselRoadVehicle

consist = RefrigeratedTruck(id='fortiscue_refrigerated',
                            base_numeric_id=180,
                            name='Fortiscue',
                            vehicle_life=40,
                            gen=4,
                            intro_date_offset=4)  # introduce later than gen epoch by design

consist.add_unit(type=DieselRoadVehicle,
                 capacity=25,
                 vehicle_length=6)

consist.add_unit(capacity=15,
                 vehicle_length=4)
