"""New unit objects with catalogue-owned identity."""
class RoadVehicleUnit:
    def __init__(self,model_variant,unit_def,id,numeric_id):
        self.model_variant=model_variant
        self.unit_def=unit_def
        self.id=id
        self.numeric_id=numeric_id

class DieselVehicleUnit(RoadVehicleUnit):
    pass
