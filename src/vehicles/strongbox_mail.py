from road_vehicle import MailTramConsist, ElectricVehicleUnit

consist = MailTramConsist(id='strongbox_mail',
                   base_numeric_id=830,
                   name='Strongbox',
                   power=480,  # custom power
                   gen=4,
                   intro_date_offset=1)  # introduce later than gen epoch by design

consist.add_unit(base_platform=None, # mail trams have no base platform by design currently
                 type=ElectricVehicleUnit,
                 vehicle_length=8,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'])
