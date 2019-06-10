from road_vehicle import PaxLocalTramConsist, ElectricVehicleUnit

consist = PaxLocalTramConsist(id='fairlop_pax',
                       base_numeric_id=10,
                       name='Fairlop',
                       gen=2,
                       intro_date_offset=3)  # introduce later than gen epoch by design

consist.add_unit(base_platform=None, # pax trams have no base platform by design currently
                 type=ElectricVehicleUnit,
                 vehicle_length=6,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 12'])

consist.add_unit(base_platform=None, # pax trams have no base platform by design currently
                 vehicle_length=5,
                 repeat=2)
