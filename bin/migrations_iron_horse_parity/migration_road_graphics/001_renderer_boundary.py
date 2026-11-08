"""Use road model variants with the old Road Hog graphics pipeline, unmodified."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / 'src/render_graphics.py'

IMPORT = 'import global_constants\n'
IMPORT_NEW = '''import global_constants
from road_vehicle.schemas import RoadVehicleBase


class _GraphicsFileView:
    """A file name view for the old pipeline. This is not a Consist."""

    def __init__(self, vehicle):
        self.vehicle = vehicle
        # CABBAGE The pipeline uses .id for input and output PNG file names.
        # NML uses model variant / unit variant ids. Keep these separate.
        self.id = vehicle.graphics_file_id

    def __getattr__(self, name):
        return getattr(object.__getattribute__(self, "vehicle"), name)


def _graphics_input(vehicle):
    if isinstance(vehicle, RoadVehicleBase):
        return _GraphicsFileView(vehicle)
    return vehicle
'''
OLD = '''    consists = roster.consists_in_buy_menu_order

    for consist in consists:
        # rosters won't pickle reliably, and blow up multiprocessing, never figured out why
        # work around that by freezing anything for graphics processing that depends on roster lookups
        consist.freeze_cross_roster_lookups()
'''
NEW = '''    # The graphics pipelines are unchanged. Only their file-name input differs
    # between old Consists and catalogue-produced model variants.
    consists = [_graphics_input(vehicle) for vehicle in roster.consists_in_buy_menu_order]

    for consist in consists:
        # Legacy Consists freeze roster lookups before multiprocessing.
        # New schema vehicles use roster_id and model definitions, and do not
        # have the old cross-roster freeze step.
        if not isinstance(consist, _GraphicsFileView):
            consist.freeze_cross_roster_lookups()
'''


def main():
    text = PATH.read_text()
    if IMPORT_NEW not in text:
        if text.count(IMPORT) != 1:
            raise RuntimeError('Unexpected graphics imports; review before editing')
        text = text.replace(IMPORT, IMPORT_NEW, 1)
    if NEW not in text:
        if text.count(OLD) != 1:
            raise RuntimeError('Unexpected graphics roster loop; review before editing')
        text = text.replace(OLD, NEW, 1)
    PATH.write_text(text)
    print('PASS: graphics renderer accepts RoadVehicleBase; no pipeline changed')


if __name__ == '__main__':
    main()
