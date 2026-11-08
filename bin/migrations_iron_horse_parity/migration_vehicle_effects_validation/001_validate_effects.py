#!/usr/bin/env python3
"""Compare road-vehicle effects in legacy and current generated NML."""

import argparse
import csv
import re
from collections import Counter
from pathlib import Path

PAIRS = (
    (
        "road-hog",
        Path("generated.reference/road-hog.reference.nml"),
        Path("generated/road-hog.nml"),
    ),
    (
        "heqs",
        Path("generated.reference/heqs.reference.nml"),
        Path("generated/heqs.nml"),
    ),
)
ITEM = re.compile(r"\bitem\s*\(\s*([^,]+)\s*,\s*([^,]+)\s*,\s*([^)]+)\)\s*\{", re.M)
PROPERTY = re.compile(r"\bproperty\s*\{", re.M)
GRAPHICS = re.compile(r"\bgraphics\s*\{", re.M)
ASSIGNMENT = re.compile(r"\b([A-Za-z_]\w*)\s*:\s*(.*?);", re.S)
SWITCH = re.compile(
    r"\bswitch\s*\(\s*[^,]+\s*,\s*SELF\s*,\s*"
    r"([A-Za-z_]\w*_create_visual_effect)\s*,\s*(.*?)\)\s*\{",
    re.S,
)
FIELDS = ("grf", "vehicle", "field", "reference", "current")


def remove_comments(source):
    return re.sub(
        r'"(?:\\.|[^"\\])*"|//[^\n]*|/\*[\s\S]*?\*/',
        lambda match: match.group() if match.group().startswith('"') else "",
        source,
    )


def closing_brace(source, start):
    depth = 0
    for index in range(start, len(source)):
        if source[index] == "{":
            depth += 1
        elif source[index] == "}":
            depth -= 1
            if depth == 0:
                return index
    raise ValueError(f"Unclosed NML block at offset {start}")


def normalise(value):
    return re.sub(r"\s+", "", value)


def assignments(block):
    return {
        match.group(1): normalise(match.group(2))
        for match in ASSIGNMENT.finditer(block)
    }


def read_effects(path):
    source = remove_comments(path.read_text(encoding="utf-8-sig"))
    switches = {
        match.group(1): normalise(match.group(2))
        for match in SWITCH.finditer(source)
    }
    records = {}
    for match in ITEM.finditer(source):
        start = match.end() - 1
        body = source[start + 1 : closing_brace(source, start)]
        vehicle = f"{normalise(match.group(1))}:{normalise(match.group(3))}"
        record = records.setdefault(vehicle, {})
        for prop in PROPERTY.finditer(body):
            begin = prop.end() - 1
            values = assignments(body[begin + 1 : closing_brace(body, begin)])
            for key in ("effect_spawn_model", "sound_effect"):
                if key in values:
                    if key in record and record[key] != values[key]:
                        raise ValueError(f"Conflicting {vehicle}.{key} in {path}")
                    record[key] = values[key]
        for graphic in GRAPHICS.finditer(body):
            begin = graphic.end() - 1
            values = assignments(body[begin + 1 : closing_brace(body, begin)])
            if "create_effect" in values:
                symbol = values["create_effect"]
                expression = switches.get(symbol)
                if expression is None:
                    raise ValueError(f"Missing create_effect switch {symbol} in {path}")
                key = "create_effect_expression"
                if key in record and record[key] != expression:
                    raise ValueError(f"Conflicting {vehicle}.{key} in {path}")
                record[key] = expression
    if not records:
        raise ValueError(f"No NML vehicle items found in {path}")
    return records


def compare():
    rows = []
    for grf, reference_path, current_path in PAIRS:
        for path in (reference_path, current_path):
            if not path.is_file():
                raise FileNotFoundError(path)
        reference = read_effects(reference_path)
        current = read_effects(current_path)
        for vehicle in sorted(reference.keys() | current.keys()):
            before = reference.get(vehicle, {})
            after = current.get(vehicle, {})
            for field in sorted(before.keys() | after.keys()):
                old = before.get(field, "<missing>")
                new = after.get(field, "<missing>")
                if old != new:
                    rows.append(
                        dict(
                            grf=grf,
                            vehicle=vehicle,
                            field=field,
                            reference=old,
                            current=new,
                        )
                    )
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, default=Path("generated/effects_audit")
    )
    args = parser.parse_args()
    rows = compare()
    args.output.mkdir(parents=True, exist_ok=True)
    with (args.output / "differences.csv").open(
        "w", encoding="utf-8", newline=""
    ) as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    counts = Counter((row["grf"], row["field"]) for row in rows)
    report = ["# Vehicle effect differences", ""]
    report.append(f"{len(rows)} divergences found.\n")
    report.append("| GRF | Field | Differences |")
    report.append("|---|---|---:|")
    for (grf, field), count in sorted(counts.items()):
        report.append(f"| {grf} | `{field}` | {count} |")
    report.extend(["", "## Individual differences", ""])
    for row in rows:
        report.append(f"### {row['grf']} {row['vehicle']} — {row['field']}")
        report.append(f"- Reference: `{row['reference']}`")
        report.append(f"- Current: `{row['current']}`")
        report.append("")
    (args.output / "report.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )
    print(f"Effect differences: {len(rows)}")
    for (grf, field), count in sorted(counts.items()):
        print(f"  {grf} {field}: {count}")
    print(f"Reports: {args.output}")
    return 1 if rows else 0


if __name__ == "__main__":
    raise SystemExit(main())
