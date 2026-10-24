# CABBAGE Catalogue owns the numeric IDs. Do not allocate IDs in the roster.
"""Install road catalogue; keep excluded Iron Horse methods in source reference."""
from _common import PAYLOAD,write
write('src/road_vehicle/catalogue.py',(PAYLOAD/'road_vehicle/catalogue.py').read_bytes())
