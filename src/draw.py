import json, math, os, random, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data')
OUT = os.path.join(ROOT, 'out')

D = json.load(open(os.path.join(DATA, 'cocktails.json'), encoding='utf-8'))
ROWS = D['rows']
ING_DRINKS = D['ing_drinks']
S = D['stats']

W = H = 1000

# --- palette: derived from the eight base spirits this dataset actually has, laid out as a wheel ---
SPIRIT_ORDER = ['Gin', 'Tequila', 'Rum', 'Whisky', 'Brandy', 'Liqueur', 'Wine', 'Vodka']
HUE = {
    'Gin':     '#149C8C',
    'Tequila': '#8FBE2A',
    'Rum':     '#E8A020',
    'Whisky':  '#D9541F',
    'Brandy':  '#B32747',
    'Liqueur': '#DE4C97',
    'Wine':    '#6E4DAE',
    'Vodka':   '#2F79D0',
}
IBA_HUE = {
    'Unforgettables':        '#E0A21A',
    'Contemporary Classics': '#DC3C3C',
    'New Era Drinks':        '#0F9C9C',
}
NEUTRAL = '#C9C5BD'

CITRUS = ('lemon juice', 'lime juice', 'grapefruit juice', 'orange juice', 'lime', 'lemon')


def has_citrus(r):
    low = [i.strip().lower() for i in r['ings']]
    return any(c in low for c in CITRUS)


def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


# ---------- hand-drawn geometry: everything is wobbled, nothing is a perfect primitive ----------
def wob(pts, amp=1.6, rng=None):
    rng = rng or random
    return [(x + rng.uniform(-amp, amp), y + rng.uniform(-amp, amp)) for x, y in pts]


def spath(pts, close=False, smooth=True):
    """Catmull-rom-ish smooth path through points."""
    if not smooth or len(pts) < 3:
        d = 'M%.1f %.1f' % pts[0] + ''.join(' L%.1f %.1f' % p for p in pts[1:])
        return d + (' Z' if close else '')
    p = list(pts)
    if close:
        p = [pts[-1]] + list(pts) + [pts[0], pts[1]]
    else:
        p = [pts[0]] + list(pts) + [pts[-1]]
    d = 'M%.1f %.1f' % p[1]
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6.0, p1[1] + (p2[1] - p0[1]) / 6.0)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6.0, p2[1] - (p3[1] - p1[1]) / 6.0)
        d += ' C%.1f %.1f %.1f %.1f %.1f %.1f' % (c1[0], c1[1], c2[0], c2[1], p2[0], p2[1])
    return d + (' Z' if close else '')


def rough_circle(cx, cy, r, amp=None, n=None, rng=None):
    rng = rng or random
    amp = amp if amp is not None else max(0.6, r * 0.06)
    n = n or max(9, int(r / 2.2) + 8)
    pts = []
    off = rng.uniform(0, 6.28)
    for i in range(n):
        a = off + i * 2 * math.pi / n
        rr = r + rng.uniform(-amp, amp)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return spath(pts, close=True)


def rbox(x0, y0, x1, y1, amp=1.8, rng=None):
    """A drawn box: corners subdivided so the smoothing keeps the edges straight."""
    rng = rng or random
    corners = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    pts = []
    for i in range(4):
        ax, ay = corners[i]; bx, by = corners[(i + 1) % 4]
        for k in range(6):
            t = k / 6.0
            pts.append((ax + (bx - ax) * t, ay + (by - ay) * t))
    return spath(wob(pts, amp, rng), close=True)


def rough_line(x1, y1, x2, y2, amp=1.4, rng=None):
    rng = rng or random
    n = max(3, int(math.hypot(x2 - x1, y2 - y1) / 26) + 2)
    pts = [(x1 + (x2 - x1) * i / n, y1 + (y2 - y1) * i / n) for i in range(n + 1)]
    return spath(wob(pts, amp, rng))


