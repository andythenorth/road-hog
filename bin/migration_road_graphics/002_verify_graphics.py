"""Render the bus sprite sheet, then compare pixels if an old copy exists."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / 'generated/graphics/leyburn_pax.png'
REFERENCE = ROOT / 'graphics.reference/leyburn_pax.png'


def main():
    cmd = [sys.executable, 'src/render_graphics.py', '--pool_workers=0', '--grf-name=migration_test']
    print('RUN:', ' '.join(cmd), flush=True)
    subprocess.run(cmd, cwd=ROOT, check=True)
    if not OUTPUT.is_file():
        raise SystemExit(f'FAIL: expected graphics file missing: {OUTPUT}')
    from PIL import Image, ImageChops
    with Image.open(OUTPUT) as rendered:
        rendered.load()
        print(f'PASS: {OUTPUT.relative_to(ROOT)} produced, {rendered.size}, {rendered.mode}')
        if not REFERENCE.is_file():
            print('NOT VERIFIED: pixel parity (put old PNG at graphics.reference/leyburn_pax.png)')
            return
        with Image.open(REFERENCE) as original:
            original.load()
            if rendered.mode != original.mode or rendered.size != original.size:
                raise SystemExit('FAIL: old and new PNG modes or dimensions differ')
            if rendered.mode == 'P' and rendered.getpalette() != original.getpalette():
                raise SystemExit('FAIL: old and new PNG palettes differ')
            if ImageChops.difference(rendered, original).getbbox() is not None:
                raise SystemExit('FAIL: old and new PNG pixels differ')
            print('PASS: graphics pixels and palette match legacy reference')


if __name__ == '__main__':
    main()
