from roster import Roster

from vehicles import catchcan

roster = Roster(id = 'heqs',
                numeric_id = 2,
                grf_name="heqs",
                grfid=r"41\50\12\03",
                str_grf_name="HEQS",
                # keep dates for power and speeds matched
                truck_speeds = {0: 25, 1905: 40, 1935: 55, 1965: 70, 1985: 80},
                tram_speeds = {0: 25, 1900: 35, 1930: 45, 1960: 55, 1990: 65},
                truck_power_bands = {0: 100, 1905: 150, 1935: 250, 1965: 450, 1985: 700},
                tram_power_bands = {0: 100, 1900: 200, 1930: 350, 1960: 550, 1990: 800},
                vehicles = [catchcan])
