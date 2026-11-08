"""Small schema hierarchy for Road Hog model variants.

CABBAGE Stage 002 only installs structure. Stage 006 adds road NML methods.
"""


class RoadVehicleBase:
    def __init__(self, producer, catalogue_entry):
        self.producer = producer
        self.catalogue_entry = catalogue_entry
        self.model_def = producer.catalogue.model_def
        self.units = []
        self.id = catalogue_entry.model_variant_id

    def render(self, templates, graphics_path):
        raise NotImplementedError("RoadVehicle NML methods are installed by Stage 006")


class PassengerVehicle(RoadVehicleBase):
    """Common passenger stuff, buses and other pax vehicles will use this."""


class Bus(PassengerVehicle):
    """Bus defaults. There may be more later when we convert the fleet."""
