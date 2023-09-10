import copy
import os
import pickle
import tomllib
currentdir = os.curdir

import global_constants
from rosters import registered_rosters
import utils

class Roster(object):
    """
    Rosters compose a set of consists (vehicles) which is complete for gameplay.
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.numeric_id = kwargs.get('numeric_id')
        self.grf_name = kwargs.get("grf_name")
        self.grfid = kwargs.get("grfid")
        self.str_grf_name = kwargs.get("str_grf_name")
        self.intro_dates = kwargs.get('intro_dates')
        self.speeds = kwargs.get('speeds')
        self.power_bands = kwargs.get('power_bands')
        self.consists = []
        self.unit_capacity_per_vehicle_type = kwargs.get('unit_capacity_per_vehicle_type')

        for vehicle in kwargs.get('vehicles'):
            consist = vehicle.main(self.id)
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

    def get_lang_data(self, lang):
        # strings optionally vary per roster, so we have a method to fetch all lang data via the roster
        global_pragma = {}
        lang_strings = {}
        with open(os.path.join(currentdir, "src", "lang", lang + ".toml"), "rb") as fp:
            lang_source = tomllib.load(fp)

        for node_name, node_value in lang_source.items():
            if node_name == "GLOBAL_PRAGMA":
                # explicit handling of global pragma items
                global_pragma["grflangid"] = node_value["grflangid"]
                global_pragma["plural"] = node_value["plural"]
                if node_value.get("gender", False):
                    global_pragma["gender"] = node_value["gender"]
                if node_value.get("case", False):
                    global_pragma["case"] = node_value["case"]
            else:
                # all lang strings should provide a default base value, which can optionally be over-ridden per roster
                if self.id in node_value.keys():
                    lang_strings[node_name] = node_value[self.id]
                else:
                    lang_strings[node_name] = node_value["base"]

        for consist in self.consists_in_buy_menu_order:
            if consist._name is not None:
                lang_strings["STR_NAME_" + consist.id.upper()] = consist._name

        return {"global_pragma": global_pragma, "lang_strings": lang_strings}

    def register(roster):
        registered_rosters.append(roster)
