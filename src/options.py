"""Build the one-screen gate: every treatment as a poster thumbnail plus a 1:1 detail strip.

    python src/options.py            -> out/options.png

The strip is the whole argument. Row 1 is the eight archetypes at 130px (the top shelf), row 2 is
the same eight at 37px (the tail), row 3 is a real slice of the ninety at 37px and chroma 0.50 —
because the only question that matters is whether that row is still a picket fence.
"""
import os, subprocess, sys

os.environ.setdefault('PYTHONHASHSEED', '0')
if os.environ.get('PYTHONHASHSEED') == '0' and not os.environ.get('_HASHED'):
    os.environ['_HASHED'] = '1'
    sys.exit(subprocess.run([sys.executable] + sys.argv, env=os.environ).returncode)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout import *
import treatments
from treatments import OPTIONS, KINDS, GROUND, INK

SRC = os.path.dirname(os.path.abspath(__file__))
PW_T, PH_T = 1000, 1250
THUMB = 268                                          # poster thumbnail width, in the sheet
SW, SH = 706, 334                                    # detail strip, drawn and shown 1:1
HEAD_H, H2_H, PAD = 140, 42, 36                      # fixed, so the sheet height is exact
THUMB_H = int(round(THUMB * PH_T / float(PW_T)))
ROW_H = PAD + H2_H + max(THUMB_H, SH)
SHEET_W = 40 + THUMB + 30 + SW + 40

h_of = lambda u: 20 + 17.0 * math.sqrt(u)
items = sorted(USE.items(), key=lambda kv: (-kv[1], kv[0]))

# one real ingredient per archetype, so the colour in the strip is the colour on the page
SPECIMEN = {'tall': 'gin', 'short': 'sweet vermouth', 'dash': 'angostura bitters',
            'jar': 'sugar syrup', 'can': 'soda water', 'citrus': 'lemon juice',
            'cherry': 'maraschino cherry', 'sprig': 'mint'}
TAIL = [nm for nm, u in items if u == 1][::4]        # 23 of the ninety, spread across the shelf


def strip(T):
    """The 1:1 detail strip for one treatment."""
    g = [paper(4, 220, col='#4A4234', op=0.030, w=SW, h=SH, rmax=1.2)]

    def row(names, h, by, chroma, fine, gap):
        ws = [T.width(kind_of(n), h) for n in names]
        x = (SW - sum(ws) - gap * (len(names) - 1)) / 2
        g.append('<path d="%s" stroke="%s" stroke-width="%.1f" fill="none" opacity="%.2f" '
                 'stroke-linecap="round"/>'
                 % (rough_line(18, by + 3, SW - 18, by + 4, 1.2, random.Random(3)), INK,
                    2.4 if chroma > 0.7 else 1.6, 0.8 if chroma > 0.7 else 0.38))
        for n, w in zip(names, ws):
            sv, _ = T.render(n, h, x + w / 2, by, chroma, hash(n) & 0xffff, fine=fine)
            g.append(sv)
            x += w + gap

    row([SPECIMEN[k] for k in KINDS], 130, 160, 1.00, True, 15)      # top shelf, full chroma
    row([SPECIMEN[k] for k in KINDS], 37, 232, 1.00, False, 15)      # the same eight, tail size
    row(TAIL, 37, 304, 0.50, False, 4.4)                             # the real ninety, at 50%
    for lab, y in (('130 px \u00b7 top shelf', 178), ('37 px', 250),
                   ('37 px \u00b7 the ninety, at half chroma', 322)):
        g.append(txt(18, y, lab, 8.6, INK, op=0.42, track=0.8))
    return svg_open(SW, SH, GROUND) + ''.join(g) + '</svg>'


def build():
    for T in OPTIONS:
        env = dict(os.environ, TREATMENT=T.key, SHELF_OUT='opt-' + T.key)
        subprocess.run([sys.executable, 'shelf.py'], cwd=SRC, env=env, check=True,
                       stdout=subprocess.DEVNULL)
        subprocess.run([sys.executable, 'render.py', 'opt-' + T.key, str(PW_T), str(PH_T)],
                       cwd=SRC, env=env, check=True, stdout=subprocess.DEVNULL)
        open(os.path.join(OUT, 'strip-%s.svg' % T.key), 'w', encoding='utf-8').write(strip(T))
        print('built', T.key)

    rows = []
    for i, T in enumerate(OPTIONS):
        rows.append(
            '<section><h2><b>%s</b><span>%s</span></h2>'
            '<div class="r"><img class="t" src="opt-%s.png"><img class="s" src="strip-%s.svg">'
            '</div></section>' % (esc(T.title), esc(T.note), T.key, T.key))

    html = ("""<!doctype html><meta charset="utf-8"><style>
 *{margin:0;padding:0;box-sizing:border-box}
 body{width:%dpx;background:#EFEDE8;font:400 13px/1.45 'Century Gothic',Futura,sans-serif;
      color:#2E2A24}
 header{height:%dpx;padding:30px 40px 0}
 header h1{font-size:25px;font-weight:400;letter-spacing:.2px}
 header p{font-size:12.5px;opacity:.62;margin-top:7px;max-width:940px}
 section{height:%dpx;padding:16px 40px 0}
 section+section{border-top:1px solid #DAD6CE}
 h2{font-size:12px;font-weight:400;letter-spacing:1.6px;text-transform:uppercase;
    height:%dpx;display:flex;gap:14px;align-items:baseline}
 h2 b{font-weight:400}
 h2 span{letter-spacing:0;text-transform:none;font-size:11.5px;opacity:.55;flex:1}
 .r{display:flex;gap:30px;align-items:flex-start}
 img.t{width:%dpx;height:auto;background:#fff;box-shadow:0 1px 5px rgba(0,0,0,.16)}
 img.s{width:%dpx;height:%dpx;background:#fff;box-shadow:0 1px 5px rgba(0,0,0,.16)}
</style><header><h1>Half the shelf &#183; bottle and fruit art, six treatments</h1>
<p>Same data, same layout, same encoding &#8212; only the drawing changes. Left: the whole poster.
Right, at 1:1: the eight archetypes at 130px and at 37px, then a real slice of the ninety at 37px
and half chroma. The tail has to stay a picket fence.</p></header>%s"""
            % (SHEET_W, HEAD_H, ROW_H, H2_H, THUMB, SW, SH, ''.join(rows)))
    path = os.path.join(OUT, 'options.html')
    open(path, 'w', encoding='utf-8').write(html)

    height = HEAD_H + ROW_H * len(OPTIONS)
    subprocess.run([sys.executable, '-c',
                    'import subprocess,sys,os;'
                    'subprocess.run([os.environ.get("CHROME", r"C:\\Program Files\\Google\\Chrome'
                    '\\Application\\chrome.exe"), "--headless=new", "--disable-gpu",'
                    '"--hide-scrollbars", "--force-device-scale-factor=1",'
                    '"--user-data-dir=" + sys.argv[1], "--window-size=" + sys.argv[2],'
                    '"--screenshot=" + sys.argv[3], "file:///" + sys.argv[4]], check=True)',
                    os.path.join(ROOT, '.chrome-profile'), '%d,%d' % (SHEET_W, height),
                    os.path.join(OUT, 'options.png'), path.replace('\\', '/')], check=True)
    print('options.png', os.path.getsize(os.path.join(OUT, 'options.png')) // 1024, 'kB',
          '%dx%d' % (SHEET_W, height))


if __name__ == '__main__':
    build()
