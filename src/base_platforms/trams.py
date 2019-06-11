from base_platform import BasePlatform
from road_vehicle import DieselVehicleUnit, SteamVehicleUnit


class EngineTramBase(BasePlatform):
    capacity = 0
    always_use_same_spriterow = True


# engines

class SteamEngineTram1(EngineTramBase):
    type = SteamVehicleUnit
    vehicle_length = 4


class SteamEngineTram2(EngineTramBase):
    type = SteamVehicleUnit
    vehicle_length = 4
