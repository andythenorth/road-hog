from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
UNITS = ROOT / "src/road_vehicle/units.py"
SCHEMAS = ROOT / "src/road_vehicle/schemas.py"
PROPERTIES = ROOT / "src/templates/properties.pynml"
ENGLISH = ROOT / "src/templates/english.pylng"


def replace_optional(text, old, new):
    if old in text:
        return text.replace(old, new)
    return text


def update_units(text):
    for cls, suffix, sound in (
        ("DieselVehicleUnit", "DIESEL", "SOUND_DEPARTURE_OLD_RV_1"),
        ("SteamVehicleUnit", "STEAM", "SOUND_FACTORY"),
        ("ElectricVehicleUnit", "ELECTRIC", "SOUND_POWER_STATION"),
    ):
        pattern = rf"(?m)^class {cls}\(RoadVehicleUnit\):\n"
        matches = list(re.finditer(pattern, text))
        if len(matches) != 1:
            raise RuntimeError(f"Expected one declaration of {cls}")
        start = matches[0].end()
        next_class = re.search(r"(?m)^class \w+\(", text[start:])
        end = start + next_class.start() if next_class else len(text)
        section = text[start:end]
        declaration = f'    default_sound_effect = "{sound}"\n'
        if declaration not in section:
            section = declaration + "\n" + section
        section = replace_optional(
            section, f'        self.model_variant.default_sound_effect = "{sound}"\n', ""
        )
        section = replace_optional(
            section, f'        self.model_variant._power_type_suffix = "{suffix}"\n', ""
        )
        section = replace_optional(section, f'    power_type_suffix = "{suffix}"\n', "")
        text = text[:start] + section + text[end:]

    text = replace_optional(
        text, "        # CABBAGE Stage 005: restore legacy unit-originating model defaults.\n", ""
    )
    text = replace_optional(
        text,
        "# CABBAGE BEGIN LEGACY UNIT TYPES STAGE 005\n"
        "# CABBAGE Port unit-originating effects and consist state, not unit aliases.\n"
        "# DieselVehicleUnit exists already; restore its missing model side effects.\n",
        "",
    )
    text = replace_optional(text, "# CABBAGE END LEGACY UNIT TYPES STAGE 005\n", "")
    if re.search(r"self\.model_variant\.(?:_power_type_suffix|default_sound_effect)\s*=", text):
        raise RuntimeError("Unit constructor still mutates parent sound or suffix")
    return text


def update_schemas(text):
    # Both the legacy getter and the attempted lead-unit getter are superseded.
    getter = re.compile(
        r"(?m)^    @property\n    def sound_effect\(self\):\n"
        r"(?:        .*\n|            .*\n)+\n"
    )
    text, count = getter.subn("", text)
    if count > 1:
        raise RuntimeError("Multiple sound_effect getters")

    start_marker = "    @property\n    def name(self):\n"
    start = text.find(start_marker)
    if start == -1:
        raise RuntimeError("No RoadVehicleBase.name property")
    end = text.find("\n\n", start + len(start_marker))
    if end == -1:
        raise RuntimeError("Cannot locate end of name property")
    current = text[start:end]
    replacement = (
        "    @property\n"
        "    def name(self):\n"
        "        return (\n"
        '            "string(STR_NAME_CONSIST, string(STR_NAME_"\n'
        "            + self.model_def.model_id.upper()\n"
        '            + "), string("\n'
        "            + self.name_type_suffix\n"
        '            + "))"\n'
        "        )"
    )
    if current != replacement:
        if "STR_NAME_CONSIST" not in current or "self.name_type_suffix" not in current:
            raise RuntimeError("Unexpected name property; refusing to replace")
        text = text[:start] + replacement + text[end:]
    return text


def update_properties(text):
    old = "${model_variant.sound_effect}"
    new = '${getattr(model_variant, "_sound_effect", None) or unit.default_sound_effect}'
    if old in text:
        text = text.replace(old, new)
    elif new not in text:
        raise RuntimeError("Unexpected sound_effect template expression")
    return text


def update_english(text):
    old = "STR_NAME_CONSIST                                                :{STRING} {STRING} ({STRING})"
    new = "STR_NAME_CONSIST                                                :{STRING} {STRING}"
    if old in text:
        return text.replace(old, new)
    if new not in text:
        raise RuntimeError("Unexpected STR_NAME_CONSIST format")
    return text


def main():
    changes = {}
    for path, transform in (
        (UNITS, update_units),
        (SCHEMAS, update_schemas),
        (PROPERTIES, update_properties),
        (ENGLISH, update_english),
    ):
        before = path.read_text(encoding="utf-8")
        after = transform(before)
        changes[path] = (before, after)
    # Validate all transformations before writing any file.
    for path, (before, after) in changes.items():
        if before != after:
            path.write_text(after, encoding="utf-8")
            print(f"updated {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