# ---------- packing ----------
def pack_in_circle(radii, R, rng=None, iters=260):
    """Place circles of the given radii inside a circle of radius R, greedy + relaxation.
    Returns list of (x, y) relative to centre, in the input order."""
    rng = rng or random
    n = len(radii)
    pos = []
    for i, r in enumerate(radii):
        a = i * 2.399963
        rad = R * math.sqrt((i + 0.5) / n) * 0.86
        pos.append([rad * math.cos(a), rad * math.sin(a)])
    for _ in range(iters):
        for i in range(n):
            for j in range(i + 1, n):
                dx = pos[j][0] - pos[i][0]
                dy = pos[j][1] - pos[i][1]
                d = math.hypot(dx, dy) or 0.001
                need = radii[i] + radii[j] + 0.9
                if d < need:
                    push = (need - d) / 2
                    ux, uy = dx / d, dy / d
                    pos[i][0] -= ux * push; pos[i][1] -= uy * push
                    pos[j][0] += ux * push; pos[j][1] += uy * push
        for i in range(n):
            d = math.hypot(*pos[i]) or 0.001
            pos[i][0] -= pos[i][0] / d * 0.55
            pos[i][1] -= pos[i][1] / d * 0.55
            lim = R - radii[i]
            if d > lim:
                pos[i][0] *= lim / d; pos[i][1] *= lim / d
    return [(p[0], p[1]) for p in pos]


def pack_in_rect(radii, w, h, rng=None, iters=200):
    rng = rng or random
    n = len(radii)
    pos = [[rng.uniform(-w / 2, w / 2), rng.uniform(-h / 2, h / 2)] for _ in range(n)]
    for _ in range(iters):
        for i in range(n):
            for j in range(i + 1, n):
                dx = pos[j][0] - pos[i][0]; dy = pos[j][1] - pos[i][1]
                d = math.hypot(dx, dy) or 0.001
                need = radii[i] + radii[j] + 0.7
                if d < need:
                    push = (need - d) / 2; ux, uy = dx / d, dy / d
                    pos[i][0] -= ux * push; pos[i][1] -= uy * push
                    pos[j][0] += ux * push; pos[j][1] += uy * push
        for i in range(n):
            pos[i][0] *= 0.995; pos[i][1] *= 0.995
            pos[i][0] = max(-w / 2 + radii[i], min(w / 2 - radii[i], pos[i][0]))
            pos[i][1] = max(-h / 2 + radii[i], min(h / 2 - radii[i], pos[i][1]))
    return [(p[0], p[1]) for p in pos]


def svg_open(w=W, h=H, bg='#ffffff', extra=''):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">'
            '<rect width="%d" height="%d" fill="%s"/>%s' % (w, h, w, h, w, h, bg, extra))


def write(name, body, w=W, h=H, bg='#ffffff', defs=''):
    out = svg_open(w, h, bg, defs) + body + '</svg>'
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write(out)
    print('wrote', name, len(out) // 1024, 'kB')


def paper(seed=1, n=2600, w=W, h=H, col='#000', op=0.045, rmax=1.2):
    rng = random.Random(seed)
    g = ['<g fill="%s" opacity="%.3f">' % (col, op)]
    for _ in range(n):
        g.append('<circle cx="%.0f" cy="%.0f" r="%.2f"/>' % (
            rng.uniform(0, w), rng.uniform(0, h), rng.uniform(0.3, rmax)))
    g.append('</g>')
    return ''.join(g)


def mix(a, b, t):
    """t of the way from a to b."""
    a, b = a.lstrip('#'), b.lstrip('#')
    return '#%02X%02X%02X' % tuple(
        int(int(a[i:i + 2], 16) * (1 - t) + int(b[i:i + 2], 16) * t) for i in (0, 2, 4))


def shade(hexc, f):
    """f>1 lightens toward white, f<1 darkens."""
    h = hexc.lstrip('#')
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    if f >= 1:
        t = min(1.0, f - 1.0)
        r, g, b = (int(c + (255 - c) * t) for c in (r, g, b))
    else:
        r, g, b = (int(c * f) for c in (r, g, b))
    return '#%02X%02X%02X' % (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
