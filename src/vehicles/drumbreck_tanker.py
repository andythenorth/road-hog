from road_vehicle import TankerTramConsist
from base_platforms.trams import SteamEngineTram1

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(
        schema_name="TankerTram",
        model_id="drumbreck_tanker",
        base_numeric_id=800,
        name="Drumbreck",
        gen=1,
        intro_year_offset=4,
    )  # introduce later than gen epoch by design

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit", base_platform=SteamEngineTram1
    )

    model_def.add_unit_def(
        unit_cls_name="RoadVehicleUnit",
        base_platform=None,  # no base platform by design currently
        vehicle_length=4,
        repeat=3,
    )

    return [model_def]
