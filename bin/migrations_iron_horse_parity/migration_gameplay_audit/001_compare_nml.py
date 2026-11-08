#!/usr/bin/env python3
"""Review gameplay-property differences between legacy and current generated NML."""

import argparse
import csv
import hashlib
import re
from collections import defaultdict
from pathlib import Path

PAIRS = {
    "road-hog": (
        Path("generated.reference/road-hog.reference.nml"),
        Path("generated/road-hog.nml"),
    ),
    "heqs": (
        Path("generated.reference/heqs.reference.nml"),
        Path("generated/heqs.nml"),
    ),
}
# Graphics and callbacks are deliberately not compared. These are Action 0
# property names excluded because their migration was already reviewed.
EXCLUDE = {
    "cargo_allow_refit",
    "cargo_disallow_refit",
    "refittable_cargo_classes",
    "non_refittable_cargo_classes",
}
ITEM = re.compile(r"\bitem\s*\(\s*([^,]+)\s*,\s*([^,]+)\s*,\s*([^)]+)\)\s*\{", re.M)
PROPERTY = re.compile(r"\bproperty\s*\{", re.M)
ASSIGNMENT = re.compile(r"\b([a-zA-Z_][\w]*)\s*:\s*(.*?);", re.S)
FIELDS = ["id", "grf", "vehicle", "property", "reference", "current", "decision", "reason"]


def remove_comments(source):
    # Do not strip comment tokens within quoted strings.
    return re.sub(r'"(?:\\.|[^"\\])*"|//[^\n]*|/\*[\s\S]*?\*/',
                  lambda match: match.group() if match.group().startswith('"') else "", source)


def closing_brace(text, opening):
    depth = 0
    in_string = False
    escaped = False
    for pos in range(opening, len(text)):
        char = text[pos]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return pos
    raise ValueError(f"Unclosed brace at offset {opening}")


def normalise(value):
    return re.sub(r"\s+", "", value)


def extract(path):
    text = remove_comments(path.read_text(encoding="utf-8-sig"))
    results = defaultdict(dict)
    for match in ITEM.finditer(text):
        block_start = match.end() - 1
        block = text[block_start + 1:closing_brace(text, block_start)]
        # Use feature and numeric ID; symbol names change during migrations.
        vehicle = f"{normalise(match.group(1))}:{normalise(match.group(3))}"
        for prop_match in PROPERTY.finditer(block):
            start = prop_match.end() - 1
            props = block[start + 1:closing_brace(block, start)]
            for assignment in ASSIGNMENT.finditer(props):
                key = assignment.group(1)
                if key not in EXCLUDE:
                    value = normalise(assignment.group(2))
                    # Duplicate declarations on the same numeric ID are accepted
                    # only when identical (e.g. repeated climate declarations).
                    old = results[vehicle].get(key)
                    if old is not None and old != value:
                        raise ValueError(f"Conflicting {vehicle}.{key} in {path}")
                    results[vehicle][key] = value
    if not results:
        raise ValueError(f"No item properties parsed from {path}")
    return results


def differences():
    rows = []
    for grf, (reference_path, current_path) in PAIRS.items():
        for path in (reference_path, current_path):
            if not path.is_file():
                raise FileNotFoundError(path)
        reference = extract(reference_path)
        current = extract(current_path)
        for vehicle in sorted(reference.keys() | current.keys()):
            before = reference.get(vehicle, {})
            after = current.get(vehicle, {})
            for prop in sorted(before.keys() | after.keys()):
                old = before.get(prop, "<missing>")
                new = after.get(prop, "<missing>")
                if old == new:
                    continue
                fingerprint = hashlib.sha256(
                    "\x00".join((grf, vehicle, prop, old, new)).encode()
                ).hexdigest()[:16]
                rows.append({
                    "id": fingerprint,
                    "grf": grf,
                    "vehicle": vehicle,
                    "property": prop,
                    "reference": old,
                    "current": new,
                    "decision": "",
                    "reason": "",
                })
    return rows


