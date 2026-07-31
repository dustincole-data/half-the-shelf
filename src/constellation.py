# B (round 2) — derived constellation. 143 drinks and all 177 ingredients in one field. The 90
# ingredients that serve a single drink become the fringe, and the fringe is the finding.
from layout import *
import numpy as np

INK = '#26221C'
PALE = '#C7BEB0'

drinks = {r['id']: r for r in ROWS}
ing_all = sorted(USE)
nodes = [('d', r['id']) for r in ROWS] + [('i', k) for k in ing_all]
idx = {n: i for i, n in enumerate(nodes)}
edges = [(idx[('d', r['id'])], idx[('i', i.strip().lower())]) for r in ROWS for i in r['ings']]
N = len(nodes)
print('nodes %d = %d drinks + %d ingredients | edges %d' % (N, len(ROWS), len(ing_all), len(edges)))

ei = np.array([e[0] for e in edges]); ej = np.array([e[1] for e in edges])
deg = np.bincount(np.concatenate([ei, ej]), minlength=N).astype(float)

# ---- pass 1: free layout, only to learn the angular order of the spirits ----
rs = np.random.RandomState(3)
P = rs.randn(N, 2) * 90
k = 34.0
for it in range(340):
    t = 1 - it / 340.0
    d = P[:, None, :] - P[None, :, :]
    dist = np.sqrt((d ** 2).sum(-1)) + 1e-6
    rep = (k * k / dist ** 2)[:, :, None] * d
    np.fill_diagonal(rep[:, :, 0], 0); np.fill_diagonal(rep[:, :, 1], 0)
    F = rep.sum(1)
    dv = P[ej] - P[ei]
    dl = np.sqrt((dv ** 2).sum(-1))[:, None] + 1e-6
    att = dv * (dl / k) * 1.1
    np.add.at(F, ei, att); np.add.at(F, ej, -att)
    F -= P * (0.012 + 0.06 / (1 + deg))[:, None]
    n = np.sqrt((F ** 2).sum(-1))[:, None] + 1e-9
    P += F / n * np.minimum(n, 15.0 * t + 1.2)
P -= np.median(P, axis=0)

SPIRITS = [s for s in HUE if s != 'Liqueur']
ang = {}
for sp in HUE:
    ids = [idx[('d', r['id'])] for r in ROWS if r['base'] == sp]
    c = P[ids].mean(0)
    ang[sp] = math.atan2(c[1], c[0])
ring = sorted(SPIRITS, key=lambda s: ang[s]) + ['Liqueur']
print('angular order the free layout produced:', ring)

WHEEL = ['#12968A', '#2F79D0', '#6E4DAE', '#A82348', '#DA3F87', '#D9541F', '#E8A020', '#8FBE2A']
H2 = {sp: WHEEL[i] for i, sp in enumerate(ring[:-1])}
H2['Liqueur'] = '#9E9A92'                       # grey is spent on the residual category

# ---- pass 2: territories on the ring, core ingredients drawn in, singletons pushed out ----
R0 = 235.0
anchor = {sp: np.array([R0 * math.cos(-math.pi / 2 + i * 2 * math.pi / len(ring)),
                        R0 * math.sin(-math.pi / 2 + i * 2 * math.pi / len(ring))])
          for i, sp in enumerate(ring)}
home = np.zeros((N, 2)); pull = np.zeros(N)
for r_ in ROWS:
    home[idx[('d', r_['id'])]] = anchor[r_['base']]
    pull[idx[('d', r_['id'])]] = 0.075
for nm in ing_all:
    i = idx[('i', nm)]
    ds = [d for d in ROWS if nm in [x.strip().lower() for x in d['ings']]]
    sps = set(d['base'] for d in ds)
    a = np.mean([anchor[s] for s in sps], axis=0)
    if USE[nm] == 1:
        home[i] = anchor[ds[0]['base']] * 2.32   # the fringe sits outside its own territory
        pull[i] = 0.115
    else:
        # the further an ingredient reaches, the harder the centre pulls it
        w = min(1.0, (USE[nm] - 1) / 8.0)
        home[i] = a * (1.0 - 0.62 * w)
        pull[i] = 0.045 + 0.05 * w

