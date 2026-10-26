from road_vehicle.model_def import ModelDef

# for each generation, bus and coach variants have same power and intro date
# coaches faster, lower capacity than equivalent bus


def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="Bus",
        model_id="leyburn_pax",
        base_numeric_id=20,
        name="Leyburn",
        power=100,  # custom power
        speed=40,
        gen=2,
        intro_year_offset=-1,
    )  # introduce earlier than gen epoch by design

    model_def.add_unit_def(
        unit_cls_name="DieselVehicleUnit",
        vehicle_length=7,
    )

    result.append(model_def)
    return result
