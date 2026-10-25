"""Give the new model schema the bits docs needs. Keep this small."""
from _common import ROOT, replace_once

path = ROOT / 'src/road_vehicle/schemas.py'
old = '''    @property
    def roster(self):
        return road_hog.roster_manager.get_roster_by_id(self.roster_id)
'''
new = '''    # Docs use an intro year for the sort and the page date range.
    # CABBAGE Old Road Hog returned 999 here as a shim. Use the real year now;
    # check the docs ordering again when we move vehicles with exact intro dates.
    @property
    def intro_year(self):
        return self.intro_date

    @property
    def roster(self):
        return road_hog.roster_manager.get_roster_by_id(self.roster_id)
'''
replace_once(path, old, new)
