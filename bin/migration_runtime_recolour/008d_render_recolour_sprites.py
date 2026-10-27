#!/usr/bin/env python3
"""Enable IH custom recolour sprites in the NML header (full data ordering)."""
from pathlib import Path
import ast
p=Path('src/render_nml.py')
if not p.is_file():raise SystemExit('Run from repo root')
t=p.read_text()
anchor='    header_items = ["header", "cargo_table", "roadtypes_tramtypes"]'
repl="""    # CABBAGE352: IH recolour sprite table, before road-vehicle items.\n    # Complete wagon strategy template is staged, but its IH badge/parameter\n    # dependencies must be adapted before it can be included in generated NML.\n    header_items = ["header", "cargo_table", "roadtypes_tramtypes", "recolour_sprites"]"""
if repl not in t:
    if t.count(anchor)!=1:raise SystemExit('CABBAGE352 render_nml header anchor changed')
    t=t.replace(anchor,repl)
ast.parse(t)
if p.read_text()!=t:p.write_text(t)
print('008d full IH recolour sprite table enabled; wagon procedures staged OK')
