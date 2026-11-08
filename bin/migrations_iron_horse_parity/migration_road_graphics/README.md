# Road Hog graphics migration (after NML and language commits)

Only `src/road_vehicle/schemas.py` and `src/render_graphics.py` are edited.
`src/gestalt_graphics/`, graphics assets, constants and NML templates are not changed.

Run from the repository root:

```sh
python3 bin/migration_road_graphics/000_schema_graphics.py && \
python3 bin/migration_road_graphics/001_renderer_boundary.py && \
python3 bin/migration_road_graphics/002_verify_graphics.py
```

Validation uses `PW=0` for clear errors. This makes the real, existing
`CheckBuyMenuOnlyPipeline` run. The output is expected at
`generated/graphics/leyburn_pax.png` (that path comes from the old pipeline).
For old/new pixel parity, place the old PNG at
`graphics.reference/migration_test/leyburn_pax.png`.

CABBAGE: Only Leyburn (single diesel bus, default sprite pipeline) has been
considered here. Do not infer that multi-unit or visible-cargo graphics work.

If any pipeline interface fails, review the source. Do not patch the pipeline
without explicit approval.
