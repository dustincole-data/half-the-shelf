"""Rasterise an SVG in out/ to a PNG beside it, via headless Chrome.

    python src/render.py shelf 1000 1250
"""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'out')
PROFILE = os.path.join(ROOT, '.chrome-profile')
CHROME = os.environ.get('CHROME', r'C:\Program Files\Google\Chrome\Application\chrome.exe')

name = sys.argv[1]
w = sys.argv[2] if len(sys.argv) > 2 else '1000'
h = sys.argv[3] if len(sys.argv) > 3 else '1250'
svg = os.path.join(OUT, name + '.svg')
png = os.path.join(OUT, name + '.png')
if not os.path.exists(svg):
    raise SystemExit('no such file: %s' % svg)

subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars',
                '--force-device-scale-factor=1', '--user-data-dir=' + PROFILE,
                '--window-size=%s,%s' % (w, h), '--screenshot=' + png,
                'file:///' + svg.replace('\\', '/')], check=True)
print(png, os.path.getsize(png) // 1024, 'kB')
