#!/usr/bin/env python3
"""Migration 002: resolve Polar Fox cargo classes like Iron Horse, at unit call sites."""
import argparse
import ast
import difflib
import os
from pathlib import Path
import tempfile
import sys

UNIT = Path("src/road_vehicle/units.py")
SCHEMA = Path("src/road_vehicle/schemas.py")
TEMPLATE = Path("src/templates/properties.pynml")
METHOD = """    def get_cargo_classes_as_nml_prop(self, allow_disallow_key):
        result = []
        for class_refit_group in self.model_variant.class_refit_groups:
            for cargo_class in global_constants.base_refits_by_class[
                class_refit_group
            ][allow_disallow_key]:
                result.append(cargo_class)
        return "bitmask(" + ",".join(result) + ")"

"""
OLD_SCHEMA = """    @property
    def refittable_classes(self):
        return ",".join(
            set(
                c
                for group in self.class_refit_groups
                for c in global_constants.base_refits_by_class[group]
            )
        )

"""
OLD_ALLOWED = "refittable_cargo_classes:       bitmask(${model_variant.refittable_classes});"
OLD_DISALLOWED = "non_refittable_cargo_classes:   bitmask(); // don't set non-refittable classes, increases likelihood of breaking cargo support"
NEW_ALLOWED = 'refittable_cargo_classes:       ${unit.get_cargo_classes_as_nml_prop("allowed")};'
NEW_DISALLOWED = 'non_refittable_cargo_classes:   ${unit.get_cargo_classes_as_nml_prop("disallowed")};'

def transform(files):
    units, schema, template = (files[k] for k in (UNIT,SCHEMA,TEMPLATE))
    if METHOD not in units:
        tree=ast.parse(units)
        cls=next((n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=="RoadVehicleUnit"),None)
        if cls is None or any(isinstance(n,ast.FunctionDef) and n.name=="get_cargo_classes_as_nml_prop" for n in cls.body):
            raise ValueError("Unexpected RoadVehicleUnit structure")
        anchor="    @property\n    def chassis(self):"
        if units.count(anchor)!=1: raise ValueError("Missing/ambiguous unit insertion anchor")
        units=units.replace(anchor,METHOD+anchor)
    if OLD_SCHEMA in schema:
        schema=schema.replace(OLD_SCHEMA,"")
    elif "def refittable_classes(self):" in schema:
        raise ValueError("Unexpected schema refittable_classes implementation")
    if OLD_ALLOWED in template and OLD_DISALLOWED in template:
        template=template.replace(OLD_ALLOWED,NEW_ALLOWED).replace(OLD_DISALLOWED,NEW_DISALLOWED)
    elif NEW_ALLOWED not in template or NEW_DISALLOWED not in template:
        raise ValueError("Unexpected template refit call sites")
    for text in (units,schema): ast.parse(text)
    return {UNIT:units,SCHEMA:schema,TEMPLATE:template}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--root",type=Path,default=Path("."))
    p.add_argument("--apply",action="store_true")
    args=p.parse_args()
    paths={k:args.root/k for k in (UNIT,SCHEMA,TEMPLATE)}
    original={k:v.read_text(encoding="utf-8") for k,v in paths.items()}
    updated=transform(original)
    for k in paths:
        diff="".join(difflib.unified_diff(original[k].splitlines(keepends=True),updated[k].splitlines(keepends=True),fromfile=str(k),tofile=str(k)))
        if diff: print(diff,end="")
    if not args.apply:
        return
    # Validate all content before touching files; stage replacements before committing.
    staged={}
    try:
        for k,path in paths.items():
            if updated[k]==original[k]: continue
            fd,tmp=tempfile.mkstemp(prefix=".refit002-",dir=path.parent)
            staged[k]=Path(tmp)
            with os.fdopen(fd,"w",encoding="utf-8",newline="") as f: f.write(updated[k])
            os.chmod(tmp,path.stat().st_mode)
        for k,tmp in staged.items(): os.replace(tmp,paths[k])
    finally:
        for tmp in staged.values():
            if tmp.exists(): tmp.unlink()
    print("Applied migration 002")
if __name__=="__main__":
    try: main()
    except (ValueError,SyntaxError,OSError) as e:
        print(f"Migration 002 aborted: {e}",file=sys.stderr)
        sys.exit(1)
