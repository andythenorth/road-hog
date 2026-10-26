"""Replace platform-instantiated UnitDefs with direct unit class declarations."""

import ast
import re
from pathlib import Path

ROOT = Path('src/vehicles')


def main():
    changes = 0
    for path in sorted(ROOT.glob('*.py')):
        original = path.read_text()
        text = original
        # Only a specific platform class reference is converted, not base_platform=None.
        pattern = re.compile(r'base_platform\s*=\s*([A-Za-z][A-Za-z0-9_]*)')
        for match in reversed(list(pattern.finditer(text))):
            cls = match.group(1)
            if cls == 'None':
                continue
            # Find the containing add_unit_def call by AST location.
            tree = ast.parse(text)
            candidate = None
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute) or node.func.attr != 'add_unit_def':
                    continue
                if node.lineno <= text.count('\n', 0, match.start()) + 1 <= node.end_lineno:
                    if any(k.arg == 'base_platform' and isinstance(k.value, ast.Name) and k.value.id == cls for k in node.keywords):
                        candidate = node
                        break
            if candidate is None:
                raise ValueError(f'Unrecognised platform reference: {path}: {cls}')
            start = sum(len(line) for line in text.splitlines(keepends=True)[:candidate.lineno - 1]) + candidate.col_offset
            end = sum(len(line) for line in text.splitlines(keepends=True)[:candidate.end_lineno - 1]) + candidate.end_col_offset
            segment = text[start:end]
            segment = re.sub(r'unit_cls_name\s*=\s*["\'][^"\']+["\']\s*,?\s*', '', segment, count=1)
            segment = re.sub(r'base_platform\s*=\s*'+re.escape(cls)+r'\b', f'unit_cls_name="{cls}"', segment, count=1)
            text = text[:start] + segment + text[end:]
        # Remove obsolete imports of now-resolved platform classes.
        text = re.sub(r'^from base_platforms\.[^\n]+\n', '', text, flags=re.M)
        text = re.sub(r'base_platform\s*=\s*None\s*,?\s*(?:# [^\n]*)?', '', text)
        if text != original:
            ast.parse(text)
            path.write_text(text)
            changes += 1
    print(f'Step 002: updated {changes} declaration files')


if __name__ == '__main__':
    main()
