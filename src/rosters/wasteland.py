from roster import Roster

from vehicles import wastelander

roster = Roster(id = 'wasteland',
                truck_speeds = {0: 20, 1900: 25, 1920: 40, 1940: 55, 1960: 70, 1980: 80},
                tram_speeds = {0: 20, 1895: 35, 1940: 50, 1980: 65},
                vehicles = [wastelander])
