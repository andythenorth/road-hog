from road_vehicle import EdiblesTankerTramConsist
from base_platforms.trams import ElectricMotorTram4

consist = EdiblesTankerTramConsist(id='bottlebrook_edibles_tanker',
                            base_numeric_id=510,
                            name='Bottlebrook',
                            gen=3,
                            intro_date_offset=6)  # introduce later than gen epoch by design

consist.add_unit(base_platform=ElectricMotorTram4,
                 repeat=2)
