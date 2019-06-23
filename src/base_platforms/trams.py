from base_platform import BasePlatform
from road_vehicle import ElectricVehicleUnit, SteamVehicleUnit


class EngineTramBase(BasePlatform):
    # an engine, with no cargo capacity or cargo sprites
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

class ElectricMotorTram1(BasePlatform):
    type = ElectricVehicleUnit
    vehicle_length = 8


class ElectricMotorTram2(BasePlatform):
    type = ElectricVehicleUnit
    vehicle_length = 8
    cargo_length = 3


class ElectricMotorTram3(BasePlatform):
    type = ElectricVehicleUnit
    vehicle_length = 8
    cargo_length = 3


class ElectricMotorTram4(BasePlatform):
    type = ElectricVehicleUnit
    vehicle_length = 8
    cargo_length = 3