def save_review(path, rows):
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def grouped_differences(rows):
    groups = defaultdict(list)
    for row in rows:
        key = (row["grf"], row["property"], row["reference"], row["current"])
        groups[key].append(row)
    return sorted(groups.items(), key=lambda entry: (-len(entry[1]), entry[0]))


def interactive_review(rows, review_path):
    groups = grouped_differences(rows)
    outstanding = [
        (key, entries)
        for key, entries in groups
        if any(row["decision"] not in ("approve", "reject") for row in entries)
    ]
    if not outstanding:
        print("No pending groups to review.")
        return

    print("Review: [A]pprove / [R]eject / [S]kip / [Q]uit")
    for index, (key, entries) in enumerate(outstanding, 1):
        pending = [row for row in entries if row["decision"] not in ("approve", "reject")]
        if not pending:
            continue
        grf, prop, old, new = key
        print(f"\n[{index}/{len(outstanding)}] {grf}: {prop} ({len(pending)} pending vehicles)")
        print(f"  Reference: {old}")
        print(f"  Current:   {new}")
        print("  Vehicles: " + ", ".join(row["vehicle"] for row in pending))
        while True:
            try:
                choice = input("  [A/R/S/Q]: ").strip().lower()
            except (KeyboardInterrupt, EOFError):
                print("\nReview stopped; previous decisions saved.")
                return
            if choice in ("a", "r", "s", "q"):
                break
            print("  Enter A, R, S or Q.")
        if choice == "q":
            break
        if choice == "s":
            continue
        decision = "approve" if choice == "a" else "reject"
        try:
            reason = input("  Reason (optional): ").strip()
        except (KeyboardInterrupt, EOFError):
            reason = ""
            print("\nReason omitted; decision saved.")
        for row in pending:
            row["decision"] = decision
            row["reason"] = reason
        save_review(review_path, rows)
        print(f"  Saved: {decision} for {len(pending)} vehicles")


def write_report(output, rows):
    groups = grouped_differences(rows)
    report = [
        "# Gameplay NML differences",
        "",
        f"{len(rows)} property differences in {len(groups)} groups.",
        "",
        "Run the script interactively to approve or reject groups, or edit `review.csv`.",
        "Approvals are retained only for identical differences on subsequent runs.",
        "",
        "Only Action 0 item `property` blocks are compared; graphics callbacks are excluded.",
        "Cargo-class and cargo-label refit properties are excluded (already migrated).",
        "",
        "Comparison is textual after whitespace/comment normalization, not an NML evaluator.",
        "",
    ]
    for (grf, prop, old, new), entries in groups:
        approved = sum(row["decision"] == "approve" for row in entries)
        rejected = sum(row["decision"] == "reject" for row in entries)
        pending = len(entries) - approved - rejected
        report.extend(
            [
                f"## {grf}: `{prop}` — {len(entries)} vehicle IDs",
                "",
                f"- Reference: `{old}`",
                f"- Current: `{new}`",
                f"- Decisions: {approved} approved, {rejected} rejected, {pending} pending",
                "- Vehicles: " + ", ".join(row["vehicle"] for row in entries),
                "",
            ]
        )
    (output / "report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    return len(groups)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("generated/gameplay_audit"))
    parser.add_argument(
        "--no-interactive", action="store_true", help="Generate reports without prompting"
    )
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    review_path = args.output / "review.csv"
    previous = {}
    if review_path.exists():
        with review_path.open(newline="", encoding="utf-8") as stream:
            previous = {row["id"]: row for row in csv.DictReader(stream)}
    rows = differences()
    for row in rows:
        existing = previous.get(row["id"], {})
        row["decision"] = existing.get("decision", "")
        row["reason"] = existing.get("reason", "")
    save_review(review_path, rows)

    if not args.no_interactive:
        interactive_review(rows, review_path)

    group_count = write_report(args.output, rows)
    pending = sum(row["decision"] not in ("approve", "reject") for row in rows)
    rejected = sum(row["decision"] == "reject" for row in rows)
    print(f"{len(rows)} differences ({group_count} groups); {pending} pending, {rejected} rejected")
    print(f"Review: {review_path} | Summary: {args.output / 'report.md'}")
    if rejected or pending:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
