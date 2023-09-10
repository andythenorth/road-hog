from road_vehicle import LogHEQSConsist, DieselVehicleUnit

consist = LogHEQSConsist(
    id="knockdown_log",
    base_numeric_id=250,
    name="Knockdown",
    power=250,  # custom power
    speed=50,
    gen=3,
)

consist.add_unit(
    base_platform=None,  # no base platform by design currently
    type=DieselVehicleUnit,
    vehicle_length=7,
)

consist.add_unit(
    base_platform=None, vehicle_length=6  # no base platform by design currently
)
