from road_vehicle import MailTram, ElectricRoadVehicle

consist = MailTram(id='foxley_mail',
                   base_numeric_id=190,
                   name='Foxley',
                   power=240,  # custom HP
                   vehicle_life=40,
                   gen=2,
                   intro_date_offset=3)  # introduce later than gen epoch by design

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=15,
                 vehicle_length=4,
                 repeat=2)
