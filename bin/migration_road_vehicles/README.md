# Road Hog vehicle migration — consolidated pipeline

This package contains the full current migration scripts, **not** production source.
Pass 1 acceptance is successful original Makefile compilation for BOTH road-hog
and HEQS, followed by byte-for-byte source restoration and golden-reference protection.
Landrace parity is diagnostic only and is not a Pass 1 acceptance gate.

## Clean baseline run

The tracked `bin/` scripts may be committed on the existing branch. Run from
repository root; keep `generated.reference/` unchanged. `git reset --hard`
will discard uncommitted tracked changes, so use it only deliberately.

```sh
set +e
for stage in 000_check_golden 001_port_base_platform \
    002_verify_base_platform 003_inventory_fleet \
    005_provision_schemas 006_integrate_schema_behaviour \
    007_attempt_fleet_cutover; do
    python3 "bin/migration_road_vehicles/${stage}.py" || break
done
```

After all earlier stages pass, with `migration_state/stage_008_trial` absent:

```sh
python3 bin/migration_road_vehicles/008_trial_fleet_build.py --build --retain
python3 bin/migration_road_vehicles/008_verify_pass1_scope.py
python3 bin/migration_road_vehicles/008_audit_migration_bridges.py
```

**The Pass 1 gate requires both build reports, freshness and source restoration.**
The independent `008_verify_landrace_parity.py` may be run for diagnostics,
but its failure does not fail Pass 1. Inspect `migration_state/reports/`.

## Architecture / stage ownership

- 000: check the read-only golden reference.
- 001: BasePlatform, UnitDef and ModelDef infrastructure, plus scalar power,
  incomplete-sprite defaults, and read-only `chassis` migration bridge.
- 002: isolated platform contract verification.
- 003: inventory legacy vehicle files.
- 005: cargo-family schemas, track-type inheritance, power-specific unit
  classes and `loading_speed_multiplier=1` default.
- 006: behaviour integration; `unique_units`, sprite-row accounting and
  articulated NML ordering are `# CABBAGE MIGRATION SHIM` implementations.
- 007: guarded vehicle candidate generation, never production installation.
  Known obsolete sprite-row (3) and running-cost (2) arguments are preserved
  as `# CABBAGE` comments in candidates.
- 008: temporary in-place installation with durable backups and exact vehicle
  restoration, normal Makefile and compiler, fresh generated output snapshots.
  No trial compiler symlink or Makefile rewriting remains.
- 008_verify_landrace_parity: read-only verification of the successful fresh
  Landrace snapshot against `generated.reference/`. Exact NML, PNG pixel and
  language-file comparisons; **no silent compatibility allowances**.
- 008_audit_migration_bridges: CABBAGE marker and potential conditional bridge
  inventory for manual future-agent review.

Former Stages 009 and 010 are folded into 001; do not run separate 009/010.
No Stage 004 or Stage 011 is required.

## Safety and recovery

Stage 008 temporarily installs candidate files in `src/vehicles/` **only**
while running the build; it restores original bytes even on ordinary failure.
Do not edit source or start concurrent builds during Stage 008. The trial
refuses to overwrite a previous trial directory. After reviewing logs and
confirming the restore journal reports `restored: true`, remove the old trial
directory before rerunning.

In case of interruption before restoration, **do not reset Git**. Run:

```sh
python3 bin/migration_road_vehicles/008_trial_fleet_build.py --restore
```

`generated/` is disposable. `generated.reference/` must not be modified.
Stage 008 snapshots the trial outputs before starting a later roster's build;
it rejects generated outputs with timestamps predating that roster build.
Copied `generated/graphics/road-hog/roadtypes/*.png` assets are exempt from
timestamp freshness checks but are still snapshotted and pixel-compared by the
strict Landrace parity gate. Other stale outputs remain failures. No graphics pipeline or NML template edits are included.

## Shim retirement and completeness review

Read `CABBAGE_REVIEW.md` and run `008_audit_migration_bridges.py` for the
source-grounded bridge register and any conditional candidates requiring
manual review. Migration conditionals must carry `# CABBAGE MIGRATION SHIM:`
with a purpose and removal condition in their **owning earlier stage**.
The scanner does not prove complete annotation; unfamiliar conditionals are
left as review items rather than being automatically relabelled.

Strict parity may reveal intentional but unapproved historical changes,
including retired legacy cost adjustments. Report differences; do not
normalize them out. HEQS is intentionally excluded from strict parity.

### CABBAGE fresh parity evidence
Stage 008 runs `make clean` before both in-place roster builds. This discards only normal generated build artifacts using the repository Makefile, and verifies that `generated.reference/` is byte-identical after cleaning. The clean log is in `migration_state/stage_008_trial/build_clean.log`. A nonzero clean result prevents the build; original vehicle files are restored in all cases. The parity gate still requires freshly timed generated outputs; copied roadtype assets are compared by pixel content, not timestamp.

### NML filename reconciliation
Stage 008 parity pairs legacy `nml/<vehicle>.nml` with candidate `nml/<vehicle>_mv_0.nml` by vehicle name. It compares bytes exactly, reports any content differences, and counts renamed files separately. No NML identifier normalization or semantic parity waiver is performed. Missing or additional variant files still fail. The generated combined `road-hog.nml` is a build artifact, not a vehicle fragment.

CABBAGE Stage 008 NML parity: legacy vehicle symbols are compared to `_mv_0_unit_0` variant/unit symbols; only the specific intro-year comment spelling is reconciled. Other content remains strict.


## First-pass acceptance (stages 000–008 only)

The acceptance criterion is compilation using the original Makefile, not Landrace
feature parity. Stage 001 inserts a **CABBAGE** renderer-boundary shim that
forces `vehicle_default.pynml` but retains schema-provisioned GestaltGraphics.
Cargo-specific and visible-cargo templates are future migration work.

Run Stage 008 with `--build` (required):

```zsh
python3 bin/migration_road_vehicles/008_trial_fleet_build.py --build
python3 bin/migration_road_vehicles/008_verify_pass1_scope.py
```

Strict NML/PNG/language Landrace comparison may be run diagnostically, but is
**not** the Pass 1 acceptance gate. Do not run stages 009–011 in this pass.
Do not commit generated migrated `src/` as part of the migration-script commit.

## Compile-only fleet cutover (explicit, reversible)

After Stage 008 compile-only acceptance succeeds, Stage 008's trial restores all
132 vehicle files. Permanently install exactly the validated Stage 007 candidates:

```zsh
python3 bin/migration_road_vehicles/008_apply_fleet_cutover.py --check
python3 bin/migration_road_vehicles/008_apply_fleet_cutover.py --apply
```

This is a **CABBAGE** compile-only cutover, not parity approval. The cutover
refuses stale source files and records original bytes under
`migration_state/stage_008_cutover/originals/`, with a durable journal. If
interrupted, use `--rollback` before touching source files or resetting Git.

```zsh
python3 bin/migration_road_vehicles/008_apply_fleet_cutover.py --rollback
```

Once applied, inspect `git diff` and perform a post-cutover Makefile build before
committing migrated `src/`. The original Stage 008 trial remains read-only evidence;
rerunning it after cutover requires new Stage 007 candidate inventory.
