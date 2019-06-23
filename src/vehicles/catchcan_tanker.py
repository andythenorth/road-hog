from road_vehicle import TankerTramConsist
from base_platforms.trams import ElectricMotorTram3

consist = TankerTramConsist(id='catchcan_tanker',
                     base_numeric_id=810,
                     name='Catchcan',
                     gen=2,
                     intro_date_offset=2)  # introduce later than gen epoch by design

consist.add_unit(base_platform=ElectricMotorTram3,
                 repeat=2)
