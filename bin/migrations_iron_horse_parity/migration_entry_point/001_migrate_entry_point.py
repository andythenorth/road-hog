from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMPLATES = ROOT / "src" / "templates"
SCHEMAS = ROOT / "src" / "road_vehicle" / "schemas.py"

GRAPHICS_TEMPLATES = (
    "vehicle_default.pynml",
    "vehicle_with_precomposited_cargo.pynml",
    "vehicle_with_cargo_specific_liveries.pynml",
)
COMMON_INCLUDES = (
    '<tal:include metal:use-macro="load: graphics_switches.pynml" />',
    '<tal:include metal:use-macro="load: capacity_switches.pynml" />',
    '<tal:include metal:use-macro="load: properties.pynml" />',
)

ENTRY_POINT = '''<tal:units repeat="unit model_variant.unique_units">
    <!--! Graphics chains - conditional on gestalt graphics -->
    <tal:block condition="model_variant.gestalt_graphics.nml_template == 'vehicle_default.pynml'">
        <tal:include metal:use-macro="load: vehicle_default.pynml" />
    </tal:block>
    <tal:block condition="model_variant.gestalt_graphics.nml_template == 'vehicle_with_precomposited_cargo.pynml'">
        <tal:include metal:use-macro="load: vehicle_with_precomposited_cargo.pynml" />
    </tal:block>
    <tal:block condition="model_variant.gestalt_graphics.nml_template == 'vehicle_with_cargo_specific_liveries.pynml'">
        <tal:include metal:use-macro="load: vehicle_with_cargo_specific_liveries.pynml" />
    </tal:block>

    <!--! Properties and callback chains -->
    <tal:include metal:use-macro="load: graphics_switches.pynml" />
    <tal:include metal:use-macro="load: capacity_switches.pynml" />
    <tal:articulated_parts condition="unit.is_lead_unit_of_consist and len(model_variant.units) > 1">
        <tal:include metal:use-macro="load: articulated_parts.pynml" />
    </tal:articulated_parts>
    <tal:include metal:use-macro="load: properties.pynml" />
</tal:units>
'''


def migrate():
    changes = {}
    for name in GRAPHICS_TEMPLATES:
        path = TEMPLATES / name
        source = path.read_text()
        modified = source
        for include in COMMON_INCLUDES:
            if modified.count(include) == 1:
                modified = modified.replace(include, "", 1)
            elif include not in modified and (TEMPLATES / "model_variant_entry_point.pynml").exists():
                pass
            else:
                raise RuntimeError(f"Unexpected include in {path}: {include}")
        if modified != source:
            changes[path] = modified.rstrip() + "\n"

    source = SCHEMAS.read_text()
    start = source.index("    def render(self, templates, graphics_path):")
    end = source.index("    @property\n    def unique_units(self):", start)
    method = source[start:end]
    if 'templates["articulated_parts.pynml"]' in method:
        new_method = '''    def render(self, templates, graphics_path):
        template = templates["model_variant_entry_point.pynml"]
        return template(model_variant=self, global_constants=global_constants)

'''
        changes[SCHEMAS] = source[:start] + new_method + source[end:]
    elif 'templates["model_variant_entry_point.pynml"]' not in method:
        raise RuntimeError("Unexpected RoadVehicleBase.render() implementation")

    entry_path = TEMPLATES / "model_variant_entry_point.pynml"
    if entry_path.exists() and entry_path.read_text() != ENTRY_POINT:
        raise RuntimeError("Entry-point template already exists with different content")
    if not entry_path.exists():
        changes[entry_path] = ENTRY_POINT

    for path, content in changes.items():
        path.write_text(content)
        print(f"updated {path.relative_to(ROOT)}")
    if not changes:
        print("no changes")


if __name__ == "__main__":
    migrate()
