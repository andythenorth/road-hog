from pathlib import Path
import re

root=Path.cwd()
s=root/'src/road_vehicle/schemas.py'
g=root/'src/gestalt_graphics/gestalt_graphics.py'
assert s.exists() and g.exists(), 'Run from Road Hog repository root'
files={s:s.read_text(),g:g.read_text()}
# Validate the public gestalt shape before any writes.
a=files[g]
start=a.index('class GestaltGraphicsSimpleBodyColourRemaps(GestaltGraphics):')
end=a.find('\nclass ',start+7)
if end<0:end=len(a)
old=a[start:end]
# Accept the exact template-only class shipped before migration 009 as well as
# the interim body_recolour_map implementation and our already-migrated class.
legacy_stub = (
    'def __init__(' not in old
    and 'def get_output_row_types(' not in old
    and 'return "vehicle_with_simple_body_colour_remaps_road.pynml"' in old
)
if not (legacy_stub or ('body_recolour_map' in old) or ('weathered_states' in old)):
    raise RuntimeError('Unexpected remap gestalt; inspect before migration')
replacement='''class GestaltGraphicsSimpleBodyColourRemaps(GestaltGraphics):
    # IH constructor interface; RH uses an existing compositor for the
    # single unweathered freight CC1 row. CC-ready passenger sprites need none.
    def __init__(self, recolour_map=None, weathered_states=None, catalogue_entry=None, **kwargs):
        super().__init__()
        self.catalogue_entry = catalogue_entry
        self.recolour_map = recolour_map
        self.weathered_states = weathered_states if weathered_states is not None else {"unweathered": recolour_map}
        if set(self.weathered_states) != {"unweathered"}:
            raise NotImplementedError("Road Hog only supports unweathered body recolouring")
        unweathered_map = self.weathered_states["unweathered"]
        if recolour_map is not None and unweathered_map != recolour_map:
            raise ValueError("recolour_map differs from unweathered weathered_states")
        if unweathered_map is not None:
            self.pipelines = pipelines.get_pipelines(
                ["extend_spriterows_for_composited_sprites_pipeline"]
            )
            # CABBAGE352: compositor calls this legacy output type livery_only.
            self.recolour_maps = [("DFLT", unweathered_map)]

    def get_output_row_types(self):
        if self.weathered_states["unweathered"] is not None:
            return ["livery_only"]
        return super().get_output_row_types()

    @property
    def nml_template(self):
        return "vehicle_with_simple_body_colour_remaps_road.pynml"
'''
files[g]=a[:start]+replacement+a[end:]

x=files[s]
# Remove scattered graphics imports; keep one canonical import group near top.
x=re.sub(r'(?m)^from gestalt_graphics\.gestalt_graphics import \(\n(?:    [^\n]+\n)+\)\n', '',x)
x=re.sub(r'(?m)^from gestalt_graphics\.gestalt_graphics import GestaltGraphics, GestaltGraphicsSimpleBodyColourRemaps\n','',x)
x=re.sub(r'(?m)^import gestalt_graphics\.graphics_constants as graphics_constants\n','',x)
x=re.sub(r'(?m)^from gestalt_graphics import graphics_constants\n','',x)
x=re.sub(r'(?m)^import polar_fox\n','',x)
intro='''import polar_fox
from gestalt_graphics import graphics_constants
from gestalt_graphics.gestalt_graphics import (
    GestaltGraphics,
    GestaltGraphicsCustom,
    GestaltGraphicsPrecompositedCargo,
    GestaltGraphicsSimpleBodyColourRemaps,
)
'''
anchor='import global_constants\n'
if anchor not in x:raise RuntimeError('Cannot find import anchor')
x=x.replace(anchor,anchor+intro,1)
# Original legacy freight schemas or partially migrated CC1 schemas.
legacy=r'GestaltGraphicsLiveryOnly\(\s*recolour_maps\s*=\s*(?:polar_fox\.constants\.tanker_livery_recolour_maps|graphics_constants\.livestock_livery_recolour_maps)\s*\)'
freight_call='''GestaltGraphicsSimpleBodyColourRemaps(
            recolour_map=graphics_constants.body_recolour_CC1,
            weathered_states={"unweathered": graphics_constants.body_recolour_CC1},
            catalogue_entry=self.catalogue_entry,
        )'''
x,n_legacy=re.subn(legacy,freight_call,x)
oldfreight=r'GestaltGraphicsSimpleBodyColourRemaps\(\s*body_recolour_map=graphics_constants\.body_recolour_CC1\s*\)'
x,n_current=re.subn(oldfreight,freight_call,x)
if n_legacy+n_current == 0 and x.count('recolour_map=graphics_constants.body_recolour_CC1,') == 6:
    pass  # already migrated
elif n_legacy+n_current != 6:
    raise RuntimeError(f'Expected 6 freight gestalts, found {n_legacy+n_current}')
# Consolidate passenger graphics on the common base.
segment_start=x.index('class PaxHaulerConsistBase(RoadVehicleBase):')
segment_end=x.index('\nclass ',segment_start+7)
seg=x[segment_start:segment_end]
needle='        super().__init__(producer, catalogue_entry)\n'
if needle not in seg:raise RuntimeError('Pax base constructor not found')
if 'self.gestalt_graphics = GestaltGraphicsSimpleBodyColourRemaps(' not in seg:
    seg=seg.replace(needle,needle+'''        self.gestalt_graphics = GestaltGraphicsSimpleBodyColourRemaps(
            weathered_states={"unweathered": None},
            catalogue_entry=self.catalogue_entry,
        )
''',1)
x=x[:segment_start]+seg+x[segment_end:]
# Remove spike classes (their only role was selecting graphics).
for name,parent in [('PaxLocalBusRuntimeRemapSpike','PaxLocalBus'),('PaxLocalTramRuntimeRemapSpike','PaxLocalTram'),('PaxExpressCoachRuntimeRemapSpike','PaxExpressCoach')]:
    pattern=rf'(?m)^class {name}\({parent}\):\n(?:    [^\n]*\n|\n)*?(?=^class |\Z)'
    x,count=re.subn(pattern,'',x)
    if count not in (0,1):raise RuntimeError(f'Unexpected number of {name}: {count}')
if 'GestaltGraphicsLiveryOnly' in x or 'RuntimeRemapSpike' in x:
    raise RuntimeError('Legacy graphics reference remains')
files[s]=x
# Update declarations only where using the temporary schema.
vehicles=root/'src/vehicles'
replace_names={
 'PaxLocalBusRuntimeRemapSpike':'PaxLocalBus',
 'PaxLocalTramRuntimeRemapSpike':'PaxLocalTram',
 'PaxExpressCoachRuntimeRemapSpike':'PaxExpressCoach',
}
changed_models=0
for path in vehicles.glob('*.py'):
    source=path.read_text(); new=source
    for oldname,newname in replace_names.items():
        new=new.replace(f'schema_name="{oldname}"',f'schema_name="{newname}"')
        new=new.replace(f"schema_name='{oldname}'",f"schema_name='{newname}'")
    if new!=source:
        files[path]=new
        changed_models+=1
if changed_models not in (0,13):raise RuntimeError(f'Expected 0 or 13 passenger models, found {changed_models}')
# No modifications until all checks passed.
for path,value in files.items():
    if path.read_text()!=value:
        path.write_text(value)
        print('updated',path)
print('011 complete: 6 freight schemas, 13 passenger declarations')
