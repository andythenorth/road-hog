from road_vehicle import DumpTramConsist
from base_platforms.trams import ElectricMotorTram3

consist = DumpTramConsist(id='hawkmoor_dump',
                   base_numeric_id=760,
                   name='Hawkmoor',
                   gen=2,
                   intro_date_offset=2)  # introduce later than gen epoch by design

consist.add_unit(base_platform=ElectricMotorTram3,
                 repeat=2)
