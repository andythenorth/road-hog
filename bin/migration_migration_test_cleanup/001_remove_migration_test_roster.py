"""Remove the temporary migration-test roster and its assets."""

from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"


def replace_once(path, old, new):
    text = path.read_text(encoding="utf-8")
    if old not in text:
        if new in text or (not new and "migration_test" not in text):
            return False
        raise RuntimeError(f"Expected text not found in {path}")
    updated = text.replace(old, new)
    if updated != text:
        path.write_text(updated, encoding="utf-8")
        print(f"Updated {path.relative_to(ROOT)}")
    return True


def main():
    replace_once(
        SRC / "road_hog.py",
        "from rosters import migration_test\n",
        "",
    )
    replace_once(
        SRC / "road_hog.py",
        "    roster_manager.add_roster(migration_test)\n",
        "",
    )
    replace_once(
        SRC / "utils.py",
        '"road-hog", "heqs", "migration_test", "id-report-only"',
        '"road-hog", "heqs", "id-report-only"',
    )
    replace_once(
        SRC / "lang" / "english.toml",
        'migration_test = "Migration Test"\n',
        "",
    )

    for path in (
        SRC / "rosters" / "migration_test.py",
        SRC / "vehicles" / "migration_test_bus.py",
    ):
        if path.exists():
            path.unlink()
            print(f"Deleted {path.relative_to(ROOT)}")

    graphics_dir = SRC / "graphics" / "migration_test"
    if graphics_dir.exists():
        files = {p.relative_to(graphics_dir).as_posix() for p in graphics_dir.rglob("*") if p.is_file()}
        if files != {"leyburn_pax.png"}:
            raise RuntimeError(f"Unexpected migration-test graphics: {sorted(files)}")
        shutil.rmtree(graphics_dir)
        print(f"Deleted {graphics_dir.relative_to(ROOT)}")

    # Report references anywhere else in tracked source, without modifying them.
    leftovers = []
    for path in SRC.rglob("*"):
        if path.is_file() and path.suffix in {".py", ".toml", ".pynml", ".lng"}:
            if "migration_test" in path.read_text(encoding="utf-8"):
                leftovers.append(path.relative_to(ROOT).as_posix())
    if leftovers:
        print("Remaining references (review):")
        for path in leftovers:
            print(f"  {path}")
    else:
        print("No remaining migration_test references in source text.")


if __name__ == "__main__":
    main()
