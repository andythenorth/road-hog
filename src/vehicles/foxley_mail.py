from road_vehicle import MailTramConsist, ElectricVehicleUnit

consist = MailTramConsist(id='foxley_mail',
                   base_numeric_id=190,
                   name='Foxley',
                   power=240,  # custom HP
                   gen=2,
                   intro_date_offset=3)  # introduce later than gen epoch by design

consist.add_unit(type=ElectricVehicleUnit,
                 vehicle_length=4,
                 repeat=2)
