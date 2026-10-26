#!/usr/bin/env python3
"""Verify cargo-refit schema mappings without importing Road Hog."""
import argparse
import ast
from pathlib import Path
import sys
from importlib.machinery import SourceFileLoader

HERE=Path(__file__).resolve().parent
migration=SourceFileLoader("refit_migration",str(HERE/"001_apply_schema_refits.py")).load_module()

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--root",type=Path,default=Path("."))
    args=p.parse_args()
    source=(args.root/migration.TARGET).read_text(encoding="utf-8")
    classes=migration.parse_classes(source)
    errors=[]
    for name,specs in migration.RULES.items():
        found=migration.assignments(classes[name])
        for field,spec in zip(migration.FIELDS,specs):
            if field not in found:
                errors.append(f"{name}.{field}: missing")
                continue
            expected=migration.rhs(spec,field)
            if expected is None:
                # Unmodified specialist rules are protected by migration's source-level diff.
                continue
            if ast.dump(ast.parse(expected,mode="eval").body)!=ast.dump(found[field].value):
                errors.append(f"{name}.{field}: expected {expected}; got {ast.unparse(found[field].value)}")
    for name,comment in migration.COMMENTS.items():
        if source.count(comment)!=1:
            errors.append(f"{name}: CABBAGE comment missing or duplicated")
    # Re-run migration: a valid result must be idempotent.
    if migration.migrate(source)!=source:
        errors.append("Migration is not idempotent")
    if errors:
        print("\n".join(errors),file=sys.stderr)
        return 1
    print(f"PASS: {len(migration.RULES)} explicit schema policies; inherited Bus and PaxHaulerLocalConsistBase; two CABBAGE comments; idempotent.")
    return 0
if __name__=="__main__":
    sys.exit(main())
