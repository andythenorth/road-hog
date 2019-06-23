from road_vehicle import FlatbedTramConsist
from base_platforms.trams import ElectricMotorTram4

consist = FlatbedTramConsist(id='stancliffe_flat',
                      base_numeric_id=410,
                      name='Stancliffe',
                      gen=3)

consist.add_unit(base_platform=ElectricMotorTram4,
                 repeat=2)
