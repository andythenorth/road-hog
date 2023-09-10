from road_vehicle import DumpTramConsist, ElectricVehicleUnit


def main(roster_id):
    consist = DumpTramConsist(
        roster_id=roster_id,
        id="nettlebridge_dump",
        base_numeric_id=310,
        name="Nettlebridge",
        gen=3,
        intro_date_offset=4,
    )  # introduce later than gen epoch by design

    consist.add_unit(
        base_platform=None,  # no base platform by design currently
        type=ElectricVehicleUnit,
        capacity=0,
        vehicle_length=4,
        always_use_same_spriterow=True,
    )

    consist.add_unit(
        base_platform=None,  # no base platform by design currently
        vehicle_length=6,
        repeat=2,
    )

    return consist
