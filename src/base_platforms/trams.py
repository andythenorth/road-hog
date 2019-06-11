from base_platform import BasePlatform
from road_vehicle import DieselVehicleUnit, ElectricVehicleUnit, SteamVehicleUnit


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


# motors (body with cabs at both end)

class ElectricMotorTram1(EngineTramBase):
    type = ElectricVehicleUnit
    vehicle_length = 8


class ElectricMotorTram2(EngineTramBase):
    type = ElectricVehicleUnit
    vehicle_length = 8
    cargo_length = 3


class ElectricMotorTram3(EngineTramBase):
    type = ElectricVehicleUnit
    vehicle_length = 8
    cargo_length = 3


class ElectricMotorTram4(EngineTramBase):
    type = ElectricVehicleUnit
    vehicle_length = 8
    cargo_length = 3
