import os.path

currentdir = os.curdir

import sys

sys.path.append(os.path.join("src"))  # add to the module search path

import global_constants
import utils

command_line_args = utils.get_command_line_args()

generated_files_path = os.path.join(currentdir, global_constants.generated_files_dir)
# exist_ok=True is used for case with parallel make (`make -j 2` or similar), don't fail with error if dir already exists
os.makedirs(generated_files_path, exist_ok=True)

# import rosters
from rosters import landrace
from rosters import heqs


class RosterManager(list):
    """
    Sometimes we want to conveniently expose attributes that span active rosters.
    This is a class to manage that, intended for use as a singleton, which can be passed to templates etc.
    Extends default python list, as we also use it when we want a list of active rosters (the instantiated class instance behaves like a list object).
    """

    def add_roster(self, roster_module):
        roster = roster_module.main()
        self.append(roster)
        # some actions have to be run after the register is added to RosterManager
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

    @property
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


# declared outside of main, got bored trying to figure out how to otherwise put it in the module scope
roster_manager = RosterManager()


def main():
    # rosters
    # in the rare case that an unfinished roster won't init cleanly, comment it out here and possibly also in the import
    # built-in support for disabled rosters was removed during the conversion to multi-grf, it was an unnecessary abstraction when only one roster is used per grf
    roster_manager.add_roster(landrace)
    roster_manager.add_roster(heqs)

    roster_manager.validate_vehicles()
