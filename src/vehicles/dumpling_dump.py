from road_vehicle import DumpFeldbahnConsist, ElectricVehicleUnit
from base_platforms.feldbahn import ElectricEngineFeldbahn1, OpenWagonFeldbahnGen3

consist = DumpFeldbahnConsist(id='dumpling_dump',
                       base_numeric_id=980,
                       name='Dumpling',
                       gen=3)

consist.add_unit(base_platform=ElectricEngineFeldbahn1)

consist.add_unit(base_platform=OpenWagonFeldbahnGen3,
                 repeat=7)
