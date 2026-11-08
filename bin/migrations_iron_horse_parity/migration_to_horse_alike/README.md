# Road Hog migration 000–007

Source based on uploaded Road Hog and Iron Horse snapshots. This is a test migration, not a fully verified GRF build.

- 000 install package and Iron Horse model def
- 001 catalogue identity/IDs
- 002 initial road schema/unit classes
- 003 install the declarative Leyburn test fixture as a whole-file payload; adapt roster to consume ModelDef lists
- 004 architecture checks
- **005 all template changes, once** (7 full template files)
- **006 NML schema and unit implementation** (NO template changes)
- 007 run full render_nml integration check

The 006 implementation is scoped to synthetic Leyburn (local diesel passenger bus). It does not claim general parity with all Road Hog vehicle classes. It has not been live-tested in your checkout, so stage 007 may fail. The original source of individual calculations remains in src/road_vehicle/__init__.py.

Use `git reset --hard` only if the migration scripts are stored outside the checkout or committed. `git clean -fd` can delete untracked scripts.


## CABBAGE Review notes

The payload contains more comments than production code would normally have.
Comments prefixed `CABBAGE` flag migration review or later human decisions.
The scripts change production source in-place. Keep the ZIP outside the checkout
before `git reset --hard`, then extract it again. Do not use `git clean -fd`
without checking which untracked files it will remove.

After stages 000–007 pass, copy the old build's NML to the repository root as
`migration_test.reference.nml`, and run:

```sh
python3 bin/migration_to_horse_alike/008_compare_reference_nml.py
```

008 compares the complete generated NML after the known Leyburn
model-variant/unit identifier rename and one template comment wording change are undone. Other differences (including
tractive effort, numeric IDs, property expressions, sprite paths) fail. The
reference NML is never overwritten or installed by migration scripts.

CABBAGE This comparison covers Leyburn only, not other vehicle types or a GRF
compiler run. A passing `render_nml.py` invocation is the end of this package.

### Stage 005 template comment correction

The template payload no longer emits CABBAGE review comments into generated NML.
The 005 installer accepts pristine templates, the immediately previous payload,
and the corrected payload. Other local edits are rejected.
Review comments remain in migration Python code. Run 005 after reset or run
it on a checkout carrying the previous Stage 005 payload.

### Declarative Leyburn at Stage 003

CABBAGE Leyburn is the only vehicle installed from a full source payload.
It uses the Iron Horse style: one ModelDef import, `main(**kwargs)` returns a
list of ModelDef, and it does not import Catalogue, schema classes or units.
The roster owns the Catalogue call. The later real Road Hog vehicle conversion
will use a separate migration pipeline; do not copy this fixture overwrite
pattern to production vehicle files.

CABBAGE Stage 002/006 now share the RoadVehicleBase → PassengerVehicle → Bus hierarchy. Stage 003 fixture declares Bus.

### Source-reference layout

CABBAGE Stage 000 no longer installs `src/road_vehicle/iron_horse_reference/`.
The original Iron Horse schema, unit, catalogue and livery sources stay under
`bin/migration_to_horse_alike/payload/road_vehicle/` for review.
They are not imported or executed by Road Hog. This reduces the source diff.

If you already ran an earlier Stage 000, reset and reapply this package;
Stage 000 does not remove previously installed reference files.
