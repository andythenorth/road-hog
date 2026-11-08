import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
UNITS = ROOT / "src/road_vehicle/units.py"
SCHEMAS = ROOT / "src/road_vehicle/schemas.py"


def replace_once(source, old, new):
    if new and new in source:
        return source
    if old in source:
        if source.count(old) != 1:
            raise ValueError("Expected one match: " + old[:90])
        return source.replace(old, new, 1)
    if new in source:
        return source
    raise ValueError("Source does not match expected version: " + old[:90])


def migrate():
    units = UNITS.read_text(encoding="utf-8")
    schemas = SCHEMAS.read_text(encoding="utf-8")

    for old, new in [
        (
            "class DieselVehicleUnit(RoadVehicleUnit):\n",
            'class DieselVehicleUnit(RoadVehicleUnit):\n    power_type_suffix = "DIESEL"\n    default_sound_effect = "SOUND_DEPARTURE_OLD_RV_1"\n',
        ),
        (
            "class SteamVehicleUnit(RoadVehicleUnit):\n",
            'class SteamVehicleUnit(RoadVehicleUnit):\n    power_type_suffix = "STEAM"\n    default_sound_effect = "SOUND_FACTORY"\n',
        ),
        (
            "class ElectricVehicleUnit(RoadVehicleUnit):\n",
            'class ElectricVehicleUnit(RoadVehicleUnit):\n    power_type_suffix = "ELECTRIC"\n    default_sound_effect = "SOUND_POWER_STATION"\n    requires_electricity_supply = True\n',
        ),
    ]:
        units = replace_once(units, old, new)

    for line in [
        '        self.model_variant._power_type_suffix = "DIESEL"\n',
        '        self.model_variant.default_sound_effect = "SOUND_DEPARTURE_OLD_RV_1"\n',
        '        self.model_variant._power_type_suffix = "STEAM"\n',
        '        self.model_variant.default_sound_effect = "SOUND_FACTORY"\n',
        '        self.model_variant.requires_electricity_supply = True\n',
        '        self.model_variant._power_type_suffix = "ELECTRIC"\n',
        '        self.model_variant.default_sound_effect = "SOUND_POWER_STATION"\n',
        '        # CABBAGE Stage 005: restore legacy unit-originating model defaults.\n',
        '# CABBAGE BEGIN LEGACY UNIT TYPES STAGE 005\n',
        '# CABBAGE Port unit-originating effects and consist state, not unit aliases.\n',
        '# DieselVehicleUnit exists already; restore its missing model side effects.\n',
        '# CABBAGE END LEGACY UNIT TYPES STAGE 005\n',
    ]:
        units = replace_once(units, line, "")

    schemas = replace_once(
        schemas,
        '        if getattr(self, "requires_electricity_supply", False):\n',
        '        if getattr(self.units[0], "requires_electricity_supply", False):\n',
    )
    schemas = replace_once(
        schemas,
        '''    @property
    def sound_effect(self):
        if getattr(self, "_sound_effect", None) is not None:
            return self._sound_effect
        return getattr(self, "default_sound_effect", None)
''',
        '''    @property
    def sound_effect(self):
        if getattr(self, "_sound_effect", None) is not None:
            return self._sound_effect
        return getattr(self.units[0], "default_sound_effect", None)
''',
    )
    schemas = replace_once(
        schemas,
        '        suffix = getattr(self, "_power_type_suffix", None)\n',
        '        suffix = getattr(self.units[0], "power_type_suffix", None)\n',
    )

    ast.parse(units, filename=str(UNITS))
    ast.parse(schemas, filename=str(SCHEMAS))
    changed = []
    for path, content in [(UNITS, units), (SCHEMAS, schemas)]:
        if path.read_text(encoding="utf-8") != content:
            path.write_text(content, encoding="utf-8")
            changed.append(str(path.relative_to(ROOT)))
    print("Updated: " + (", ".join(changed) if changed else "none"))


if __name__ == "__main__":
    migrate()
