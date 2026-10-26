from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UNITS = ROOT / "src/road_vehicle/units.py"
VEHICLES = (
    "fairlop_pax.py",
    "brightling_open.py",
    "nettlebridge_dump.py",
    "oylbarral_tanker.py",
)

CLASS = '''\n\nclass ElectricTrailerUnit(RoadVehicleUnit):
    @property
    def effect_spawn_model(self):
        return "EFFECT_SPAWN_MODEL_ELECTRIC"
'''


def main():
    units_source = UNITS.read_text()
    if "class ElectricTrailerUnit(RoadVehicleUnit):" not in units_source:
        if "class ElectricVehicleUnit(RoadVehicleUnit):" not in units_source:
            raise RuntimeError("Expected Road Hog unit hierarchy not found")
        UNITS.write_text(units_source.rstrip() + CLASS + "\n")

    for name in VEHICLES:
        path = ROOT / "src/vehicles" / name
        source = path.read_text()
        old = 'unit_cls_name="RoadVehicleUnit",'
        new = 'unit_cls_name="ElectricTrailerUnit",'
        if new in source:
            continue
        if source.count(old) != 1:
            raise RuntimeError(f"Expected one generic trailing unit in {path}")
        path.write_text(source.replace(old, new))


if __name__ == "__main__":
    main()
