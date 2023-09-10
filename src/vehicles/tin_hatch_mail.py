from road_vehicle import MailTramConsist, SteamVehicleUnit


def main(roster_id):
    consist = MailTramConsist(
        roster_id=roster_id,
        id="tin_hatch_mail",
        base_numeric_id=820,
        name="Tin Hatch",
        power=120,  # custom power
        gen=1,
    )

    consist.add_unit(
        base_platform=None,  # mail trams have no base platform by design currently
        type=SteamVehicleUnit,
        capacity=0,
        vehicle_length=3,
        effects=["EFFECT_SPRITE_STEAM, -3, 0, 12"],
        always_use_same_spriterow=True,
    )

    consist.add_unit(
        base_platform=None, vehicle_length=5  # no base platform by design currently
    )

    return consist
