from road_vehicle import PaxLocalTramConsist, ElectricVehicleUnit

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(
        schema_name="PaxLocalTram",
        model_id="northbeach_pax",
        base_numeric_id=690,
        name="Northbeach",
        gen=4,
        intro_year_offset=1,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(
        base_platform=None,  # pax trams have no base platform by design currently
        unit_cls_name="ElectricVehicleUnit",
        vehicle_length=8,
        effects=["EFFECT_SPRITE_ELECTRIC, 0, 0, 12"],
        repeat=2,
    )

    return [model_def]
