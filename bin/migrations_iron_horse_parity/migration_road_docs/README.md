# Road Hog docs migration

Run after the committed model/NML, language and graphics migrations. Do not rerun those migrations.

Stages:

- 000: expose an intro year on the new schema for docs sorting
- 001: use ModelDef name and ID in the existing DocHelper
- 002: open the legacy graphics sprite filename from the new model ID
- 003: use DocHelper for the docs numeric ID table
- 004: run render_docs and check generated HTML and Leyburn docs images

Do not change graphics pipelines, sprite assets, the roster, or NML templates.

Run from repo root:

    for n in 000 001 002 003 004; do
        echo "=== DOCS $n ==="
        python3 bin/migration_road_docs/${n}_*.py || break
    done

CABBAGE Docs sorting now uses actual intro dates, not legacy Road Hog's 999 placeholder.
This is deliberately not claimed to be byte-for-byte old docs output.
