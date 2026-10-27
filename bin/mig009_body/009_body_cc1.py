from pathlib import Path
import re

ROOT = Path.cwd()
G = ROOT / 'src/gestalt_graphics/gestalt_graphics.py'
S = ROOT / 'src/road_vehicle/schemas.py'
T = ROOT / 'src/templates/vehicle_with_simple_body_colour_remaps_road.pynml'
E = ROOT / 'src/templates/model_variant_entry_point.pynml'
LEGACY = ROOT / 'src/templates/vehicle_with_cargo_specific_liveries.pynml'

for path in (G,S,T,E):
    if not path.is_file():
        raise RuntimeError(f'missing {path}; run from repository root with step 008f applied')

old_g = G.read_text()
new_g = old_g
start = new_g.find('class GestaltGraphicsLiveryOnly(GestaltGraphics):')
end = new_g.find('class GestaltGraphicsCustom(GestaltGraphics):', start)
if start >= 0:
    if end < 0: raise RuntimeError('cannot locate end of deprecated gestalt class')
    new_g = new_g[:start] + new_g[end:]

old_class = '''class GestaltGraphicsSimpleBodyColourRemaps(GestaltGraphics):
    # CABBAGE352: IH-named graphics interface for RH's existing CC1/CC2 sprite sheets.
    # No extra processing pipeline; runtime remaps are provided by NML callbacks.

    @property
    def nml_template(self):
        return "vehicle_with_simple_body_colour_remaps_road.pynml"
'''
new_class = '''class GestaltGraphicsSimpleBodyColourRemaps(GestaltGraphics):
    # CC-ready sprites need no processing. False-colour freight bodies need
    # one unweathered CC1 output row, using the existing compositor.
    def __init__(self, body_recolour_map=None):
        super().__init__()
        self.body_recolour_map = body_recolour_map
        if body_recolour_map is not None:
            self.pipelines = pipelines.get_pipelines(
                ["extend_spriterows_for_composited_sprites_pipeline"]
            )
            # CABBAGE352: compositor still calls this row type 'livery_only'.
            # One CC1 row only; no cargo-specific or weathered variants.
            self.recolour_maps = [("DFLT", body_recolour_map)]

    def get_output_row_types(self):
        if self.body_recolour_map is not None:
            return ["livery_only"]
        return super().get_output_row_types()

    @property
    def nml_template(self):
        return "vehicle_with_simple_body_colour_remaps_road.pynml"
'''
if old_class in new_g:
    new_g = new_g.replace(old_class, new_class)
elif new_class not in new_g:
    raise RuntimeError('unexpected body recolour GestaltGraphics class')

old_s = S.read_text()
new_s = old_s
# All six legacy allocations, with arbitrary whitespace in arguments, selected by constructor.
pat = re.compile(r'GestaltGraphicsLiveryOnly\(\s*recolour_maps\s*=\s*(?:polar_fox\.constants\.tanker_livery_recolour_maps|graphics_constants\.livestock_livery_recolour_maps)\s*\)', re.M)
new_s, count = pat.subn('GestaltGraphicsSimpleBodyColourRemaps(\n            body_recolour_map=graphics_constants.body_recolour_CC1\n        )', new_s)
if count not in (0,6): raise RuntimeError(f'found {count} legacy allocations, expected 6')
if count == 0 and 'GestaltGraphicsLiveryOnly' in new_s: raise RuntimeError('unexpected legacy allocation')
new_s = new_s.replace('    GestaltGraphicsLiveryOnly,\n', '')
if 'from gestalt_graphics import graphics_constants' not in new_s:
    marker='from gestalt_graphics.gestalt_graphics import ('
    if marker not in new_s: raise RuntimeError('cannot place graphics_constants import')
    new_s = new_s.replace(marker, 'from gestalt_graphics import graphics_constants\n'+marker, 1)

old_t = T.read_text()
new_t = old_t
needle = '${list(global_constants.freight_wagon_liveries).index(model_variant.livery_def.livery_name)}'
needle_purchase = '${len(global_constants.freight_wagon_liveries) + list(global_constants.freight_wagon_liveries).index(model_variant.livery_def.livery_name)}'
if "<tal:default_livery condition=" in new_t:
    pass
elif needle in new_t and needle_purchase in new_t:
    new_t = new_t.replace('<!--! CABBAGE352 008d:', '<tal:catalogue_livery condition="model_variant.livery_def.livery_name in global_constants.freight_wagon_liveries">\n<!--! CABBAGE352 008d:',1)
    new_t += '''\n</tal:catalogue_livery>
<!--! Default freight catalogue entries have no runtime livery definition. -->
<tal:default_livery condition="model_variant.livery_def.livery_name not in global_constants.freight_wagon_liveries">
switch (FEAT_ROADVEHS, SELF, ${unit.id}_runtime_colour_mapping, 0) {
    return PALETTE_USE_DEFAULT;
}
switch (FEAT_ROADVEHS, SELF, ${unit.id}_purchase_colour_mapping, 0) {
    return PALETTE_USE_DEFAULT;
}
</tal:default_livery>
'''
elif '<tal:default_livery condition=' not in new_t:
    raise RuntimeError('unexpected road remap NML template')

old_e = E.read_text()
new_e = old_e
old_branch = '''    <tal:block condition="model_variant.gestalt_graphics.nml_template == 'vehicle_with_cargo_specific_liveries.pynml'">
        <tal:include metal:use-macro="load: vehicle_with_cargo_specific_liveries.pynml" />
    </tal:block>

'''
if old_branch in new_e: new_e=new_e.replace(old_branch,'')
elif 'vehicle_with_cargo_specific_liveries.pynml' in new_e: raise RuntimeError('unexpected legacy template selection')

changes={G:(old_g,new_g),S:(old_s,new_s),T:(old_t,new_t),E:(old_e,new_e)}
if 'GestaltGraphicsLiveryOnly' in new_g or 'GestaltGraphicsLiveryOnly' in new_s:
    raise RuntimeError('remaining legacy graphics class references')
if 'vehicle_with_cargo_specific_liveries.pynml' in new_e:
    raise RuntimeError('remaining legacy template references')
for path,(old,new) in changes.items():
    if old!=new:
        path.write_text(new)
        print('updated', path)
    else: print('unchanged',path)
if LEGACY.exists():
    LEGACY.unlink()
    print('removed',LEGACY)
print('009 complete')
