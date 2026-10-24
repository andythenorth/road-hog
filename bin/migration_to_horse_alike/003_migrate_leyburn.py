"""Install the small, declarative Leyburn fixture and accept ModelDef in roster.

CABBAGE Production vehicle definitions need their own converter later.
"""
from _common import ROOT, PAYLOAD, write

fixture = ROOT / "src/vehicles/migration_test_bus.py"
original = '"""One existing-equivalent vehicle for testing the migration factory path.\n\nRetain the original Leyburn IDs and graphics lookup until the new framework\nis wired up. This definition is deliberately in Road Hog\'s legacy format.\n"""\n\nfrom road_vehicle import PaxLocalBusConsist, DieselVehicleUnit\n\n\ndef main(roster_id):\n    consist = PaxLocalBusConsist(\n        roster_id=roster_id,\n        id="leyburn_pax",\n        base_numeric_id=20,\n        name="Leyburn",\n        power=100,\n        speed=40,\n        gen=2,\n        intro_date_offset=-1,\n    )\n    consist.add_unit(\n        base_platform=None,\n        type=DieselVehicleUnit,\n        vehicle_length=7,\n    )\n    return consist\n'
new = (PAYLOAD / "vehicles/migration_test_bus.py").read_text()
if fixture.read_text() == original:
    fixture.write_text(new)
elif fixture.read_text() != new:
    raise RuntimeError("Unexpected Leyburn file. Stage 003 refuses to replace it.")

# CABBAGE This is the actual common roster boundary. It accepts Iron Horse-style
# CABBAGE lists of ModelDef, but keeps legacy Road Hog vehicle modules working.
roster = ROOT / "src/roster.py"
old = '        for vehicle in self.consists_uninitialised:\n            consist = vehicle.main(self.id)\n            self.consists.append(consist)'
replacement = '        from road_vehicle.model_def import ModelDef\n        from road_vehicle.catalogue import Catalogue\n\n        for vehicle in self.consists_uninitialised:\n            # CABBAGE When all vehicle files return ModelDef lists this legacy\n            # CABBAGE single-consist branch can be removed.\n            result = vehicle.main(roster_id=self.id)\n            if isinstance(result, list):\n                for model_def in result:\n                    if not isinstance(model_def, ModelDef):\n                        raise TypeError(\n                            f"{vehicle.__name__}.main returned a non-ModelDef item"\n                        )\n                    # Catalogue owns the model/variant/unit IDs. The roster\n                    # only requests produced variants and keeps their order.\n                    catalogue = Catalogue(model_def, roster_id=self.id)\n                    self.consists.extend(\n                        catalogue.produce(entry) for entry in catalogue\n                    )\n            else:\n                self.consists.append(result)'
source = roster.read_text()
if old in source and replacement not in source:
    if source.count(old) != 1:
        raise RuntimeError("Roster seam occurs more than once")
    roster.write_text(source.replace(old, replacement))
elif replacement not in source:
    raise RuntimeError("Unexpected roster implementation; refusing guessed change")
print("PASS: declarative Leyburn fixture, roster creates variants using Catalogue")
