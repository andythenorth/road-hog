from road_vehicle import FruitVegFeldbahnConsist

from road_vehicle.model_def import ModelDef

# CABBAGE DEFERRED: Pass 1 supports only vehicle_default.pynml.
# CABBAGE FUTURE PASS: restore legacy template choice and cargo-specific
# spritegroups/liveries where present in this vehicle.


def main(roster_id):
    model_def = ModelDef(
        schema_name="FruitVegFeldbahn",
        model_id="pippin_fruit_veg",
        base_numeric_id=1240,
        name="Pippin",
        gen=1,
    )

    model_def.add_unit_def(
        unit_cls_name="SteamEngineFeldbahnGen1A"
    )

    model_def.add_unit_def(
        unit_cls_name="WagonFeldbahnA", repeat=5
    )

    return [model_def]
