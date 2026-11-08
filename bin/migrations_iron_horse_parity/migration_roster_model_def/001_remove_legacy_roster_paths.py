"""Remove the legacy roster paths."""

from pathlib import Path


PATH = Path("src/roster.py")

OLD_LOAD = '''        for vehicle in self.consists_uninitialised:
            # CABBAGE When all vehicle files return ModelDef lists this legacy
            # CABBAGE single-consist branch can be removed.
            result = vehicle.main(roster_id=self.id)
            if isinstance(result, list):
                for model_def in result:
                    if not isinstance(model_def, ModelDef):
                        raise TypeError(
                            f"{vehicle.__name__}.main returned a non-ModelDef item"
                        )
                    # Catalogue owns the model/variant/unit IDs. The roster
                    # only requests produced variants and keeps their order.
                    catalogue = Catalogue(model_def, roster_id=self.id)
                    self.consists.extend(
                        catalogue.produce(entry) for entry in catalogue
                    )
            else:
                self.consists.append(result)
'''

INTERIM_LOAD = '''        for vehicle in self.consists_uninitialised:
            for model_def in vehicle.main(roster_id=self.id):
                if not isinstance(model_def, ModelDef):
                    raise TypeError(
                        f"{vehicle.__name__}.main returned a non-ModelDef item"
                    )
                # Catalogue owns the model/variant/unit IDs. The roster
                # only requests produced variants and keeps their order.
                catalogue = Catalogue(model_def, roster_id=self.id)
                self.consists.extend(catalogue.produce(entry) for entry in catalogue)
'''

NEW_LOAD = '''        for vehicle in self.consists_uninitialised:
            for model_def in vehicle.main(roster_id=self.id):
                catalogue = Catalogue(model_def, roster_id=self.id)
                self.consists.extend(catalogue.produce(entry) for entry in catalogue)
'''

OLD_LANG = '''        for consist in self.consists_in_buy_menu_order:
            # Road Hog legacy vehicles own _name and id. New catalogue vehicles
            # get their name and base model ID from ModelDef instead.
            # CABBAGE Keep both paths until the old vehicle definitions are ported.
            model_def = getattr(consist, "model_def", None)
            if model_def is not None:
                name = model_def.name
                model_id = model_def.model_id
            else:
                name = consist._name
                model_id = consist.id
            if name is not None:
                lang_strings["STR_NAME_" + model_id.upper()] = name
'''

NEW_LANG = '''        for consist in self.consists_in_buy_menu_order:
            model_def = consist.model_def
            if model_def.name is not None:
                lang_strings["STR_NAME_" + model_def.model_id.upper()] = model_def.name
'''


def replace_one(source, old_values, new_value, label):
    if new_value in source:
        return source
    matches = [old for old in old_values if old in source]
    if len(matches) != 1 or source.count(matches[0]) != 1:
        raise RuntimeError(f"Unexpected {label} layout in {PATH}")
    return source.replace(matches[0], new_value, 1)


def main():
    source = PATH.read_text(encoding="utf-8")
    updated = replace_one(source, (OLD_LOAD, INTERIM_LOAD), NEW_LOAD, "loader")
    updated = replace_one(updated, (OLD_LANG,), NEW_LANG, "language")
    # ModelDef is no longer needed by the roster.
    updated = updated.replace("        from road_vehicle.model_def import ModelDef\n", "")
    if updated != source:
        PATH.write_text(updated, encoding="utf-8")
        print(f"Updated {PATH}")
    else:
        print(f"Already migrated: {PATH}")


if __name__ == "__main__":
    main()
