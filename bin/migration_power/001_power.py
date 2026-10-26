#!/usr/bin/env python3
"""Restore Road Hog scalar power declarations and roster-derived defaults."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def replace_once(text, old, new, path):
    if old not in text:
        if new in text:
            return text, False
        raise ValueError(f"Unexpected source in {path}: {old[:70]!r}")
    if text.count(old) != 1:
        raise ValueError(f"Non-unique source pattern in {path}")
    return text.replace(old, new, 1), True


def main():
    changes = {}
    edits = {
        "src/road_vehicle/schemas.py": [
            (
                """    @property
    def power(self):
        # CABBAGE Migration shim: keep old scalar Road Hog power and costs exact.
        if self.model_def.power is not None:
            return self.model_def.power
        powers = self.model_def.power_by_power_source
        if powers:
            return sum(powers.values())
        return self.roster.power_bands[self.base_track_type_name][
            self.model_def.gen - 1
        ]
""",
                """    @property
    def power(self):
        # Iron Horse style power_by_power_source was not implemented as of Oct 2026
        if self.model_def.power is not None:
            return self.model_def.power
        return self.roster.power_bands[self.base_track_type_name][
            self.model_def.gen - 1
        ]
""",
            )
        ],
        "src/road_vehicle/model_def.py": [
            (
                "from typing import Any, Dict, List, Optional",
                "from typing import Any, List, Optional",
            ),
            (
                """    # CABBAGE Migration shim: legacy Road Hog scalar power remains supported.
    # Multi-source mapping is storage only until separately implemented.
    power: Optional[int] = None
    power_by_power_source: Optional[Dict[Any, Any]] = None
""",
                "    power: Optional[int] = None\n".replace("\\n", "\n"),
            ),
            (
                """    def __post_init__(self):
        # CABBAGE Migration shim: two simultaneous power declarations are ambiguous.
        if self.power is not None and self.power_by_power_source is not None:
            raise ValueError("Specify power OR power_by_power_source, not both")

""",
                "",
            ),
            (
                """        # recalculate power in a clone
        result = {}
        for (
            power_type,
            power_value,
        ) in model_def.power_by_power_source.items():
            result[power_type] = int(
                power_value * model_def.clone_stats_adjustment_factor
            )
        model_def.power_by_power_source = result
""",
                """        # recalculate explicit power in a clone
        if model_def.power is not None:
            model_def.power = int(
                model_def.power * model_def.clone_stats_adjustment_factor
            )
""",
            ),
        ],
        "src/vehicles/migration_test_bus.py": [
            (
                'power_by_power_source={"DIESEL": 100},',
                "power=100,",
            )
        ],
    }
    for relative_path, replacements in edits.items():
        path = ROOT / relative_path
        if not path.is_file():
            raise FileNotFoundError(path)
        original = path.read_text(encoding="utf-8")
        updated = original
        for old, new in replacements:
            updated, _ = replace_once(updated, old, new, relative_path)
        if updated != original:
            compile(updated, str(path), "exec")
            changes[path] = updated
    for path, updated in changes.items():
        path.write_text(updated, encoding="utf-8")
        print(f"Updated {path.relative_to(ROOT)}")
    print(f"Complete: {len(changes)} files updated")


if __name__ == "__main__":
    main()
