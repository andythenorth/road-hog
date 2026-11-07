from collections import Counter
from functools import cached_property
import os
import tomllib

currentdir = os.curdir

import global_constants


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
        self.vehicle_liveries = kwargs.get("vehicle_liveries", {})
        # consists_uninitialised only used once at __init__ time, it's a list of modules, not the actual consists
        # init of consists has to happen in produce_vehicles, otherwise consists can't get the roster
        self.consists_uninitialised = kwargs.get("vehicles")
        self.model_variants = []
        self.model_variants_by_catalogue = {}
        self.variant_groups = None
        self.unit_capacity_per_vehicle_type = kwargs.get(
            "unit_capacity_per_vehicle_type"
        )

    def produce_vehicles(self):
        # init of consists has to happen after the roster is registered with RosterManager, otherwise consists can't get the roster
        from road_vehicle.catalogue import Catalogue

        for vehicle in self.consists_uninitialised:
            for model_def in vehicle.main(roster_id=self.id):
                catalogue = Catalogue(model_def, roster_id=self.id)
                model_variants = [catalogue.produce(entry) for entry in catalogue]
                self.model_variants_by_catalogue[catalogue.model_id] = model_variants
                self.model_variants.extend(model_variants)

    @property
    def model_variants_in_buy_menu_order(self):
        """
        Returns a flat list of VariantGroup instances, depth-first ordered from the nested parent/child structure.
        """
        result = []

        def walk(group: VariantGroup):
            result.extend(group)
            for child in group.child_groups:
                walk(child)

        for group in self.variant_groups.values():
            if group.parent_group is None:
                walk(group)

        return result

    def validate_vehicle_ids(self, numeric_id_defender):
        # has to be explicitly called after all model variants and units are registered to the roster

        # this structure is used to test for duplicate ids
        model_variant_id_counts = Counter(self.model_variants)
        # we defer collisions until they're all found
        collision_errors = []

        for model_variant in self.model_variants:
            """
            # pickled test nerfed off as (1) slow (2) mp_logger is now used, which should improve the error output when pickle does fail
            # if model_variant won't pickle, then multiprocessing blows up, catching it here is faster and easier
            try:
                pickle.dumps(model_variant)
            except:
                print("Pickling failed for model_variant:", model_variant.id)
                raise
            """
            if model_variant_id_counts[model_variant.id] > 1:
                raise BaseException(
                    f"Error: vehicle id '{model_variant.id}' is defined more than once - to fix, search src for the duplicate.\n"
                    f"The catalogue for one of them is:"
                    f"{model_variant.catalogue}"
                )
            if len(model_variant.units) == 0:
                raise BaseException(f"Error: {model_variant.id} has no units defined")
            elif len(model_variant.units) == 1:
                if model_variant.base_numeric_id <= global_constants.max_articulated_id:
                    raise BaseException(
                        f"Error: {model_variant.id} with base_numeric_id {model_variant.base_numeric_id} needs a base_numeric_id larger than 16383 "
                        f"as the range below 16383 is reserved for articulated vehicles.\n"
                        f"{model_variant.units}\n"
                        f"Unused IDs might be found in build_logs/id_report.py.log"
                    )
            elif len(model_variant.units) > 1:
                for numeric_id in model_variant.catalogue_entry.unit_numeric_ids:
                    if numeric_id > global_constants.max_articulated_id:
                        raise BaseException(
                            f"Error: {model_variant.id} has a unit variant with numeric_id {numeric_id} which is part of an articulated vehicle "
                            f"and needs a numeric_id smaller than {global_constants.max_articulated_id}.\n"
                            f"Use a lower base_numeric_id in the model_def.\n"
                            f"{model_variant.catalogue.unit_numeric_ids}"
                            f"Unused IDs might be found in build_logs/id_report.py.log"
                        )
            for numeric_id in model_variant.catalogue_entry.unit_numeric_ids:
                if numeric_id % 10 != 0:
                    continue  # only care about block-starting IDs
                if numeric_id in numeric_id_defender:
                    colliding_model_variant = numeric_id_defender[numeric_id]
                    if hasattr(model_variant, "model_id_root"):
                        if (
                            getattr(colliding_model_variant, "model_id_root", None)
                            == model_variant.model_id_root
                            and colliding_model_variant.roster.id
                            != model_variant.roster.id
                        ):
                            continue
                    # Collect all block-starting IDs (multiples of 10) for both variants
                    this_blocks = sorted(
                        {
                            nid
                            for entry in model_variant.catalogue
                            for nid in entry.unit_numeric_ids
                            if nid % 10 == 0
                        }
                    )
                    other_blocks = sorted(
                        {
                            nid
                            for entry in colliding_model_variant.catalogue
                            for nid in entry.unit_numeric_ids
                            if nid % 10 == 0
                        }
                    )
                    collision_errors.append(
                        {
                            "numeric_id": numeric_id,
                            "model_variant": model_variant.id,
                            "collides_with": colliding_model_variant.id,
                            "this_blocks": this_blocks,
                            "other_blocks": other_blocks,
                        }
                    )
                else:
                    numeric_id_defender[numeric_id] = model_variant

        if collision_errors:
            error_msg = [
                "Vehicle ID collisions detected (only multiple-of-10 IDs shown):"
            ]
            for err in collision_errors:
                error_msg.append(
                    f"{err['model_variant']} and {err['collides_with']} share numeric_id {err['numeric_id']}"
                )
                error_msg.append(f"    {err['model_variant']}: {err['this_blocks']}")
                error_msg.append(f"    {err['collides_with']}: {err['other_blocks']}")
                error_msg.append(f"")  # just a spacer
            error_msg.append(
                f"Unused numeric IDs might be found in build_logs/id_report.py.log"
            )
            raise ValueError("\n".join(error_msg))
        # no return value needed


    def add_variant_groups(self):
        # creating groups has to happen after *all* model variants are inited

        # create the structure to hold the groups, this is set to None when the roster is inited, and should be None when this method is called
        if self.variant_groups is not None:
            raise BaseException(
                "add_variant_groups() called more than once for roster " + self.id
            )

        self.variant_groups = {}

        # for every buyable variant for every model_variant
        # - add a group if it doesn't already exist
        # - add the buyable variant as a member of the group

        for model_variant in self.model_variants:
            variant_group_id = model_variant.catalogue_entry.variant_group_id
            if variant_group_id is None:
                raise ValueError(model_variant.id)
            variant_group = self.variant_groups.setdefault(
                variant_group_id, VariantGroup(id=variant_group_id)
            )
            variant_group.append(model_variant)

        # CABBAGE488: Iron Horse nests primary/secondary wagon-livery groups here.
        # Road Hog currently groups by catalogue model_id, so these suffixes never
        # occur. Retain the relationship handling for parity if grouping evolves.
        # handle nesting of wagon groups by primary and secondary livery options
        for variant_group_id, variant_group in self.variant_groups.items():
            if variant_group_id.endswith("_primary"):
                continue

            # derive the base ID stem (everything before `_static`)
            group_id_stem = variant_group_id.rsplit("_secondary", 1)[0]
            primary_group_id = f"{group_id_stem}_primary"
            primary_group = self.variant_groups.get(primary_group_id, None)
            if (primary_group is not None) and (len(variant_group) > 0):
                variant_group.parent_group = primary_group
                primary_group.child_groups.append(variant_group)


    def get_lang_data(self, lang, context):
        # strings optionally vary per roster, so we have a method to fetch all lang data via the roster
        global_pragma = {}
        lang_strings = {}
        docs_only_strings = {}
        # we have the option to suppress selected strings in specific contexts, using a dedicated suppression file
        suppressed_strings = tomllib.load(
            open(
                os.path.join(currentdir, "src", "lang", "suppressed_strings.toml"), "rb"
            )
        )

        with open(os.path.join(currentdir, "src", "lang", lang + ".toml"), "rb") as fp:
            lang_source = tomllib.load(fp)

        for node_name, node_value in lang_source.items():
            # first check if the string is suppressed in this roster, when building grf only (not docs)
            if context == "grf" and node_name in suppressed_strings:
                if self.id in suppressed_strings[node_name].get(
                    "suppressed_rosters", []
                ):
                    continue

            if node_name == "GLOBAL_PRAGMA":
                # explicit handling of global pragma items
                global_pragma["grflangid"] = node_value["grflangid"]
                global_pragma["plural"] = node_value["plural"]
                if node_value.get("gender", False):
                    global_pragma["gender"] = node_value["gender"]
                if node_value.get("case", False):
                    global_pragma["case"] = node_value["case"]
            else:
                # ach conditional jank for docs only strings, but JFDI
                if node_value.get("docs_only", False) == True:
                    docs_only_strings[node_name] = node_value["base"]
                else:
                    # all lang strings should provide a default base value, which can optionally be over-ridden per roster
                    if self.id in node_value.keys():
                        lang_strings[node_name] = node_value[self.id]
                    else:
                        lang_strings[node_name] = node_value["base"]

        for model_variants in self.model_variants_by_catalogue.values():
            example_model_variant = model_variants[0]
            if example_model_variant.model_def.name is not None:
                lang_strings["STR_NAME_" + example_model_variant.catalogue.model_id.upper()] = (
                    example_model_variant.model_def.name
                )

        return {
            "global_pragma": global_pragma,
            "lang_strings": lang_strings,
            "docs_only_strings": docs_only_strings,
        }



class VariantGroup(list):
    """
    Simple class to manage providing the variant_group nml property.
    List members are model_variant instances.
    Extends default python list, as it's a convenient behaviour (the instantiated class instance behaves like a list object).
    """

    def __init__(self, id):
        self.id = id
        self.parent_group = None
        self.child_groups = []

    def get_variant_group_prop_for_model_variant(self, model_variant):
        # faff to find the group leader (typically the first variant)
        leader = self[0]
        if self.parent_group is not None:
            if model_variant == self[0]:
                leader = self.parent_group[0]

        # guard - don't assign a group reference to the leader itself
        if leader == model_variant:
            return None

        # for nml, we want the id of the first unit
        return leader.units[0].id

    @cached_property
    def group_level(self):
        level = 0
        context = self
        while context.parent_group is not None:
            level += 1
            context = context.parent_group
        return level
