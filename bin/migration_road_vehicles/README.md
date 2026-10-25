# Road Hog — cumulative vehicle migration tools

This is the complete AVAILABLE vehicle-migration script set, not the entire Road Hog source tree. Extract at the repository root. Do not run all numbered scripts on every invocation.

## Existing already-applied source stages

- 000 golden reference check (read-only)
- 001 BasePlatform integration (writes framework source; guarded, rerunnable)
- 002 platform integration assertions (read-only; isolates test from enabled roster imports)
- 003 vehicle inventory (writes report)
- 005 schema initializer hierarchy (writes schema source; guarded)
- 006 schema behavioural integration, including Bus sound_effect correction (writes schema source; guarded)

Stages 001/005/006 were applied before the reset in the user's checkout according to previous logs. Do NOT replay them just to conduct a fleet trial; their scripts are retained for reproducibility and review.

## Active fleet trial

- 007 generates fleet candidates and diagnostic report, leaves production vehicle files alone by default. NEVER run --install until contracts and golden parity are actually established.
- 008 copies all candidates to a disposable checkout, attempts both roster builds, captures logs, never edits working production definitions.

Run:

    python3 bin/migration_road_vehicles/007_attempt_fleet_cutover.py
    python3 bin/migration_road_vehicles/008_trial_fleet_build.py --build --retain

Stage 008 refuses to overwrite an existing migration_state/stage_008_trial directory. After preserving any useful logs, manually move it aside before a second run, e.g.:

    mv migration_state/stage_008_trial migration_state/stage_008_trial_previous

Then run 008 again. Do not move it onto an existing directory.

IMPORTANT: Both real rosters must be enabled in the working source before Stage 008 copies it. The generated vehicle candidates are still INCOMPLETE and are expected to fail; Stage 008 is diagnostic, not an accepted migration or parity pass.

## Removed as redundant

008a_fix_bus_sound_effect.py — incorporated into Stage 006, including support for partially applied Stage 006.


004_draft_all_vehicles.py — the later 007 generates the fleet candidate set itself, and 008 uses it directly. No 004 outputs are needed by 007 or 008.

README-00x.md fragments from earlier partial deliveries are replaced by this unified guide. Numeric filenames are retained rather than renumbered: reports, logs, and source hashes already refer to these identifiers.

## Safety boundaries

1. Verify golden reference separately; never regenerate/overwrite it as part of trial.
2. Infrastructure/schema source modifications remain separate, guarded stages.
3. Fleet conversion candidate generation never installs to source by default.
4. Trial build installs into an isolated copy; it is not a production cutover.
5. Golden comparisons and real installation are NOT implemented by this package. Do not claim completion or parity.

Nothing here alters graphics pipeline code. The package does not include generated.reference.zip, build assets, or source/vehicle files.

Stage 007 update: removes legacy roster_id=roster_id from ModelDef constructor candidates (including inline and Black-formatted kwargs). It does not change the main(roster_id) signature or production vehicle sources. Regenerate Stage 007 candidates before Stage 008.

## Stage 009: model power migration compatibility
Run after 006: `python3 bin/migration_road_vehicles/009_model_power_compatibility.py`.
Accepts legacy scalar `power` without changing its effective value, while keeping existing `power_by_power_source`. Both together are invalid; dictionary is not multi-mode runtime support. Source edits are guarded and idempotent. Rerun stages 007 and 008 afterwards.

## Stage 010: sprite completeness default
Run `python3 bin/migration_road_vehicles/010_default_sprites_incomplete.py` after 009, before 007. Existing Road Hog sprites are not complete; the ModelDef default is False. Stage 007 validates this default before conversion.

## Track-type mixin inheritance safety fix

On existing Stage 005/006 installations, rerun Stage 005. It repairs only the five mixin class headers and inserts TrackTypeMixinBase; it preserves all Stage 006 methods and other schema source. Fresh installations produce the correct hierarchy. This does not rewrite concrete schemas or RoadVehicleBase.

## Fleet dependency ordering and iterative repair
Stage 005 provisions cargo schemas, track-type mixins, and the three legacy
steam/diesel/electric unit classes. Stage 006 checks the unit implementation
against the legacy class declarations and produces a predicted compatibility
audit in `migration_state/reports/schema_stage_006.json`. Stage 007 checks
that the power-unit classes exist before generating candidate drafts.

When disposable Stage 008 builds reveal a missing shared class or attribute,
repair its owning earlier stage, then rerun **005, 006, 009, 010, 007, 008**.
The early steps are idempotent; Stage 008 requires explicit deletion of the
old disposable trial directory. This is an iterative development loop, *not*
a release acceptance test. Do not run Stage 007 with `--install` until both
builds and the golden reference comparison pass.

### CABBAGE obsolete sprite-row callers

Stage 007 comments out legacy `unit_num_providing_spriterow_num` arguments
in generated candidate files only. The original caller is preserved as a
`# CABBAGE` comment; the UnitDef contract and graphics pipeline are unchanged.
The Stage 007 JSON report counts these commented callers.

### Retired running-cost declarations and future API
Stage 007 comments out the two legacy `type_base_running_cost_points` caller arguments
with `# CABBAGE`, preserving their original values and balancing notes. The
Iron Horse `ModelDef.fixed_run_cost_points` field is already present in the
foundation and Stage 006 provides the `RoadVehicleBase.fixed_run_cost_points`
property (default 180). The current Road Hog running-cost calculation is
intentionally unchanged and does not yet consume that property.

CABBAGE Stage 006 installs two source-verified migration shims on RoadVehicleBase: `unique_units` and `get_spriterows_for_consist_or_subpart`. Both are temporary interfaces for the unchanged graphics pipelines, ported from legacy Consist. Run Stage 006 again before Stage 007/008 on existing installations.

### Stage 006 sprite-row shim repair

Stage 006 now saves `unique_units` and `get_spriterows_for_consist_or_subpart`
into `RoadVehicleBase` even if the prior Stage 006 marker exists. These are
`# CABBAGE MIGRATION SHIM` methods. It checks the saved AST before reporting
PASS and is idempotent. No graphics pipeline or vehicle definitions are changed.

For an already-migrated checkout, rerun Stage 006, then Stage 007 and Stage 008.
For a reset checkout, run the full numbered pipeline as documented above.

Stage 001 adds a read-only `RoadVehicleUnit.chassis` property, marked CABBAGE MIGRATION SHIM, forwarding to `UnitDef.chassis` for unchanged legacy graphics consumers.
