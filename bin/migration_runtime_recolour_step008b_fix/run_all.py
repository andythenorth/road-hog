#!/usr/bin/env python3
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name('008b_fix_temp_registers.py')), run_name='__main__')
