from road_vehicle import CoveredHopperTramConsist
from base_platforms.trams import ElectricMotorTram4

consist = CoveredHopperTramConsist(id='thurlbear_covered_hopper',
                            base_numeric_id=460,
                            name='Thurlbear',
                            gen=3)

consist.add_unit(base_platform=ElectricMotorTram4,
                 repeat=2)
