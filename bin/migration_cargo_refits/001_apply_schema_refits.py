#!/usr/bin/env python3
"""Road Hog cargo refit migration 001. Python 3.10+. No external dependencies."""
import argparse
import ast
import difflib
from pathlib import Path
import sys

TARGET = Path("src/road_vehicle/schemas.py")
# Only these three attributes may be changed; all other schema code is preserved.
RULES = {
    "BoxHaulerConsistBase": ("packaged_freight", "pf_allowed:legacy_box_freight", "pf_disallowed:legacy_disallowed_express"),
    "CoveredHopperHaulerConsistBase": ("covered_hopper_freight_any_grade", "keep", "keep"),
    "DumpHaulerConsistBase": ("open_bulk_non_food_grade", "keep", "keep"),
    "EdiblesTankerConsistBase": ("liquids_food_grade", "keep", "keep"),
    "FlatbedHaulerConsistBase": ("flatbed_freight", "keep", "keep"),
    "FruitVegHaulerConsistBase": ("", "keep", "keep"),
    "LivestockHaulerConsistBase": ("", "keep", "keep"),
    "LogHaulerConsistBase": ("", "keep", "keep"),
    "MailHaulerConsistBase": ("mail,express_freight", "empty", "pf_disallowed:legacy_disallowed_express"),
    "MetalHaulerConsistBase": ("", "keep", "keep"),
    "OpenHaulerConsistBase": ("all_freight", "empty", "pf_disallowed:legacy_disallowed_express"),
    "PaxHaulerConsistBase": ("pax", "empty", "empty"),
    "RefrigeratedHaulerConsistBase": ("refrigerated_freight", "empty", "empty"),
    "SuppliesHaulerConsistBase": ("", "keep", "keep"),
    "TankerConsistBase": ("liquids_non_food_grade", "keep", "keep"),
    "IntermodalHauler": ("all_freight", "empty", "pf_disallowed:legacy_disallowed_express"),
    "PassengerVehicle": ("pax", "empty", "empty"),
}
FIELDS = ("class_refit_groups", "label_refits_allowed", "label_refits_disallowed")
COMMENTS = {
    "MetalHaulerConsistBase": "        # CABBAGE: Consider consolidating specialist metal labels in Polar Fox.\n",
    "SuppliesHaulerConsistBase": "        # CABBAGE: Consider consolidating specialist supplies labels in Polar Fox.\n",
}
def rhs(spec, field):
    if field == "class_refit_groups":
        return repr(spec.split(",")) if spec else "[]"
    if spec == "keep":
        return None
    if spec == "empty":
        return "[]"
    prefix, key = spec.split(":", 1)
    dictionary = "allowed_refits_by_label" if prefix == "pf_allowed" else "disallowed_refits_by_label"
    return f'global_constants.{dictionary}["{key}"]'

def parse_classes(src):
    tree = ast.parse(src)
    return {n.name: n for n in tree.body if isinstance(n, ast.ClassDef)}

def assignments(cls):
    result = {}
    for method in cls.body:
        if not isinstance(method, ast.FunctionDef) or method.name != "__init__":
            continue
        for node in method.body:
            if isinstance(node, ast.Assign) and len(node.targets) == 1:
                target = node.targets[0]
                if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name) and target.value.id == "self" and target.attr in FIELDS:
                    if target.attr in result:
                        raise ValueError(f"Duplicate refit assignment: {cls.name}.{target.attr}")
                    result[target.attr] = node
    return result

def migrate(source):
    classes = parse_classes(source)
    missing = set(RULES) - set(classes)
    if missing:
        raise ValueError(f"Missing classes: {sorted(missing)}")
    lines = source.splitlines(keepends=True)
    edits = []
    for name, specs in RULES.items():
        cls = classes[name]
        found = assignments(cls)
        # PassengerVehicle is the only class which previously inherited all three rules.
        expected = set() if name == "PassengerVehicle" else set(FIELDS)
        if set(found) != expected and set(found) != set(FIELDS):
            raise ValueError(f"Unexpected refit fields for {name}: {sorted(found)}")
        if name == "PassengerVehicle" and not found:
            init = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == "__init__")
            supercall = init.body[0]
            if not isinstance(supercall, ast.Expr) or "super().__init__" not in ast.unparse(supercall):
                raise ValueError("PassengerVehicle constructor structure changed")
            insertion = "".join(f"        self.{field} = {rhs(spec,field)}\n" for field,spec in zip(FIELDS,specs))
            edits.append((supercall.end_lineno,supercall.end_lineno,insertion))
        else:
            for field, spec in zip(FIELDS,specs):
                node = found[field]
                old = ast.unparse(node.value)
                # Guard: legacy group lists were empty; exceptions explicitly preserved.
                if field == "class_refit_groups" and old not in ("[]", repr(spec.split(","))):
                    raise ValueError(f"Unexpected pre-existing class groups in {name}: {old}")
                new_rhs = rhs(spec,field)
                if new_rhs is None:
                    continue
                new = f"        self.{field} = {new_rhs}\n"
                current = "".join(lines[node.lineno-1:node.end_lineno])
                if current != new:
                    edits.append((node.lineno-1,node.end_lineno,new))
        if name in COMMENTS:
            # Insert immediately before the class refit assignment; no duplicated comment.
            comment = COMMENTS[name]
            if comment not in source:
                if "class_refit_groups" not in found:
                    raise ValueError(f"Missing comment insertion anchor in {name}")
                edits.append((found["class_refit_groups"].lineno-1,found["class_refit_groups"].lineno-1,comment))
    for start,end,replacement in sorted(edits,reverse=True):
        lines[start:end] = [replacement]
    result = "".join(lines)
    ast.parse(result)
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root",type=Path,default=Path("."))
    p.add_argument("--apply",action="store_true",help="Write the file; default is diff-only")
    args=p.parse_args()
    path=args.root/TARGET
    original=path.read_text(encoding="utf-8")
    updated=migrate(original)
    diff="".join(difflib.unified_diff(original.splitlines(keepends=True),updated.splitlines(keepends=True),fromfile=str(TARGET),tofile=str(TARGET)))
    if diff:
        print(diff,end="")
    else:
        print("No changes (already migrated).")
    if args.apply and updated != original:
        # Atomic replacement, preserving file mode. Never modify on failed validation.
        import os, tempfile
        fd,tmp=tempfile.mkstemp(prefix=".schemas-refits-",dir=path.parent)
        try:
            with os.fdopen(fd,"w",encoding="utf-8",newline="") as f:
                f.write(updated)
            os.chmod(tmp,path.stat().st_mode)
            os.replace(tmp,path)
        finally:
            if os.path.exists(tmp): os.unlink(tmp)
        print("Applied:",path)
    return 0
if __name__=="__main__":
    try: sys.exit(main())
    except (ValueError,SyntaxError,OSError) as exc:
        print(f"Migration aborted: {exc}",file=sys.stderr)
        sys.exit(1)