k = 25.0
for it in range(420):
    t = 1 - it / 420.0
    d = P[:, None, :] - P[None, :, :]
    dist = np.sqrt((d ** 2).sum(-1)) + 1e-6
    rep = (k * k / dist ** 2)[:, :, None] * d
    np.fill_diagonal(rep[:, :, 0], 0); np.fill_diagonal(rep[:, :, 1], 0)
    F = rep.sum(1)
    dv = P[ej] - P[ei]
    dl = np.sqrt((dv ** 2).sum(-1))[:, None] + 1e-6
    att = dv * (dl / k) * 0.5
    np.add.at(F, ei, att); np.add.at(F, ej, -att)
    F += (home - P) * pull[:, None] * 22.0
    n = np.sqrt((F ** 2).sum(-1))[:, None] + 1e-9
    P += F / n * np.minimum(n, 14.0 * t + 1.0)

CX, CY, RMAX = 500, 762, 418
rad = np.sqrt((P ** 2).sum(-1))
SC = RMAX / np.percentile(rad, 99.0)
P *= SC
P[:, 0] *= 1.14
P -= P.mean(0)                                   # let the field fill the page width
rad = np.sqrt(((P / np.array([1.14, 1.0])) ** 2).sum(-1))
over = rad > RMAX
P[over] = P[over] / rad[over][:, None] * RMAX
XY = P + np.array([CX, CY])
AXY = {sp: anchor[sp] * SC * np.array([1.14, 1.0]) + np.array([CX, CY]) for sp in ring}


def hull(pts):
    pts = sorted(set(map(tuple, pts)))
    if len(pts) < 3:
        return pts
    def half(ps):
        h = []
        for p in ps:
            while len(h) >= 2 and ((h[-1][0] - h[-2][0]) * (p[1] - h[-2][1])
                                   - (h[-1][1] - h[-2][1]) * (p[0] - h[-2][0])) <= 0:
                h.pop()
            h.append(p)
        return h[:-1]
    return half(pts) + half(pts[::-1])


def wedges(cx, cy, r, hues):
    if len(hues) == 1:
        return '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (cx, cy, r, hues[0])
    g, step = [], 2 * math.pi / len(hues)
    for i, h in enumerate(hues):
        a0, a1 = -math.pi / 2 + i * step, -math.pi / 2 + (i + 1) * step
        g.append('<path d="M%.1f %.1f L%.1f %.1f A%.1f %.1f 0 0 1 %.1f %.1f Z" fill="%s"/>'
                 % (cx, cy, cx + r * math.cos(a0), cy + r * math.sin(a0), r, r,
                    cx + r * math.cos(a1), cy + r * math.sin(a1), h))
    return ''.join(g)


defs = ('<defs><filter id="soft" x="-45%" y="-45%" width="190%" height="190%">'
        '<feGaussianBlur stdDeviation="24"/></filter></defs>')
out = []

# territories: the large washed pass
out.append('<g filter="url(#soft)">')
for sp in ring:
    pts = [tuple(XY[idx[('d', r['id'])]]) for r in ROWS if r['base'] == sp]
    hp = hull(pts)
    if len(hp) >= 3:
        out.append('<path d="%s" fill="%s" opacity="%.2f"/>'
                   % (spath(list(hp), close=True), H2[sp], 0.09 if sp == 'Liqueur' else 0.15))
out.append('</g>')

