#!/usr/bin/env python3
"""Insert CABBAGE352 livery parity markers; comments only, no runtime changes."""
from pathlib import Path

PATCHES = {'src/road_vehicle/model_def.py': ('    additional_liveries: List[Any] = None', '    # CABBAGE352: model and template livery provision / overrides need parity review.\n'), 'src/road_vehicle/schemas.py': ('class RoadVehicleBase:', '# CABBAGE352: schema livery defaults and inheritance need parity review.\n'), 'src/road_vehicle/livery.py': ('class LiverySupplier(dict):', '# CABBAGE352: shared and roster livery registration is not yet wired.\n'), 'src/road_vehicle/catalogue.py': ('    def livery_defs(self):', '        # CABBAGE352: verify group, inheritance and sprite-row resolution against Iron Horse.\n'), 'src/roster.py': ('        self.model_variants_by_catalogue = {}', '        # CABBAGE352: roster livery dictionaries and groups are not yet provisioned.\n'), 'src/road_hog.py': ('    def add_roster(self, roster_module):', '        # CABBAGE352: register roster liveries before catalogue production.\n'), 'src/rosters/landrace.py': ('from roster import Roster', '# CABBAGE352: provision roster-specific liveries and named groups here.\n'), 'src/rosters/heqs.py': ('from roster import Roster', '# CABBAGE352: provision roster-specific liveries and named groups here.\n'), 'src/global_constants.py': ('company_colour_maps = polar_fox.constants.company_colour_maps', '# CABBAGE352: runtime custom colour maps, colour sets and complements not yet provided.\n'), 'src/render_nml.py': ('def render_header_item_nml(header_item, roster, consists, graphics_path):', '# CABBAGE352: pass runtime livery and custom-colour providers to NML templates.\n'), 'src/gestalt_graphics/gestalt_graphics.py': ('    def buy_menu_row_map(self, pipeline):', '        # CABBAGE352: livery-specific sprite rows and purchase presentation undecided.\n'), 'src/templates/properties.pynml': ('    graphics {', '        // CABBAGE352: runtime colour_mapping and purchase_colour_mapping callbacks absent.\n'), 'src/templates/vehicle_default.pynml': ('spriteset(${unit.id}_ss,', '// CABBAGE352: livery-specific sprite-row selection not yet defined.\n'), 'src/templates/graphics_switches.pynml': ('// buy menu graphics', '// CABBAGE352: livery-specific purchase graphics and swatches not yet defined.\n'), 'src/templates/model_variant_entry_point.pynml': ('    <!--! Graphics chains - conditional on gestalt graphics -->', '    <!--! CABBAGE352: livery-aware graphics routing not yet defined. -->\n')}
root = Path("src")
updates = {}
for path, (anchor, comment) in PATCHES.items():
    target = Path(path)
    original = target.read_text()
    if "CABBAGE352" in original:
        raise RuntimeError(f"{target}: CABBAGE352 already present; no changes made")
    if original.count(anchor) != 1:
        raise RuntimeError(f"{target}: expected one anchor {anchor!r}; no changes made")
    # Place the marker before the anchor; indent is already in comment.
    updated = original.replace(anchor, comment + anchor, 1)
    updates[target] = updated
for target, updated in updates.items():
    target.write_text(updated)
print(f"Inserted CABBAGE352 markers in {len(updates)} files")
