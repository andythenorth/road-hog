#!/usr/bin/env python3
"""012: Align Road Hog ID validation/reporting with Iron Horse's ID blocks.

Run from the Road Hog repository root:
    python bin/mig012_id_block_parity/012_id_block_parity.py

Does not change declared base_numeric_id values or catalogue allocation.
"""

import ast
from pathlib import Path


def project_root():
    for parent in (Path.cwd(), *Path(__file__).resolve().parents):
        if (parent / "src" / "road_hog.py").is_file():
            return parent
    raise RuntimeError("Could not find Road Hog repository root")


def replace_method(source, class_name, method_names, replacement):
    tree = ast.parse(source)
    cls = next((n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == class_name), None)
    if cls is None:
        raise RuntimeError(f"Missing class {class_name}")
    method = next((n for n in cls.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name in method_names), None)
    if method is None:
        raise RuntimeError(f"Missing method {class_name}.{method_names}")
    lines = source.splitlines(keepends=True)
    start = method.lineno - 1
    if method.decorator_list:
        start = min(d.lineno for d in method.decorator_list) - 1
    lines[start:method.end_lineno] = [replacement.rstrip() + "\n"]
    return "".join(lines)


VALIDATE = '''    def validate_vehicle_ids(self, numeric_id_defender):
        # All rosters must have finished producing model variants and units.
        seen_variant_ids = set()
        collision_errors = []

        for model_variant in self.consists:
            if model_variant.id in seen_variant_ids:
                raise ValueError(f"Vehicle id '{model_variant.id}' is defined more than once")
            seen_variant_ids.add(model_variant.id)

            if not model_variant.units:
                raise ValueError(f"Vehicle '{model_variant.id}' has no units defined")

            base_id = model_variant.base_numeric_id
            if base_id % 10:
                raise ValueError(
                    f"{model_variant.id}: base_numeric_id {base_id} is not a multiple of 10"
                )

            numeric_ids = model_variant.catalogue_entry.unit_numeric_ids
            if len(model_variant.units) == 1:
                if base_id <= global_constants.max_articulated_id:
                    raise ValueError(
                        f"{model_variant.id}: base_numeric_id {base_id} must exceed "
                        f"{global_constants.max_articulated_id} for a single-unit vehicle"
                    )
            else:
                for numeric_id in numeric_ids:
                    if numeric_id > global_constants.max_articulated_id:
                        raise ValueError(
                            f"{model_variant.id}: articulated unit ID {numeric_id} exceeds "
                            f"{global_constants.max_articulated_id}"
                        )

            # All IDs occupy their containing block, not just IDs ending in zero.
            # Liveries within one catalogue may legitimately share a block.
            for block_id in {numeric_id - numeric_id % 10 for numeric_id in numeric_ids}:
                previous = numeric_id_defender.get(block_id)
                if previous is None:
                    numeric_id_defender[block_id] = model_variant
                elif previous.catalogue is not model_variant.catalogue:
                    collision_errors.append(
                        f"block {block_id}: {previous.id} ({previous.roster_id}) "
                        f"and {model_variant.id} ({model_variant.roster_id})"
                    )

        if collision_errors:
            raise ValueError("Vehicle ID block collisions:\\n" + "\\n".join(sorted(set(collision_errors))))
'''


def migrate_road_hog(source):
    # Also supports the preceding validation migration (dictionary already in use).
    if 'self.numeric_id_defender = []' in source:
        source = source.replace('self.numeric_id_defender = []', 'self.numeric_id_defender = {}')
    if 'roster.validate_vehicles(self.numeric_id_defender)' in source:
        source = source.replace('roster.validate_vehicles(self.numeric_id_defender)',
                                'roster.validate_vehicle_ids(self.numeric_id_defender)')
    if 'roster.validate_vehicle_ids(self.numeric_id_defender)' not in source:
        raise RuntimeError('Unexpected RosterManager validation call; inspect road_hog.py')
    return source


def migrate_roster(source):
    if 'def validate_vehicles(' not in source and 'def validate_vehicle_ids(' not in source:
        raise RuntimeError('Unknown roster validation method')
    return replace_method(source, 'Roster',
                          {'validate_vehicles', 'validate_vehicle_ids'}, VALIDATE)


def migrate_report(source):
    required = ('import iron_horse', 'iron_horse.main()', 'def find_vacant_id_runs(')
    if not all(term in source for term in required):
        raise RuntimeError('Unexpected id_report.py; inspect before migration')
    source = source.replace('import iron_horse', 'import road_hog')
    source = source.replace('iron_horse.main()', 'road_hog.main(validate_vehicle_ids=True)')
    # Function argument must be used; module global is accessed only in main().
    source = source.replace(
        'if id not in iron_horse.roster_manager.numeric_id_defender:',
        'if id not in numeric_id_defender:',
    )
    source = source.replace('iron_horse.roster_manager.numeric_id_defender',
                            'road_hog.roster_manager.numeric_id_defender')
    return source


def main():
    root = project_root()
    changes = (
        (root / 'src' / 'road_hog.py', migrate_road_hog),
        (root / 'src' / 'roster.py', migrate_roster),
        (root / 'src' / 'id_report.py', migrate_report),
    )
    updates = []
    for path, transform in changes:
        old = path.read_text(encoding='utf-8')
        new = transform(old)
        ast.parse(new, filename=str(path))
        updates.append((path, old, new))

    for path, old, new in updates:
        if new == old:
            print(f'Unchanged: {path.relative_to(root)}')
        else:
            path.write_text(new, encoding='utf-8')
            print(f'Updated:   {path.relative_to(root)}')
    print('No vehicle IDs have been reassigned.')


if __name__ == '__main__':
    main()
