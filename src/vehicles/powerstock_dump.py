from road_vehicle import DumpTruckConsist

from road_vehicle.model_def import ModelDef



def main(roster_id):
    result = []

    model_def = ModelDef(
        schema_name="DumpTruck",
        model_id="powerstock_dump",
        base_numeric_id=340,
        name="Powerstock",
        gen=5,
        intro_year_offset=4,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(
        unit_cls_name="DieselCaboverSemiTractorTruckGen5A",
    )

    model_def.add_unit_def(unit_cls_name="RoadVehicleUnit", vehicle_length=7)

    result.append(model_def)
    return result
