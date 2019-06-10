from road_vehicle import MailTruckConsist, DieselVehicleUnit

consist = MailTruckConsist(id='brass_monkey_mail',
                    base_numeric_id=570,
                    name='Brass Monkey',
                    power=140,
                    speed=55,
                    gen=3,
                    intro_date_offset=1)  # introduce later than gen epoch by design

consist.add_unit(base_platform=None, # mail trucks have no base platform by design currently
                 type=DieselVehicleUnit,
                 vehicle_length=6)
