"""Standardise Road Hog vehicle-module main() functions on result lists."""

import ast
import re
import tokenize
from pathlib import Path


VEHICLES_DIR = Path("src/vehicles")


def convert(path):
    with tokenize.open(path) as stream:
        source = stream.read()
        encoding = stream.encoding

    tree = ast.parse(source, filename=str(path))
    mains = [
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == "main"
    ]
    if len(mains) != 1:
        return False

    main = mains[0]
    returns = [node for node in ast.walk(main) if isinstance(node, ast.Return)]
    if len(returns) != 1:
        raise ValueError(f"Unexpected number of main() returns: {path}")

    ret = returns[0]
    if isinstance(ret.value, ast.Name) and ret.value.id == "result":
        return False
    if not (
        isinstance(ret.value, ast.List)
        and len(ret.value.elts) == 1
        and isinstance(ret.value.elts[0], ast.Name)
        and ret.value.elts[0].id == "model_def"
    ):
        raise ValueError(f"Unexpected main() return expression: {path}")

    lines = source.splitlines(keepends=True)
    return_line = lines[ret.lineno - 1]
    if not re.fullmatch(r"\s*return \[model_def\]\s*", return_line):
        raise ValueError(f"Unexpected return formatting: {path}")

    indent = " " * (ret.col_offset)
    newline = "\r\n" if "\r\n" in source else "\n"
    lines[ret.lineno - 1] = f"{indent}result.append(model_def){newline}{indent}return result{newline}"

    # Insert after any existing function docstring; otherwise at the start of main().
    if (
        main.body
        and isinstance(main.body[0], ast.Expr)
        and isinstance(main.body[0].value, ast.Constant)
        and isinstance(main.body[0].value.value, str)
    ):
        insert_at = main.body[0].end_lineno
    else:
        insert_at = main.body[0].lineno - 1

    lines.insert(insert_at, f"{indent}result = []{newline}{newline}")
    updated = "".join(lines)
    ast.parse(updated, filename=str(path))
    with open(path, "w", encoding=encoding, newline="") as output:
        output.write(updated)
    return True


def main():
    if not VEHICLES_DIR.is_dir():
        raise SystemExit("Run from the Road Hog repository root (src/vehicles missing)")

    updated = []
    for path in sorted(VEHICLES_DIR.glob("*.py")):
        if convert(path):
            updated.append(path)
    print(f"Standardised {len(updated)} vehicle modules")


if __name__ == "__main__":
    main()
