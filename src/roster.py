from rosters import registered_rosters
import pickle
import utils

class Roster(object):
    """
    Rosters compose a set of consists (vehicles) which is complete for gameplay.
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.numeric_id = kwargs.get('numeric_id')
        self.intro_dates = kwargs.get('intro_dates')
        self.speeds = kwargs.get('speeds')
        # default power, determined by intro date; can be over-ridden per vehicle when needed
        self.default_truck_power_bands = kwargs.get('truck_power_bands')
        self.default_tram_power_bands = kwargs.get('tram_power_bands')
        self.consists = []
        for vehicle in kwargs.get('vehicles'):
            consist = vehicle.consist
            consist.roster_id = self.id
            self.consists.append(consist)

    @property
    def buy_menu_sort_order(self):
        return [consist.id for consist in self.consists]

    @property
    def consists_in_buy_menu_order(self):
        result = []
        result.extend(self.consists)
        for consist in result:
            # if consist won't pickle, then multiprocessing blows up, catching it here is faster and easier
            try:
                pickle.dumps(consist)
            except:
                utils.echo_message("Pickling failed for consist: " + consist.id)
                raise
        return result

    def register(roster):
        registered_rosters.append(roster)
