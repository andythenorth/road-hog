"""Run the real Makefile and report golden/current NML differences for review."""

import difflib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "generated" / "final_migration_audit"
PAIRS = (
    ("road-hog", "generated.reference/road-hog.reference.nml", "generated/road-hog.nml"),
    ("heqs", "generated.reference/heqs.reference.nml", "generated/heqs.nml"),
)


def main():
    if not (ROOT / "Makefile").is_file():
        raise SystemExit("Makefile missing: run inside the Road Hog repository")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    with (OUTPUT / "make.log").open("w", encoding="utf-8") as log:
        result = subprocess.run(
            ["make"], cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, check=False
        )
    if result.returncode != 0:
        print(f"FAIL: make exited {result.returncode}; inspect {OUTPUT / 'make.log'}")
        return result.returncode
    print("PASS: make exited 0")
    lines = ["# Final NML reference comparison", "", "Full `make`: PASS.", ""]
    missing = False
    for name, reference, current in PAIRS:
        before = ROOT / reference
        after = ROOT / current
        if not before.is_file() or not after.is_file():
            lines.append(f"- **{name}**: MISSING reference or generated NML")
            missing = True
            continue
        old = before.read_text(encoding="utf-8").splitlines(keepends=True)
        new = after.read_text(encoding="utf-8").splitlines(keepends=True)
        diff = list(
            difflib.unified_diff(old, new, fromfile=reference, tofile=current)
        )
        (OUTPUT / f"{name}.diff").write_text("".join(diff), encoding="utf-8")
        lines.append(
            f"- **{name}**: {'identical' if not diff else f'different; inspect `{name}.diff` and existing approved gameplay audit'}"
        )
    lines.extend(
        [
            "",
            "Differences are expected; this report does not approve or reject them.",
            "Use the existing gameplay and language review decisions for acceptance.",
        ]
    )
    (OUTPUT / "verification.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Verification report: {OUTPUT / 'verification.md'}")
    return 2 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
