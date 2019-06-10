from road_vehicle import PaxLocalTramConsist, ElectricVehicleUnit

consist = PaxLocalTramConsist(id='newbold_pax',
                       base_numeric_id=30,
                       name='Newbold',
                       gen=3,
                       intro_date_offset=1)  # introduce later than gen epoch by design

consist.add_unit(base_platform=None, # pax trams have no base platform by design currently
                 type=ElectricVehicleUnit,
                 vehicle_length=8,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 12'],
                 repeat=2)
