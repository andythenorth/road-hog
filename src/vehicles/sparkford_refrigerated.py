from road_vehicle import RefrigeratedTramConsist, ElectricVehicleUnit

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(
        schema_name="RefrigeratedTram",
        model_id="sparkford_refrigerated",
        base_numeric_id=390,
        name="Sparkford",
        gen=3,
        intro_year_offset=10,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(
        base_platform=None,  # no base platform by design currently
        unit_cls_name="ElectricVehicleUnit",
        vehicle_length=8,
        repeat=2,
    )

    return [model_def]
