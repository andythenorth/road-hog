"""Replace copied track-type settings with ordinary mixin inheritance."""

import ast
from pathlib import Path


SOURCE = Path("src/road_vehicle/schemas.py")
TRACK_FIELDS = {
    "base_track_type_name",
    "roadveh_flag_tram",
    "tractive_effort_coefficient",
    "name_suffix_vehicle_type",
    "vehicle_role",
}


def migrate(source):
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    edits = []

    def replace(start, end, new):
        edits.append((start - 1, end, new))

    classes = {
        node.name: node for node in tree.body if isinstance(node, ast.ClassDef)
    }
    for lineno, line in enumerate(lines, 1):
        if line.strip() in {
            "# Road Hog default, not Iron Horse train default (0.3).",
            "# CABBAGE The original track mixins use class attributes; keep that composition.",
        }:
            replace(lineno, lineno, "")

    base = classes["RoadVehicleBase"]
    base_init = next(
        node
        for node in base.body
        if isinstance(node, ast.FunctionDef) and node.name == "__init__"
    )

    for node in base_init.body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Attribute) or not isinstance(
            target.value, ast.Name
        ):
            continue
        if target.value.id != "self":
            continue
        if target.attr in {
            "base_track_type_name",
            "roadveh_flag_tram",
            "tractive_effort_coefficient",
        }:
            replace(node.lineno, node.end_lineno, "")

    if not any(
        isinstance(node, ast.FunctionDef) and node.name == "tractive_effort_coefficient"
        for node in base.body
    ):
        marker = next(
            node
            for node in base.body
            if isinstance(node, ast.FunctionDef) and node.name == "power"
        )
        property_text = (
            "    @property\n"
            "    def tractive_effort_coefficient(self):\n"
            "        if self.model_def.tractive_effort_coefficient is not None:\n"
            "            return self.model_def.tractive_effort_coefficient\n"
            "\n"
            "        return self.default_tractive_effort_coefficient\n"
            "\n"
        )
        replace(
            marker.decorator_list[0].lineno,
            marker.decorator_list[0].lineno - 1,
            property_text,
        )

    for name, cls in classes.items():
        if name.startswith("TrackTypeMixin"):
            for node in cls.body:
                if not isinstance(node, ast.Assign) or len(node.targets) != 1:
                    continue
                target = node.targets[0]
                if (
                    isinstance(target, ast.Name)
                    and target.id == "tractive_effort_coefficient"
                ):
                    old = lines[node.lineno - 1]
                    replace(
                        node.lineno,
                        node.end_lineno,
                        old.replace(
                            "tractive_effort_coefficient",
                            "default_tractive_effort_coefficient",
                            1,
                        ),
                    )
            continue

        if name == "RoadVehicleBase" or not cls.bases:
            continue

        init = next(
            (
                node
                for node in cls.body
                if isinstance(node, ast.FunctionDef) and node.name == "__init__"
            ),
            None,
        )
        copied = []
        if init is not None:
            for node in init.body:
                if not isinstance(node, ast.Assign) or len(node.targets) != 1:
                    continue
                target, value = node.targets[0], node.value
                if (
                    isinstance(target, ast.Attribute)
                    and isinstance(target.value, ast.Name)
                    and target.value.id == "self"
                    and target.attr in TRACK_FIELDS
                    and isinstance(value, ast.Attribute)
                    and isinstance(value.value, ast.Name)
                    and value.value.id.startswith("TrackTypeMixin")
                ):
                    copied.append((node, value.value.id))

        if copied:
            mixins = {mixin for _, mixin in copied}
            if len(mixins) != 1:
                raise RuntimeError(f"Mixed track-type settings in {name}: {mixins}")
            mixin = next(iter(mixins))
        elif name == "IntermodalHauler":
            # Previously inherited RoadVehicleBase's ROAD defaults.
            mixin = "TrackTypeMixinTruckBusCoach"
        else:
            continue

        if not any(
            isinstance(parent, ast.Name) and parent.id == mixin
            for parent in cls.bases
        ):
            header = lines[cls.lineno - 1]
            old = f"class {name}("
            if not header.startswith(old):
                raise RuntimeError(f"Unexpected class declaration: {header.strip()}")
            replace(
                cls.lineno,
                cls.lineno,
                header.replace(old, f"class {name}({mixin}, ", 1),
            )

        remove_whole_init = False
        if init is not None and copied:
            copied_nodes = {id(node) for node, _ in copied}
            remaining = [node for node in init.body if id(node) not in copied_nodes]
            if len(remaining) == 1 and isinstance(remaining[0], ast.Expr):
                expr = remaining[0].value
                if (
                    isinstance(expr, ast.Call)
                    and isinstance(expr.func, ast.Attribute)
                    and expr.func.attr == "__init__"
                    and isinstance(expr.func.value, ast.Call)
                    and isinstance(expr.func.value.func, ast.Name)
                    and expr.func.value.func.id == "super"
                ):
                    remove_whole_init = True
                    replace(
                        init.lineno,
                        init.end_lineno,
                        "    pass\n" if len(cls.body) == 1 else "",
                    )

        if not remove_whole_init:
            for node, _ in copied:
                replace(node.lineno, node.end_lineno, "")

    for start, end, content in sorted(
        edits, key=lambda edit: (edit[0], edit[1]), reverse=True
    ):
        lines[start:end] = [content] if content else []

    result = "".join(lines)
    ast.parse(result)
    return result


def main():
    source = SOURCE.read_text(encoding="utf-8")
    updated = migrate(source)
    if updated != source:
        SOURCE.write_text(updated, encoding="utf-8")
        print(f"Updated {SOURCE}")
    else:
        print("No changes")


if __name__ == "__main__":
    main()
