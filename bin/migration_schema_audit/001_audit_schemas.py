from __future__ import annotations

import ast
import csv
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
SCHEMA = SRC / "road_vehicle" / "schemas.py"
OUT = ROOT / "generated" / "schema_audit"


def symbols(tree):
    return [node for node in tree.body if isinstance(node, ast.ClassDef)]


def names_in_ast(tree):
    result = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            result.add(node.id)
        if isinstance(node, ast.Attribute):
            result.add(node.attr)
        if isinstance(node, ast.ImportFrom):
            result.update(alias.name for alias in node.names)
    return result


def main():
    tree = ast.parse(SCHEMA.read_text(encoding="utf-8"), filename=str(SCHEMA))
    classes = symbols(tree)
    all_files = sorted(SRC.rglob("*.py"))
    parsed = {}
    for path in all_files:
        try:
            parsed[path] = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError as exc:
            print(f"Skipping {path.relative_to(ROOT)}: {exc}")
    external = {
        path: names_in_ast(parsed_tree)
        for path, parsed_tree in parsed.items()
        if path != SCHEMA
    }
    parents = {
        cls.name: [ast.unparse(base) for base in cls.bases] for cls in classes
    }
    rows = []
    for cls in classes:
        callers = [
            str(path.relative_to(ROOT))
            for path, names in external.items()
            if cls.name in names
        ]
        children = [
            name for name, bases in parents.items() if cls.name in bases
        ]
        rows.append(
            {
                "class": cls.name,
                "line": cls.lineno,
                "bases": ", ".join(parents[cls.name]),
                "derived_classes": ", ".join(children),
                "python_files_referring_to_name": len(callers),
                "files": "; ".join(callers),
            }
        )
    text = SCHEMA.read_text(encoding="utf-8")
    markers = [
        (i, line.strip())
        for i, line in enumerate(text.splitlines(), 1)
        if "CABBAGE" in line
    ]
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "classes.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    with (OUT / "cabbage.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["line", "comment"])
        writer.writerows(markers)
    unreferenced = [
        row for row in rows
        if not row["python_files_referring_to_name"] and not row["derived_classes"]
    ]
    report = [
        "# Schema architecture audit",
        "",
        f"Source: `{SCHEMA.relative_to(ROOT)}`",
        f"Classes: {len(rows)}; CABBAGE markers: {len(markers)}",
        "",
        "## Classes with no external Python name references and no subclasses",
        "",
        "These are candidates for inspection, not confirmed unused classes. The audit does not resolve dynamic lookups or template references.",
        "",
        "| Class | Line | Bases |",
        "|---|---:|---|",
    ]
    for row in unreferenced:
        report.append(f"| `{row['class']}` | {row['line']} | `{row['bases']}` |")
    report += ["", "## CABBAGE markers", ""]
    for line, comment in markers:
        report.append(f"- L{line}: `{comment}`")
    report += [
        "",
        "## Interpretation",
        "",
        "Class inheritance and named Python references are counted; dynamic class creation, string-based references, Chameleon templates and build scripts outside src are not resolved. Check the current production roster and build before deleting any class.",
        "",
    ]
    (OUT / "report.md").write_text("\n".join(report), encoding="utf-8")
    print(f"{len(rows)} classes, {len(markers)} CABBAGE markers, {len(unreferenced)} candidates")
    print(f"Report: {OUT / 'report.md'}")


if __name__ == "__main__":
    main()
