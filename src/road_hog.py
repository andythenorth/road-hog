import importlib
import os.path

currentdir = os.curdir

import sys

sys.path.append(os.path.join("src"))  # add to the module search path

from functools import cached_property

import global_constants
import utils
from utils import timing

command_line_args = utils.get_command_line_args()

generated_files_path = os.path.join(currentdir, global_constants.generated_files_dir)

from badges.badge import BadgeManager

roster_module_names = [
    "landrace",
    "heqs",
]

class RosterManager(list):
    """
    Sometimes we want to conveniently expose attributes that span active rosters.
    This is a class to manage that, intended for use as a singleton, which can be passed to templates etc.
    Extends default python list, as we also use it when we want a list of active rosters (the instantiated class instance behaves like a list object).
    """

    def add_rosters(self, roster_module_names):
        for roster_module_name in roster_module_names:
            roster_module = importlib.import_module(
                "." + roster_module_name, package="rosters"
            )
            roster = roster_module.main()
            self.append(roster)

        # run after all rosters have been registered
        for roster in self:
            roster.post_init_actions()

    def validate_vehicles(self):
        # has to be explicitly called after all rosters are active, and all vehicles and vehicle units are registered to each roster
        # validation will also populate numeric_id_defender which can be re-used for ID reporting
        # actual validation is delegated to the roster
        self.numeric_id_defender = []
        for roster in self:
            roster.validate_vehicles(self.numeric_id_defender)

    """
    !! copied from Horse - needed?
    def add_buyable_variant_groups(self):
        # has to be explicitly called after all vehicles and vehicle units are registered to each roster
        for roster in self:
            roster.add_buyable_variant_groups()
    """

    @cached_property
    def active_roster(self):
        # special case if we only want the id report, which does not require an active roster
        if command_line_args.grf_name == "id-report-only":
            return None

        for roster in self:
            if roster.grf_name == command_line_args.grf_name:
                return roster
        # roster should always be found by this point, but eh
        raise Exception("RosterManager: no valid roster found for active_roster")

    def get_roster_by_id(self, roster_id):
        for roster in self:
            if roster.id == roster_id:
                return roster
        else:
            raise Exception("RosterManager: no roster found for ", roster_id)

# @timing
def main():
    # exist_ok=True is used for case with parallel make (`make -j 2` or similar), don't fail with error if dir already exists
    os.makedirs(generated_files_path, exist_ok=True)

    # globals within this module, accessible externally as road_hog.foo
    globals()["badge_manager"] = BadgeManager()
    globals()["roster_manager"] = RosterManager()

    roster_manager.add_rosters(roster_module_names)
    roster_manager.validate_vehicles()

    # BadgeManager.produce_badges() must be made a no-op separately.
    #badge_manager.produce_badges(roster_manager=roster_manager)
