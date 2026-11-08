#!/usr/bin/env python3
"""Remove only redundant passenger ModelDef liveries; keep genuine overrides."""
from pathlib import Path
import ast

ROOT=Path('src/vehicles')
NAMES=(
 'RANDOM_LIVERIES_COMPLEMENT_COMPANY_COLOUR',
 'RANDOM_LIVERIES_CLOVER_OCHRE_SULPHUR',
 'RANDOM_LIVERIES_TEAL_PEWTER_SILVER',
)
PAX_SCHEMAS={'PaxLocalBusRuntimeRemapSpike','PaxLocalTramRuntimeRemapSpike','PaxExpressCoachRuntimeRemapSpike'}

def main():
    replacements={}
    seen=0
    for path in ROOT.glob('*.py'):
        original=path.read_text()
        tree=ast.parse(original, filename=str(path))
        calls=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='ModelDef']
        if not calls: continue
        if len(calls)!=1: raise RuntimeError(f'{path}: multiple ModelDef calls; review manually')
        kws={k.arg:k for k in calls[0].keywords}
        if 'schema_name' not in kws:continue
        schema=ast.literal_eval(kws['schema_name'].value)
        if schema not in PAX_SCHEMAS:continue
        seen+=1
        lv=kws.get('liveries')
        if lv is None: continue
        if tuple(ast.literal_eval(lv.value)) != NAMES:
            print(f'{path}: retaining explicit livery override')
            continue
        # Remove the whole keyword using token positions; do not touch other model properties.
        lines=original.splitlines(keepends=True)
        first=lv.lineno-1
        last=lv.end_lineno-1
        if not lines[first][:lv.col_offset].isspace(): raise RuntimeError(f'{path}: unexpected livery indentation')
        if lines[last][lv.end_col_offset:].strip()!=',': raise RuntimeError(f'{path}: livery keyword lacks trailing comma')
        del lines[first:last+1]
        # Remove stale migration comment, only if immediately preceding the keyword.
        if first>0 and first-1 < len(lines) and 'CABBAGE352' in lines[first-1] and ('catalogue' in lines[first-1] or '008d' in lines[first-1] or '008e' in lines[first-1] or '008f' in lines[first-1]):
            del lines[first-1]
        revised=''.join(lines)
        ast.parse(revised, filename=str(path))
        replacements[path]=revised
    if seen!=13:raise RuntimeError(f'Expected 13 passenger model files; found {seen}')
    for path, text in replacements.items(): path.write_text(text)
    print(f'010b: removed {len(replacements)} redundant model livery lists from {seen} passenger models')

if __name__=='__main__':main()
