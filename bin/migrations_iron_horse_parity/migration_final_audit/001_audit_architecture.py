"""Read-only inventory of migration markers and potentially obsolete interfaces."""

import ast
import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
OUTPUT = ROOT / "generated" / "final_migration_audit"


def python_files():
    return sorted(SRC.rglob("*.py"))


def inspect_source():
    markers = []
    definitions = []
    sources = {}
    for path in python_files():
        relative = str(path.relative_to(ROOT))
        content = path.read_text(encoding="utf-8")
        sources[relative] = content
        for lineno, line in enumerate(content.splitlines(), 1):
            if "CABBAGE" in line:
                markers.append((relative, lineno, line.strip()))
        try:
            tree = ast.parse(content, filename=relative)
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                definitions.append((relative, node.lineno, node.name))
    # Textual references are leads for review, not proof of dead code.
    results = []
    for path, line, name in definitions:
        if name.startswith("__"):
            continue
        occurrences = sum(
            len(re.findall(r"\b" + re.escape(name) + r"\b", text))
            for text in sources.values()
        )
        if occurrences == 1:
            results.append((path, line, name, occurrences))
    return markers, results


def main():
    if not SRC.is_dir():
        raise SystemExit("Run from a Road Hog repository containing src/")
    markers, candidates = inspect_source()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    with (OUTPUT / "cabbage.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["file", "line", "marker", "decision", "notes"])
        writer.writerows((*marker, "", "") for marker in markers)
    with (OUTPUT / "unused_candidates.csv").open(
        "w", newline="", encoding="utf-8"
    ) as f:
        writer = csv.writer(f)
        writer.writerow(["file", "line", "definition", "text_references"])
        writer.writerows(candidates)
    counts = Counter(path for path, _, _ in markers)
    lines = [
        "# Final architecture audit",
        "",
        f"- `CABBAGE` markers: {len(markers)}",
        f"- Single-reference definitions (manual review only): {len(candidates)}",
        "",
        "## Marker counts by file",
        "",
        "| File | Count |",
        "|---|---:|",
    ]
    lines.extend(f"| `{file}` | {count} |" for file, count in counts.most_common())
    lines.extend(
        [
            "",
            "Review `cabbage.csv` and `unused_candidates.csv` before removing code.",
            "Single-reference names may be called dynamically (getattr, templates, etc.).",
            "No source files were modified.",
        ]
    )
    (OUTPUT / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Architecture report: {OUTPUT / 'report.md'}")
    print(f"Markers: {len(markers)}; candidates: {len(candidates)}")


if __name__ == "__main__":
    main()
