from road_vehicle import PaxLocalTramConsist, ElectricVehicleUnit

consist = PaxLocalTramConsist(id='twinhills_pax',
                       base_numeric_id=70,
                       name='Twinhills',
                       gen=5)

consist.add_unit(base_platform=None, # pax trams have no base platform by design currently
                 type=ElectricVehicleUnit,
                 vehicle_length=8,
                 repeat=2)
