from road_vehicle import LivestockTramConsist
from base_platforms.trams import ElectricMotorTram1

consist = LivestockTramConsist(id='trotalong_livestock',
                        base_numeric_id=720,
                        name='Trotalong',
                        gen=2,
                        intro_date_offset=1)  # introduce later than gen epoch by design

consist.add_unit(base_platform=ElectricMotorTram1,
                 repeat=2)
