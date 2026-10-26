from road_vehicle import PaxLocalTramConsist, ElectricVehicleUnit

from road_vehicle.model_def import ModelDef



def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="PaxLocalTram",
        model_id="newbold_pax",
        base_numeric_id=30,
        name="Newbold",
        gen=3,
        intro_year_offset=1,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(
        unit_cls_name="ElectricVehicleUnit",
        vehicle_length=8,
        effects=["EFFECT_SPRITE_ELECTRIC, 0, 0, 12"],
        repeat=2,
    )

    result.append(model_def)
    return result
