from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class LiveryDef:
    livery_name: str
    colour_set_names: List = field(default_factory=list)
    docs_image_input_cc: Optional[List] = None
    is_freight_wagon_livery: Optional[bool] = False
    purchase_swatch_colour_set_names: List = field(default_factory=list)
    proxy_livery_for_badge_display_and_filter: Optional[str] = None
    has_predrawn_badge_sprite: Optional[bool] = False
    relative_spriterow_num: Optional[int] = None
    remap_to_cc: Optional[str] = None
    use_weathering: Optional[bool] = False

    @property
    def purchase_swatch(self):
        if not self.is_freight_wagon_livery:
            return None
        if self.purchase_swatch_colour_set_names:
            return self.purchase_swatch_colour_set_names
        return list(set(self.colour_set_names))

    @property
    def display_and_filter_name(self):
        return self.proxy_livery_for_badge_display_and_filter or self.livery_name

    @property
    def display_and_filter_name_badge_label(self):
        return f"livery/iron_horse/{self.display_and_filter_name.lower()}"

    @property
    def internal_name_badge_label(self):
        return f"_ih_livery_def/internal_livery_name/{self.livery_name.lower()}"

    @property
    def weathering_badge_label(self):
        return f"_ih_livery_def/use_weathering/{self.use_weathering}"
