# Road Hog language migration

Run after the committed model/NML migration. No earlier stages need rerunning.

1. `python3 bin/migration_road_lang/000_port_roster_lang.py`
2. `python3 bin/migration_road_lang/001_verify_lang.py`

The reference directory must be named `lang.reference` at the repository root, with the old `.lng` files inside (nested subdirectories are fine).

Stage 000 changes only `src/roster.py`. Stage 001 runs the actual renderer, then compares each generated `.lng` file against the reference. Formatting whitespace and comment-only lines are ignored; language values and pragma fields must match.

CABBAGE If translation output differs because of meaningful version data, review the actual diff rather than suppressing the value.
