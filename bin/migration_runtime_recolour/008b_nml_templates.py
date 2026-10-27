#!/usr/bin/env python3
"""Install colour sprite data and road-feature random-bit helper; keep IH originals as references in bin."""
from pathlib import Path
here=Path(__file__).resolve().parent
out=Path('src/templates')
if not out.is_dir():raise SystemExit('Run from repo root')
road=(here/'alt_vars_random_bits.pynml').read_text().replace('FEAT_TRAINS','FEAT_ROADVEHS')
road='<!--! CABBAGE352: road feature variant; 0x5F lead-unit relative access needs NML compile and articulated testing -->\n'+road
payloads={'recolour_sprites.pynml':(here/'recolour_sprites.pynml').read_text(),
          'alt_vars_random_bits_road.pynml':road}
for name,content in payloads.items():
 p=out/name
 if p.exists() and p.read_text()!=content:raise SystemExit(f'CABBAGE352 template collision: {p}')
for name,content in payloads.items():
 p=out/name
 if not p.exists():p.write_text(content)
print('008b recolour sprite table and road random-bit helper staged; IH train originals remain in bin only')
