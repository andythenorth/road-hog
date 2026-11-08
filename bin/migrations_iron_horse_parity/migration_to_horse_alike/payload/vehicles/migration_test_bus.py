"""Leyburn bus for testing the new model path.

CABBAGE This is a test vehicle, not the converter for the rest of Road Hog.
"""
from road_vehicle.model_def import ModelDef


def main(**kwargs):
    model_def = ModelDef(
        schema_name="Bus",
        model_id="leyburn_pax",
        base_numeric_id=20,
        name="Leyburn",
        gen=2,
        sprites_complete=True,
        speed=40,
        power_by_power_source={"DIESEL": 100},
        intro_year_offset=-1,
    )
    model_def.add_unit_def(
        unit_cls_name="DieselVehicleUnit",
        vehicle_length=7,
    )
    return [model_def]
