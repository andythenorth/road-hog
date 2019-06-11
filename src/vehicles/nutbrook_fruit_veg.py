from road_vehicle import FruitVegTramConsist
from base_platforms.trams import ElectricMotorTram4

consist = FruitVegTramConsist(id='nutbrook_fruit_veg',
                       base_numeric_id=960,
                       name='Nutbrook',
                       gen=3)

consist.add_unit(base_platform=ElectricMotorTram4,
                 repeat=2)
