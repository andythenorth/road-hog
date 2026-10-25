# CABBAGE migration bridge register

This is the future-agent review entry point. **Do not remove a bridge simply
because Landrace compiles.** Compare fresh generated NML and PNGs against
`generated.reference/` first; HEQS is diagnostic only.

## Active bridge ownership

| Owner | Bridge or temporary compromise | Retirement test |
|---|---|---|
| 001 | `ModelDef.power` scalar alongside future `power_by_power_source`; conflict rejected | Define multi-power source model and verify all Road Hog costs |
| 001 | `sprites_complete=False` as current fleet-wide default | Sprite completeness tracked accurately for new vehicles |
| 001 | `RoadVehicleUnit.chassis` delegates to `unit_def.chassis` | Remaining graphics callers no longer access legacy unit attribute |
| 001 | Legacy `BasePlatform` reconfiguration semantics including `type` overrides, repeats, IDs | New contract and Golden parity tests replace old platform API |
| 005 | Legacy cargo-family schema initialisers and five inherited road/tram mixins | Source-grounded semantic parity for all families |
| 005 | Distinct Steam/Diesel/Electric unit classes and legacy parent side effects | Unit integration migrated without legacy state coupling |
| 005 | Base `loading_speed_multiplier=1` | Replaced by explicit stable schema default |
| 006 | `RoadVehicleBase.unique_units` | Graphics consumers use native model API |
| 006 | `get_spriterows_for_consist_or_subpart` | All graphics pipelines use native row accounting |
| 006 | Articulated callback emitted before unit NML | New rendering contract handles callback declaration ordering |
| 006 | `fixed_run_cost_points` exposed but intentionally unused | Running-cost migration receives explicit economic design decision |
| 007 | Legacy `roster_id` omitted from ModelDef constructor | All vehicle declarations written natively |
| 007 | `PaxLocalBusConsist` maps to `Bus` | Legacy schema names removed |
| 007 | Obsolete sprite-row override callers commented `CABBAGE` (3) | Vehicle definitions updated and reviewed |
| 007 | Legacy running-cost point callers commented `CABBAGE` (2) | Balance changes reviewed and accepted |
| 007 | Default unit classes inferred from legacy `add_unit()` | Explicit `UnitDef` classes for every vehicle |
| 008 | Temporary in-place candidate install, restore journal, fresh output snapshot | Cutover complete and generation parity certified |

## Important safety controls

- `generated.reference/` is read-only. Never normalize or overwrite it.
- `generated/` is disposable, and Stage 008 temporarily writes production
  vehicle files but restores their exact bytes; recovery is `008 ... --restore`.
- Stage 008 `--build --retain` **only certifies that build tools succeed**.
  Next run `008_verify_landrace_parity.py` for strict Landrace comparison.
- Stage 008 snapshots are accepted only with a positive freshness manifest.
  A stale file is a failed verification rather than implied parity.
- All differences are reported. No silent exclusions of renamed identifiers,
  costs, graphics switches, sprite rows, or dynamic version strings.
- To inspect additional conditions, run `008_audit_migration_bridges.py`.
  Review any `review_required=true` entries and annotate genuine shims **in the
  owning earlier stage**, with `# CABBAGE MIGRATION SHIM:` and a removal rule.
  Do not mechanically label all conditionals as legacy bridges.
- No modifications to the graphics pipelines or NML templates are intended.

## Acceptance checklist

1. Baseline source state clean; Stages 000, 001, 002, 003, 005, 006, 007.
2. Stage 008 completed and production vehicle bytes restored.
3. Landrace compiler and installer succeed.
4. `008_verify_landrace_parity.py` passes exact NML, pixel-identical PNGs,
   and byte-identical language files; all expected reference artifacts exist.
5. Audit every CABBAGE bridge before accepting production cutover.

- **Stage 008 copied roadtype asset freshness exception**: CABBAGE MIGRATION VERIFICATION. Landrace `graphics/road-hog/roadtypes/*.png` are copied, not regenerated. Exempt timestamps only; preserve full pixel parity. Retire if assets become generated outputs.

- CABBAGE Stage 008 NML symbol normalization: retire once the reference and generated NML use one naming convention. It never changes generated NML and does not mask other changes.
