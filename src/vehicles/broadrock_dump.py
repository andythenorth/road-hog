from road_vehicle import DumpHEQSConsist
from base_platforms.heqs import DieselConventionalCabSemiTractorHaulerGen3A

consist = DumpHEQSConsist(id='broadrock_dump',
                   base_numeric_id=100,
                   name='Broadrock',
                   power=400,
                   speed=40,  # dibbled up above RL for game balance
                   type_base_running_cost_points=20,  # dibble running costs for game balance
                   gen=3,
                   intro_date_offset=-3)  # introduce earlier than gen epoch by design

consist.add_unit(base_platform=DieselConventionalCabSemiTractorHaulerGen3A)

consist.add_unit(#capacity=55,  # much bigger is not much better here
                 vehicle_length=6)
