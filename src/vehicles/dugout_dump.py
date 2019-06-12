from road_vehicle import DumpFeldbahnConsist, ElectricVehicleUnit
from base_platforms.feldbahn import ElectricEngineFeldbahn1, OpenWagonFeldbahnGen3

consist = DumpFeldbahnConsist(id='dugout_dump',
                       base_numeric_id=1010,
                       name='Dugout',
                       gen=3)

consist.add_unit(base_platform=ElectricEngineFeldbahn1)

consist.add_unit(base_platform=OpenWagonFeldbahnGen3,
                 repeat=7)
