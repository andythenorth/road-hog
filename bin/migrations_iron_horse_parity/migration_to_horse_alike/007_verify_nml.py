"""Check post-migration NML generation; do not modify repository source."""
import os, subprocess, sys
from _common import ROOT
command=[sys.executable,'src/render_nml.py','--pool_workers=16','--grf-name=migration_test']
result=subprocess.run(command,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
print(result.stdout)
if result.returncode: raise SystemExit(result.returncode)
p=ROOT/'generated/migration_test.nml'
if not p.exists() or 'item(FEAT_ROADVEHS' not in p.read_text():
 raise SystemExit('NML missing real road vehicle items')
print('PASS: render_nml.py wrote road vehicle item NML')
