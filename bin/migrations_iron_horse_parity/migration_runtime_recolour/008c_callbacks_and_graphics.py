#!/usr/bin/env python3
"""Introduce RH graphics template and callbacks without changing active vehicle declarations."""
from pathlib import Path
import ast
root=Path('src'); templates=root/'templates'
gg=root/'gestalt_graphics/gestalt_graphics.py';entry=templates/'model_variant_entry_point.pynml';props=templates/'properties.pynml'
for f in (gg,entry,props):
 if not f.is_file():raise SystemExit(f'Missing {f}; run from repo root')
g=gg.read_text();e=entry.read_text();p=props.read_text()
klass="""\n\nclass GestaltGraphicsSimpleBodyColourRemaps(GestaltGraphics):
    # CABBAGE352: IH-named graphics interface for RH's existing CC1/CC2 sprite sheets.
    # No extra processing pipeline; runtime remaps are provided by NML callbacks.

    @property
    def nml_template(self):
        return "vehicle_with_simple_body_colour_remaps_road.pynml"
"""
if 'class GestaltGraphicsSimpleBodyColourRemaps(' not in g:g=g.rstrip()+klass+'\n'
elif klass.strip() not in g:raise SystemExit('CABBAGE352 graphics class collision')
newblock="""    <tal:block condition="model_variant.gestalt_graphics.nml_template == 'vehicle_with_simple_body_colour_remaps_road.pynml'">
        <tal:include metal:use-macro="load: vehicle_with_simple_body_colour_remaps_road.pynml" />
    </tal:block>
"""
if newblock.strip() not in e:
 anchor='    <!--! Properties and callback chains -->'
 if e.count(anchor)!=1:raise SystemExit('entrypoint anchor missing')
 e=e.replace(anchor,newblock+'\n'+anchor)
callbacks="""        <!--! CABBAGE352: colour callbacks are placeholders until wagon recolour procedures are adapted to RH. -->
        <tal:runtime_colours condition="model_variant.gestalt_graphics.nml_template == 'vehicle_with_simple_body_colour_remaps_road.pynml'">
            colour_mapping:                 PALETTE_USE_DEFAULT;
            purchase_colour_mapping:        PALETTE_USE_DEFAULT;
        </tal:runtime_colours>
"""
if callbacks.strip() not in p:
 anchor='        create_effect:                  ${unit.id}_create_visual_effect;'
 if p.count(anchor)!=1:raise SystemExit('properties anchor missing')
 p=p.replace(anchor,anchor+'\n'+callbacks)
# Dedicated template deliberately drops cargo-specific livery selection.
template="""<!--! CABBAGE352: dedicated single-sprite body colour remap graphics path.
     Cargo-specific sprite selection intentionally omitted. -->
<tal:include metal:use-macro="load: spriteset_templates.pynml" />

spriteset(${unit.id}_ss, "${global_constants.graphics_path}${model_variant.model_def.model_id}.png") {
  spriteset_template_${unit.id}(10 + ${unit.spriterow_num * 30})
}

spritegroup ${unit.id}_sg {
    loaded: [${unit.id}_ss];
    loading: [${unit.id}_ss];
}

switch (FEAT_ROADVEHS, SELF, ${unit.id}_switch_graphics, 0) {
    return ${unit.id}_sg;
}
"""
dest=templates/'vehicle_with_simple_body_colour_remaps_road.pynml'
if dest.exists() and dest.read_text()!=template:raise SystemExit('CABBAGE352 graphics template collision')
# Preflight all outputs before writing any of them.
ast.parse(g)
for f,v in [(gg,g),(entry,e),(props,p),(dest,template)]:
 if not f.exists() or f.read_text()!=v:f.write_text(v)
print('008c graphics template and callbacks staged; no vehicle graphics declarations changed')