# edges
out.append('<g fill="none" stroke-linecap="round">')
for a, b in edges:
    nm = nodes[b][1]
    x1, y1 = XY[a]; x2, y2 = XY[b]
    mx = (x1 + x2) / 2 - (y2 - y1) * 0.14
    my = (y1 + y2) / 2 + (x2 - x1) * 0.14
    if USE[nm] == 1:
        out.append('<path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f" stroke="%s" stroke-width="0.85" '
                   'opacity="0.42"/>' % (x1, y1, mx, my, x2, y2, PALE))
    else:
        out.append('<path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f" stroke="%s" stroke-width="1.5" '
                   'opacity="0.15"/>' % (x1, y1, mx, my, x2, y2, H2[drinks[nodes[a][1]]['base']]))
out.append('</g>')

# the fringe: 90 dots that carry almost no ink
for nm in ing_all:
    if USE[nm] != 1:
        continue
    x, y = XY[idx[('i', nm)]]
    out.append('<circle cx="%.1f" cy="%.1f" r="3.0" fill="%s"/>' % (x, y, PALE))

# drinks
for r_ in ROWS:
    x, y = XY[idx[('d', r_['id'])]]
    out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" opacity="0.92"/>'
               % (x, y, 2.0 + 0.9 * r_['n'], H2[r_['base']]))

# shared ingredients, split into the spirits that use them
for nm in ing_all:
    u = USE[nm]
    if u < 2:
        continue
    x, y = XY[idx[('i', nm)]]
    r = 2.4 + 2.25 * math.sqrt(u)
    sps = sorted(set(d['base'] for d in ROWS if nm in [i.strip().lower() for i in d['ings']]),
                 key=lambda s: ring.index(s))
    out.append(wedges(x, y, r, [H2[s] for s in sps]))
    out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#FFFFFF" '
               'stroke-width="1.1"/>' % (x, y, r))

# the six workhorses get named where they sit, pushed clear of the crowd
placed = []
for nm, u in sorted(USE.items(), key=lambda kv: -kv[1])[:4]:
    x, y = XY[idx[('i', nm)]]
    r = 2.4 + 2.25 * math.sqrt(u)
    v = np.array([x - CX, y - CY]); n_ = np.hypot(*v) or 1
    lx, ly = x + v[0] / n_ * (r + 22), y + v[1] / n_ * (r + 22) + 4
    for px, py in placed:
        if abs(px - lx) < 74 and abs(py - ly) < 15:
            ly += 16
    placed.append((lx, ly))
    out.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-family="%s" font-size="12" '
               'fill="#FFFFFF" stroke="#FFFFFF" stroke-width="3.4" stroke-linejoin="round">%s</text>'
               % (lx, ly, SANS, nice(nm)))
    out.append(txt(lx, ly, nice(nm), 12, INK, 'middle', 0.95))

# hub badges, on the ring the layout itself chose
for sp in ring:
    c = AXY[sp]
    n = sum(1 for r in ROWS if r['base'] == sp)
    rr = 17 + 2.4 * math.sqrt(n) * 1.9
    out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#FFFFFF" opacity="0.90"/>' % (c[0], c[1], rr))
    out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="%s" stroke-width="2.6"/>'
               % (c[0], c[1], rr, H2[sp]))
    fs = min(19, max(10, rr * 0.40))
    out.append(txt(c[0], c[1] + fs * 0.10, sp.upper(), fs, INK, 'middle', track=0.6))
    out.append(txt(c[0], c[1] + fs * 1.25, str(n), fs * 0.82, INK, 'middle', 0.5))

# ---------------------------------------------------------------- masthead
out.append(txt(ML, MT + 52, HEADLINE_1, T_DISPLAY, INK))
out.append(txt(ML, MT + 112, HEADLINE_2, T_DISPLAY, INK))
for i, line in enumerate(['These 143 classic cocktails call for 177 different',
                          'ingredients. Ninety of them appear in exactly one drink',
                          'and nothing else &#8212; the pale fringe around the edge.']):
    out.append(txt(ML, MT + 166 + i * 25, line, T_DECK, INK, op=0.74))

