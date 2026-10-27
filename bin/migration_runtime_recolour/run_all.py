#!/usr/bin/env python3
"""Full repeatable step 008 infrastructure migration from clean RH checkout."""
import subprocess,sys
from pathlib import Path
here=Path(__file__).resolve().parent
for script in ('008a_colour_data.py','008b_nml_templates.py','008c_callbacks_and_graphics.py','008d_render_recolour_sprites.py'):
 subprocess.run([sys.executable,str(here/script)],check=True)
print('Step 008 infrastructure complete. Runtime livery selection NOT activated; no vehicle declarations changed.')
