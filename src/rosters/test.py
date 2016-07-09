from roster import Roster

from vehicles import (honister,
                      wookey,
                      cloud_hill,
                      nettlebridge,
                      scrooby_top,
                      chainburn,
                      stakebeck,
                      big_rigg,
                      windergill,
                      capo,
                      towerhouse)

roster = Roster(id = 'brit',
                numeric_id = 1,
                # keep dates for power and speeds matched
                truck_speeds = {0: 25, 1905: 40, 1935: 55, 1965: 70, 1985: 80},
                tram_speeds = {0: 25, 1900: 35, 1930: 45, 1960: 55, 1990: 65},
                truck_power_bands = {0: 100, 1905: 150, 1935: 250, 1965: 450, 1985: 700},
                tram_power_bands = {0: 100, 1900: 200, 1930: 350, 1960: 550, 1990: 800},
                vehicles = [honister,
                            wookey,
                            capo,
                            cloud_hill,
                            nettlebridge,
                            scrooby_top,
                            chainburn,
                            big_rigg,
                            windergill,
                            stakebeck,
                            towerhouse])
