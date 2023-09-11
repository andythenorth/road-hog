# JFDI module to help do some doc formatting

import global_constants
import utils


class DocHelper(object):
    # Some constants
    palette = utils.dos_palette_to_rgb()

    # these only used in docs as of April 2018
    docs_sprite_max_width = (
        65  # up to 2 units eh + 1 extra pixel to accomodate couplers on trams
    )
    docs_sprite_height = 16

    def __init__(self, lang_strings):
        self.lang_strings = lang_strings

    def docs_sprite_width(self, consist):
        # !! might want to add 1 here if trams get extra 1px for couplings, but eh, we'll see
        return min((consist.buy_menu_width), self.docs_sprite_max_width)

    def get_vehicles_by_subclass(self, consists):
        vehicles_by_subclass = {}
        for consist in consists:
            subclass = type(consist)
            if subclass in vehicles_by_subclass:
                vehicles_by_subclass[subclass].append(consist)
            else:
                vehicles_by_subclass[subclass] = [consist]
        return vehicles_by_subclass

    def fetch_prop(self, result, prop_name, value):
        result["vehicle"][prop_name] = value
        result["subclass_props"].append(prop_name)
        return result

    def get_props_to_print_in_code_reference(self, subclass, consists):
        props_to_print = {}
        for vehicle in self.get_vehicles_by_subclass(consists)[subclass]:
            result = {"vehicle": {}, "subclass_props": []}
            result = self.fetch_prop(
                result, "Vehicle Name", self.unpack_name_string(vehicle)["full_name"]
            )
            result = self.fetch_prop(result, "HP", int(vehicle.power))
            result = self.fetch_prop(result, "Speed (mph)", vehicle.speed)
            result = self.fetch_prop(
                result, "Weight (t)", int(vehicle.weight)
            )  # cast to int to get same result as game will show
            result = self.fetch_prop(result, "Intro Date", vehicle.intro_date)
            result = self.fetch_prop(result, "Vehicle Life", vehicle.vehicle_life)
            result = self.fetch_prop(result, "Capacity", vehicle.total_capacity)
            result = self.fetch_prop(
                result, "Buy Cost Factor", round(vehicle.buy_cost, 2)
            )
            result = self.fetch_prop(
                result, "Running Cost Factor", round(vehicle.running_cost, 2)
            )
            # result = self.fetch_prop(result, 'Loading Speed', vehicle.loading_speed)
            props_to_print[vehicle] = result["vehicle"]
            props_to_print[subclass] = result["subclass_props"]

        return props_to_print

    def unpack_name_string(self, consist):
        substrings = consist.name.split("string(")
        name = consist._name
        type_suffix = self.lang_strings[substrings[3][0:-3]]
        power_suffix = self.lang_strings[substrings[4][0:-2]]
        return {
            "full_name": name + " " + type_suffix + " (" + power_suffix + ")",
            "name": name,
            "type_suffix": type_suffix,
            "power_suffix": power_suffix,
        }

    def get_base_numeric_id(self, consist):
        return consist.base_numeric_id

    def get_active_nav(self, doc_name, nav_link):
        return ("", "active")[doc_name == nav_link]

    def get_special_features_for_vehicle(self, consist):
        result = []
        if consist.loading_speed_multiplier > 1:
            result.append(
                "faster loading"
            )  # assumes we never do slower loading penalty
        if consist.cargo_age_period > global_constants.CARGO_AGE_PERIOD:
            result.append(
                "improved payment"
            )  # assumes we never do higher cargo decay penalty
        return result

    def get_base_track_types(self, consists):
        result = []
        for consist in consists:
            result.append(consist.base_track_type_name)
        return sorted(set(result))

    def remap_company_colours(self, remap):
        result = {}
        input_colours = {"CC1": 198, "CC2": 80}
        for input_colour, output_colour in remap.items():
            for i in range(0, 8):
                result[
                    input_colours[input_colour] + i
                ] = self.get_palette_index_for_company_colour(output_colour, i)
        return result

    def get_palette_index_for_company_colour(self, company_colour, offset):
        return global_constants.company_colour_maps[company_colour][offset]
