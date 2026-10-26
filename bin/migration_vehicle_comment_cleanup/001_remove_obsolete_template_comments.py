"""Remove superseded first-pass template migration comments from vehicle modules.

Run from the Road Hog repository root. Only the exact three-line comment block
is removed; all other CABBAGE markers are preserved.
"""

from pathlib import Path


OBSOLETE_BLOCK = (
    "# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.\n"
    "# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific\n"
    "# spritegroups/liveries where present in this vehicle.\n"
)


def main():
    vehicles_dir = Path("src/vehicles")
    if not vehicles_dir.is_dir():
        raise SystemExit("Run from the repository root (src/vehicles not found).")

    changed = []
    for path in sorted(vehicles_dir.glob("*.py")):
        original = path.read_bytes()
        newline = b"\r\n" if b"\r\n" in original else b"\n"
        block = OBSOLETE_BLOCK.encode("utf-8").replace(b"\n", newline)
        occurrences = original.count(block)
        if not occurrences:
            continue
        if occurrences != 1:
            raise SystemExit(f"Expected one obsolete comment block in {path}; found {occurrences}.")
        updated = original.replace(block, b"", 1)
        path.write_bytes(updated)
        changed.append(str(path))

    print(f"Removed obsolete template migration comments from {len(changed)} vehicle modules.")
    for path in changed:
        print(f"  {path}")


if __name__ == "__main__":
    main()
