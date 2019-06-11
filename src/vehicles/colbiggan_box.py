from road_vehicle import BoxTramConsist
from base_platforms.trams import ElectricMotorTram4

consist = BoxTramConsist(id='colbiggan_box',
                  base_numeric_id=880,
                  name='Colbiggan',
                  gen=3)

consist.add_unit(base_platform=ElectricMotorTram4,
                 repeat=2)