# teach the mark
tx = PW - MR - 300
out.append(txt(tx, MT + 20, 'HOW TO READ IT', T_SECTION, INK, op=0.7, track=2.2))
out.append('<path d="M%.1f %.1f L%.1f %.1f" stroke="%s" stroke-width="0.8" opacity="0.22"/>'
           % (tx, MT + 29, PW - MR, MT + 29, INK))
demo = ROWS[[r['name'] for r in ROWS].index('Penicillin')] if any(r['name'] == 'Penicillin' for r in ROWS) \
    else ROWS[0]
dcx, dcy = tx + 82, MT + 122
out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>'
           % (dcx, dcy, 2.0 + 0.9 * demo['n'], H2[demo['base']]))
for i, ing in enumerate(demo['ings']):
    nm = ing.strip().lower()
    a = -math.pi / 2 + i * 2 * math.pi / demo['n']
    x, y = dcx + 52 * math.cos(a), dcy + 52 * math.sin(a)
    solo = USE[nm] == 1
    out.append('<path d="M%.1f %.1f L%.1f %.1f" stroke="%s" stroke-width="%.1f" opacity="%.2f"/>'
               % (dcx, dcy, x, y, PALE if solo else H2[demo['base']], 0.9 if solo else 1.5,
                  0.45 if solo else 0.35))
    if solo:
        out.append('<circle cx="%.1f" cy="%.1f" r="2.6" fill="%s"/>' % (x, y, PALE))
    else:
        out.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>'
                   % (x, y, 2.4 + 2.25 * math.sqrt(USE[nm]), H2[demo['base']]))
    ax = 'start' if math.cos(a) > -0.2 else 'end'
    out.append(txt(x + (9 if ax == 'start' else -9), y + 3.5, nice(nm), 10, INK, ax, 0.75))
nsolo = sum(1 for i in demo['ings'] if USE[i.strip().lower()] == 1)
WORD = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four'}
out.append(txt(tx, MT + 222, 'One drink, %s. %s of its %d ingredients are'
               % (demo['name'], WORD.get(nsolo, str(nsolo)), demo['n']), T_MICRO, INK, op=0.62))
out.append(txt(tx, MT + 236, 'used by nothing else in the set &#8212; drawn pale.',
               T_MICRO, INK, op=0.62))

# ---------------------------------------------------------------- the annotation
solos = [(nm, XY[idx[('i', nm)]]) for nm in ing_all if USE[nm] == 1]
tgt = min(solos, key=lambda kv: kv[1][0] + kv[1][1] * 1.15)[1]
out.append('<path d="M%.1f %.1f Q%.1f %.1f %.1f %.1f" fill="none" stroke="#B23A26" '
           'stroke-width="1.3" opacity="0.9"/>'
           % (ML + 8, 434, (ML + tgt[0]) / 2 - 20, 452, tgt[0] - 7, tgt[1] - 6))
out.append('<circle cx="%.1f" cy="%.1f" r="5.6" fill="none" stroke="#B23A26" stroke-width="1.6"/>'
           % (tgt[0], tgt[1]))
out.append(txt(ML, 408, 'THE FRINGE &#183; 90 INGREDIENTS, ONE DRINK EACH', T_SECTION, '#B23A26',
               op=0.95, track=1.8))
out.append(txt(ML, 426, 'They are 51% of the shelf and 16% of the pour.', T_MICRO, INK, op=0.6))

out.append(txt(ML, PH - 30, 'Position is found by what the drinks share; the colour wheel is then laid '
               'out to match the order the layout produced.', T_MICRO, INK, op=0.45))
out.append(txt(ML, PH - 16, 'TheCocktailDB &#183; the 143 alcoholic cocktails on the IBA official list '
               'or in its Cocktail category &#183; 579 ingredient slots, 177 distinct.',
               T_MICRO, INK, op=0.45))

write('constellation.svg', ''.join(out), w=PW, h=PH, bg='#FFFFFF', defs=defs)
