#!/usr/bin/env python3
"""Port immutable IH runtime colour definitions, utility and strings; safe to rerun."""
from pathlib import Path
import ast, re
root=Path.cwd(); here=Path(__file__).resolve().parent
files={k:root/k for k in ('src/global_constants.py','src/utils.py','src/lang/english.toml')}
for p in files.values():
    if not p.is_file(): raise SystemExit(f'Missing {p}; run from repo root')
constants=files['src/global_constants.py']; utils=files['src/utils.py']; lang=files['src/lang/english.toml']
c=constants.read_text(); u=utils.read_text(); l=lang.read_text()
cp=(here/'ih_runtime_colour_constants.py.txt').read_text()
up=(here/'ih_unpack_colour.py.txt').read_text()
lp=(here/'ih_livery_strings.toml.txt').read_text()
marker='# CABBAGE352 step 008a: IH runtime colour definitions (ordered)'
keys={'custom_wagon_recolour_sprite_maps','colour_sets','complements_to_company_colours','freight_wagon_liveries'}
found={t.id for n in ast.parse(c).body if isinstance(n,(ast.Assign,ast.AnnAssign)) for t in (n.targets if isinstance(n,ast.Assign) else [n.target]) if isinstance(t,ast.Name)}
# Compare exact previously-installed payload, not just names.
if marker in c:
    if c.split(marker,1)[1].strip()!=cp.strip():raise SystemExit('CABBAGE352 conflicting colour definitions')
elif keys & found:
    raise SystemExit('CABBAGE352 unexpected colour definitions: '+str(sorted(keys&found)))
else:c=c.rstrip()+'\n\n'+marker+'\n'+cp.rstrip()+'\n'
umarker='# CABBAGE352 step 008a: IH unpack_colour'
if umarker in u:
    if u.split(umarker,1)[1].strip()!=up.strip():raise SystemExit('CABBAGE352 conflicting unpack_colour')
elif any(isinstance(n,ast.FunctionDef) and n.name=='unpack_colour' for n in ast.parse(u).body):
    raise SystemExit('CABBAGE352 unexpected unpack_colour')
else:
    if not re.search(r'^import global_constants\s*$',u,re.M):raise SystemExit('CABBAGE352 missing global_constants import in utils')
    u=u.rstrip()+'\n\n'+umarker+'\n'+up.rstrip()+'\n'
lm='# CABBAGE352 step 008a: IH livery strings'
existing=dict((k,v) for k,v in re.findall(r'^\[([^]]+)\]\s*\n(.*?)(?=^\[|\Z)',l,re.M|re.S))
incoming=dict((k,v) for k,v in re.findall(r'^\[([^]]+)\]\s*\n(.*?)(?=^\[|\Z)',lp,re.M|re.S))
coll=existing.keys()&incoming.keys()
if coll:
    if any(existing[k].strip()!=incoming[k].strip() for k in coll):raise SystemExit('CABBAGE352 conflicting lang keys: '+str(sorted(coll)))
    if coll!=incoming.keys():raise SystemExit('CABBAGE352 partial language import; inspect')
else:l=l.rstrip()+'\n\n'+lm+'\n'+lp.rstrip()+'\n'
# All preflight tests done before writes.
for p,value in [(constants,c),(utils,u),(lang,l)]:
    if p.read_text()!=value:p.write_text(value)
print('008a colour data / utils / strings OK')
