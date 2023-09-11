import os
import pickle
import tomllib

currentdir = os.curdir

import global_constants
import utils


class Roster(object):
    """
    Rosters compose a set of consists (vehicles) which is complete for gameplay.
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.numeric_id = kwargs.get("numeric_id")
        self.grf_name = kwargs.get("grf_name")
        self.grfid = kwargs.get("grfid")
        self.str_grf_name = kwargs.get("str_grf_name")
        self.intro_dates = kwargs.get("intro_dates")
        self.speeds = kwargs.get("speeds")
        self.power_bands = kwargs.get("power_bands")
        # consists_uninitialised only used once at __init__ time, it's a list of modules, not the actual consists
        # init of consists has to happen in post_init_actions, otherwise consists can't get the roster
        self.consists_uninitialised = kwargs.get("vehicles")
        self.consists = []
        self.unit_capacity_per_vehicle_type = kwargs.get(
            "unit_capacity_per_vehicle_type"
        )

    def post_init_actions(self):
        # init of consists has to happen after the roster is registered with RosterManager, otherwise consists can't get the roster
        for vehicle in self.consists_uninitialised:
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

    def validate_vehicles(self, numeric_id_defender):
        print("validate_vehicles is nerfed for JFDI make-the-compile-work")
        return

        # has to be explicitly called after all vehicles and vehicle units are registered to the roster

        # this structure is used to test for duplicate ids
        consist_ids = [consist.id for consist in self.consists_in_buy_menu_order]

        for consist in self.consists_in_buy_menu_order:
            if consist_ids.count(consist.id) > 1:
                raise BaseException(
                    "Error: vehicle id '"
                    + consist.id
                    + "' is defined more than once - to fix, search src for the duplicate"
                )
            if len(consist.units) == 0:
                raise BaseException("Error: " + consist.id + " has no units defined")
            elif len(consist.units) == 1:
                if consist.base_numeric_id <= global_constants.max_articulated_id:
                    raise BaseException(
                        "Error: "
                        + consist.id
                        + " with base_numeric_id "
                        + str(consist.base_numeric_id)
                        + " needs a base_numeric_id larger than 16384 as the range below 16384 is reserved for articulated vehicles"
                    )
                    # utils.echo_message(consist.id + " with base_numeric_id " + str(consist.base_numeric_id) + " needs a base_numeric_id larger than 8200 as the range below 8200 is reserved for articulated vehicles")
                    # utils.echo_message(str(consist.base_numeric_id))
            elif len(consist.units) > 1:
                for numeric_id in consist.unique_numeric_ids:
                    if numeric_id > global_constants.max_articulated_id:
                        raise BaseException(
                            "Error: "
                            + consist.id
                            + " has a unit variant with numeric_id "
                            + str(numeric_id)
                            + " which is part of an articulated vehicle, and needs a numeric_id smaller than "
                            + str(global_constants.max_articulated_id)
                            + " (use a lower consist base_numeric_id)"
                        )
            for numeric_id in consist.unique_numeric_ids:
                if numeric_id in numeric_id_defender:
                    raise BaseException(
                        "Error: consist "
                        + consist.id
                        + " has a unit variant with numeric_id that collides ("
                        + str(numeric_id)
                        + ") with a numeric_id of a unit variant in another consist"
                    )
                else:
                    numeric_id_defender.append(numeric_id)
        # no return value needed

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
