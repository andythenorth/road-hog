from road_vehicle import LivestockTramConsist, ElectricVehicleUnit

consist = LivestockTramConsist(id='trotalong_livestock',
                        base_numeric_id=720,
                        name='Trotalong',
                         gen=2,
                        intro_date_offset=1)  # introduce later than gen epoch by design

consist.add_unit(type=ElectricVehicleUnit,
                 vehicle_length=8,
                 repeat=2)
