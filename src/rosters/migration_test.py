"""Isolated one-vehicle roster for the Road Hog framework migration.

Register this module manually in road_hog.py and disable production rosters.
The vehicle deliberately reuses Leyburn's existing identifier and sprites.
"""

from roster import Roster
from vehicles import migration_test_bus


def main():
    return Roster(
        id="migration_test",
        numeric_id=1,
        grf_name="migration_test",
        grfid=r"\97\87\EA\FF",
        str_grf_name="Migration Test",
        intro_dates={
            "ROAD": [1860, 1920, 1945, 1970, 1995, 2020],
            "LOLZ": [1860, 1920, 1945, 1970, 1995, 2020],
            "HEQS": [1925, 1945, 1965, 1985, 2015, 2035],
            "RAIL": [1860, 1900, 1930, 1960, 1990, 2020],
        },
        speeds={
            "ROAD": [25, 40, 55, 70, 80, 80],
            "LOLZ": [25, 40, 55, 70, 80, 80],
            "HEQS": [25, 30, 40, 50, 60, 60],
            "RAIL": [25, 35, 45, 55, 65, 65],
        },
        power_bands={
            "ROAD": [100, 150, 250, 450, 650, 750],
            "LOLZ": [100, 150, 250, 450, 650, 750],
            "HEQS": [100, 150, 250, 450, 650, 750],
            "RAIL": [240, 480, 720, 960, 1200, 1440],
        },
        unit_capacity_per_vehicle_type={
            "bus": [1, 44, 50, 60, 72],
            "coach": [1, 2, 30, 40, 40],
            "feldbahn": [16, 20, 20],
            "freight_tram": [16, 30, 36],
            "freight_truck": [1, 12, 15, 20, 20, 20],
            "lolz": [1, 2, 3, 4, 5, 6],
            "mail_tram": [24, 15, 18, 36, 36],
            "mail_truck": [1, 12, 15, 25, 25],
            "pax_tram": [20, 27, 50, 60, 70],
        },
        vehicles=[migration_test_bus],
    )
