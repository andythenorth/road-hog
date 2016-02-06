from rosters import registered_rosters
import pickle

class Roster(object):
    """
    Rosters compose a set of vehicles which is complete for gameplay.
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.numeric_id = kwargs.get('numeric_id')
        # default speeds, determined by intro date; can be over-ridden per vehicle when needed
        self.default_truck_speeds = kwargs.get('truck_speeds')
        self.default_tram_speeds = kwargs.get('tram_speeds')
        # default power, determined by intro date; can be over-ridden per vehicle when needed
        self.default_truck_power_bands = kwargs.get('truck_power_bands')
        self.default_tram_power_bands = kwargs.get('tram_power_bands')
        self.vehicles = []
        for vehicle in kwargs.get('vehicles'):
            self.vehicles.append(vehicle.consist)
            vehicle.consist.roster_id = self.id

    @property
    def buy_menu_sort_order(self):
        return [consist.id for consist in self.vehicles]

    @property
    def consists_in_buy_menu_order(self):
        result = []
        result.extend(self.vehicles)
        for consist in result:
            # if consist won't pickle, then multiprocessing blows up, catching it here is faster and easier
            try:
                pickle.dumps(consist)
            except:
                print("Pickling failed for consist:", consist.id)
                raise
        return result

    def register(roster):
        registered_rosters.append(roster)
