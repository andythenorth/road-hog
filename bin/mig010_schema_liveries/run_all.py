#!/usr/bin/env python3
"""Run from Road Hog repository root. Stages can also be invoked separately."""
from pathlib import Path
import runpy
for stage in ('010a_schema_liveries.py','010b_remove_model_liveries.py'):
    runpy.run_path(str(Path(__file__).with_name(stage)),run_name='__main__')
