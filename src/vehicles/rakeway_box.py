from road_vehicle import BoxTramConsist
from base_platforms.trams import ElectricMotorTram3

consist = BoxTramConsist(id='rakeway_box',
                  base_numeric_id=870,
                  name='Rakeway',
                  gen=2)

consist.add_unit(base_platform=ElectricMotorTram3,
                 repeat=2)
