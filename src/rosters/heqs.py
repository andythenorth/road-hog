from roster import Roster

from vehicles import witch_hill_dump


def main():
    return Roster(
        id="heqs",
        numeric_id=2,
        grf_name="heqs",
        grfid=r"\41\50\12\03",
        str_grf_name="HEQS",
        # default intro dates per generation, can be over-ridden if needed by setting intro_date kw on consist
        intro_dates={
            "ROAD": [
                1860,
                1920,
                1945,
                1970,
                1995,
                2020,
            ],  # gen 1 is long, then after 1920, quite aggressive 25 year gaps for trucks / buses
            "LOLZ": [1860, 1920, 1945, 1970, 1995, 2020],  # keep matched to ROAD
            "HEQS": [
                1925,
                1945,
                1965,
                1985,
                2015,
                2035,
            ],  # very aggressive 20 year gaps to reflect rapid development + overtake feldbahn
            "RAIL": [1860, 1900, 1930, 1960, 1990, 2020],
        },  # 30 year gaps for trams
        speeds={
            "ROAD": [25, 40, 55, 70, 80, 80],
            "LOLZ": [
                25,
                40,
                55,
                70,
                80,
                80,
            ],  # match to ROAD otherwise LOLZ vehicles cause road blocks
            "HEQS": [25, 30, 40, 50, 60, 60],
            "RAIL": [25, 35, 45, 55, 65, 65],
        },
        power_bands={
            "ROAD": [100, 150, 250, 450, 650, 750],
            "LOLZ": [100, 150, 250, 450, 650, 750],
            "HEQS": [100, 150, 250, 450, 650, 750],  # more likely to be over-ridden eh?
            "RAIL": [240, 480, 720, 960, 1200, 1440],
        },  # tram power is excessive compare to RL, otherwise the OpenTTD physics model spanks the trams
        # note that a few of these will only be used by singleton vehicles
        # but it's convenient to have one and only one standard way to do this (excepting local _capacity over-rides for joker cases)
        # !! might be better to do it per consist, and then divide that over vehicles in capacity(), with allocation of remainders
        unit_capacity_per_vehicle_type={
            "feldbahn": [16, 20, 20],
            "freight_truck": [1, 12, 15, 20, 20, 20],
            "lolz": [1, 2, 3, 4, 5, 6],
        },
        vehicles=[
            witch_hill_dump,
        ],
    )
