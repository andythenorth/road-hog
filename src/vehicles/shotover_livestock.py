from road_vehicle import LivestockTramConsist, ElectricVehicleUnit

consist = LivestockTramConsist(id='shotover_livestock',
                        base_numeric_id=370,
                        name='Shotover',
                        vehicle_life=40,
                        gen=3,
                        intro_date_offset=1)  # introduce later than gen epoch by design

consist.add_unit(type=ElectricVehicleUnit,
                 capacity=36,
                 vehicle_length=8,
                 repeat=2)
