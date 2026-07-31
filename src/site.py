"""The poster with the lights on.

    python src/site.py           -> out/site/index.html   (one file, no build step, no deps)

Same data, same geometry, same cut-paper art as out/shelf.svg. What it adds is the one thing the
mode structurally cannot carry on paper: the relationship between an ingredient and the drinks that
use it. Point at a bottle and the shelf admits what it is hiding.

Then the second act. `Buy the shelf` empties the page and lets you fill it a bottle at a time; the
counter is the finding, self-administered. Thirty bottles still will not get you thirty drinks.
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout import *
import treatments
from treatments import GROUND, INK
from page import PAGE
from shelfgrid import h_of, place, seed_of, ITEMS, TIERS, STACK, SPLIT

T = treatments.get('cutpaper')
ICON = 'data:image/svg+xml,' + '%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2032%2032%22%3E%3Cpath%20d%3D%22M11%2030%20L11%2014%20L13.5%2010.5%20L13.5%203%20L18.5%203%20L18.5%2010.5%20L21%2014%20L21%2030%20Z%22%20fill%3D%22%231F9E8E%22%2F%3E%3Cpath%20d%3D%22M16%2030%20L16%203%20L18.5%203%20L18.5%2010.5%20L21%2014%20L21%2030%20Z%22%20fill%3D%22%2317786B%22%2F%3E%3Cpath%20d%3D%22M13%205.4%20L19%205.4%20L19%203%20L13%203%20Z%22%20fill%3D%22%230F5A50%22%2F%3E%3C%2Fsvg%3E'        # the cut-paper bottle, as the tab icon
SITE = os.path.join(OUT, 'site')
rng = random.Random(5)

IDX = dict((nm, i) for i, (nm, u) in enumerate(ITEMS))
DRINKS = sorted(ROWS, key=lambda r: r['name'])
USES = collections.defaultdict(list)                 # ingredient index -> drink indices
for di, r in enumerate(DRINKS):
    for nm in set(x.strip().lower() for x in r['ings']):   # once per drink, never once per slot
        USES[IDX[nm]].append(di)


# ---------------------------------------------------------------- the drawing
def speckle():
    """The poster's paper, as a tile instead of 3600 loose circles — same grain, a tenth the bytes."""
    q = random.Random(9)
    dots = ''.join('<circle cx="%.0f" cy="%.0f" r="%.2f"/>'
                   % (q.uniform(0, 160), q.uniform(0, 160), q.uniform(0.3, 1.3)) for _ in range(92))
    return ('<defs><pattern id="pp" width="160" height="160" patternUnits="userSpaceOnUse">'
            '<g fill="#4A4234" opacity="0.032">%s</g></pattern></defs>'
            '<rect width="%d" height="%d" fill="url(#pp)"/>' % (dots, PW, PH))


def objects():
    """Every ingredient, drawn where the poster puts it and wrapped so it can be pointed at."""
    out, geo = [], {}
    for ti, (hy, baselines, chroma, label, head) in enumerate(STACK):
        row = TIERS[ti]
        cut = SPLIT.get(ti)
        parts = [row[:cut], row[cut:]] if cut else [row]
        for bi, by in enumerate(baselines):
            part = parts[bi]
            centres, gap = place(part, T)
            out.append('<path d="%s" stroke="%s" stroke-width="%.1f" fill="none" opacity="%.2f" '
                       'stroke-linecap="round"/>'
                       % (rough_line(ML - 8, by + 3, PW - MR + 8, by + 4, 1.3, rng), INK,
                          3.0 if chroma > 0.7 else 1.8, 0.85 if chroma > 0.7 else 0.40))
            for cx, nm, u, w in centres:
                sv, _ = T.render(nm, h_of(u), cx, by, chroma, seed_of(nm), fine=chroma >= 0.95)
                h = h_of(u)
                pad = min(gap / 2, 7)
                # x/y/h/w are the object's real drawn box. getBBox() would also see the shadow
                # and closure papers, which are cut oversize and clipped away, and would drag the
                # card off the mark by more than fifty pixels on the tallest bottles.
                out.append('<g class="o" data-i="%d" data-x="%.1f" data-y="%.1f" data-h="%.1f" '
                           'data-w="%.1f">%s'
                           '<rect class="hit" x="%.1f" y="%.1f" width="%.1f" height="%.1f"/></g>'
                           % (IDX[nm], cx, by, h, w, sv,
                              cx - w / 2 - pad, by - h - 4, w + pad * 2, h + 10))
                geo[IDX[nm]] = (round(cx, 1), round(by, 1), round(h, 1))
            if label == 'flat':
                slot = (CW - gap * 0.5) / len(part)
                for cx, nm, u, w in centres:
                    lines, fs = fit(nice(nm), slot - 6, T_MICRO)
                    for li, ln in enumerate(lines):
                        out.append(txt(cx, by + 23 + li * (fs + 2.4), ln, fs, INK, 'middle', 0.85))
                    out.append(txt(cx, by + 53, str(u), T_LABEL, INK, 'middle', 0.48))
            elif label == 'turned':
                for cx, nm, u, w in centres:
                    t = '%s &#183; %d' % (nice(nm), u)
                    fs = min(9.8, 122.0 / (len(nice(nm)) + 4) / CHW)
                    out.append('<text x="%.1f" y="%.1f" text-anchor="end" font-family="%s" '
                               'font-size="%.1f" fill="%s" opacity="0.82" '
                               'transform="rotate(-90 %.1f %.1f)">%s</text>'
                               % (cx + 3.4, by + 19, SANS, fs, INK, cx + 3.4, by + 19, t))
        out.append(txt(ML, hy, head, T_SECTION, INK, op=0.62, track=2.2))
        out.append(txt(PW - MR, hy, '%d ingredients' % len(row), T_SECTION, INK, 'end', 0.45,
                       track=1.4))
        out.append('<path d="M%d %.1f L%d %.1f" stroke="%s" stroke-width="0.8" opacity="0.22"/>'
                   % (ML, hy + 9, PW - MR, hy + 9, INK))
    return ''.join(out), geo


CHW = 0.60


def fit(label, maxw, size):
    def w(t, fs):
        return len(t) * CHW * fs
    if w(label, size) <= maxw:
        return [label], size
    words = label.split()
    for c in range(len(words) - 1, 0, -1):
        a, b = ' '.join(words[:c]), ' '.join(words[c:])
        if max(w(a, size), w(b, size)) <= maxw:
            return [a, b], size
    if len(words) > 1:
        a, b = words[0], ' '.join(words[1:])
        return [a, b], max(7.6, min(size, maxw / (max(len(a), len(b)) * CHW)))
    return [label], max(7.2, maxw / (len(label) * CHW))


def masthead():
    o = [txt(ML, MT + 52, HEADLINE_1, T_DISPLAY, INK), txt(ML, MT + 112, HEADLINE_2, T_DISPLAY, INK)]
    o.append('<g class="deck">')
    for i, line in enumerate(DECK_LINES):
        o.append(txt(ML, MT + 166 + i * 25, line, T_DECK, INK, op=0.74))
    o.append('</g>')
    tx = PW - MR - 300
    o.append('<g class="teach">')
    o.append(txt(tx, MT + 20, 'HOW TO READ IT', T_SECTION, INK, op=0.7, track=2.2))
    o.append('<path d="M%.1f %.1f L%.1f %.1f" stroke="%s" stroke-width="0.8" opacity="0.22"/>'
             % (tx, MT + 29, PW - MR, MT + 29, INK))
    dy = MT + 178
    o.append('<path d="%s" stroke="%s" stroke-width="2.2" fill="none" opacity="0.55" '
             'stroke-linecap="round"/>'
             % (rough_line(tx + 8, dy + 3, PW - MR, dy + 4, 1.1, rng), INK))
    for nm, dx in [('gin', tx + 46), ('angostura bitters', tx + 150), ('aperol', tx + 240)]:
        u = USE[nm]
        sv, w = T.render(nm, h_of(u), dx, dy, 1.0, seed_of(nm))
        o.append(sv)
        o.append(txt(dx, dy + 24, nice(nm).split()[0], T_MICRO, INK, 'middle', 0.8))
        o.append(txt(dx, dy + 38, '%d drink%s' % (u, '' if u == 1 else 's'), T_MICRO, INK,
                     'middle', 0.5))
    o.append(txt(tx, dy + 58, 'One object per ingredient, drawn as the thing it is. Its',
                 T_MICRO, INK, op=0.6))
    o.append(txt(tx, dy + 72, 'height is how many of the 143 drinks call for it.',
                 T_MICRO, INK, op=0.6))
    o.append('</g>')
    return ''.join(o)


def footer():
    q = random.Random(77)
    o = ['<path d="%s" stroke="#B23A26" stroke-width="2.6" fill="none" opacity="0.9" '
         'stroke-linecap="round"/>'
         % spath(wob([(ML - 22, 1008), (ML - 32, 1014), (ML - 32, 1046), (ML - 40, 1052),
                      (ML - 32, 1058), (ML - 32, 1090), (ML - 22, 1096)], 0.9, q))]
    o.append(txt(ML, 1146, NOTE_1, T_DECK, '#B23A26', op=0.95))
    o.append(txt(ML, 1170, NOTE_2, T_DECK, '#B23A26', op=0.95))
    o.append(txt(ML, 1198, SHELF_LINE, T_DECK, INK, op=0.6))
    o.append(txt(ML, PH - 16, SOURCE_LINE,
                 T_MICRO, INK, op=0.45))
    return ''.join(o)




def index_section():
    """The ninety-two, listed by the drink that makes you buy them.

    On the poster they are ninety-two nearly identical marks with no room for a name. Here each one
    gets its name back, filed under the single drink it exists for, worst offenders first."""
    worst = []
    for di, r in enumerate(DRINKS):
        ings = sorted(set(IDX[i.strip().lower()] for i in r['ings']))
        solo = [i for i in ings if len(USES[i]) == 1]
        if solo:
            worst.append((len(solo), r['name'], r['base'], solo))
    worst.sort(key=lambda x: (-x[0], x[1]))
    # the index and the poster are two renderings of one set; if they ever disagree, stop
    listed = sorted(i for _, _, _, solo in worst for i in solo)
    assert len(listed) == len(set(listed)) == len(SINGLE), (len(listed), len(SINGLE))
    assert len(worst) == N_WITH_SINGLE, (len(worst), N_WITH_SINGLE)
    cards = []
    for n, name, base, solo in worst:
        cards.append('<article><h4><i style="background:%s"></i>%s <s>%s</s></h4><ul>%s</ul></article>'
                     % (HUE.get(base, '#B9A489'), esc(name), esc(base),
                        ''.join('<li data-i="%d">%s</li>' % (i, esc(nice(ITEMS[i][0])))
                                for i in solo)))
    lede = ('%s of the 177 bottles pour exactly one drink and nothing else. They are not exotic by '
            'accident — they are the price of these <b>%d drinks</b>, each of which needs at '
            'least one bottle no other drink on the page will ever ask for again. %s of them ask '
            'for more than one. Click any bottle to find it back on the shelf.'
            % (cap1(word(len(SINGLE))), len(worst),
               cap1(word(sum(1 for w in worst if w[0] > 1)))))
    return ('<section id="ninety"><h2>The %s</h2><p class="lede">%s</p><div id="grid">%s</div>'
            '</section>' % (word(len(SINGLE)), lede, ''.join(cards)))


# ---------------------------------------------------------------- the page
def build():
    body, geo = objects()
    svg = ('<svg id="sheet" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d">'
           '<rect width="%d" height="%d" fill="%s"/>%s%s%s%s</svg>'
           % (PW, PH, PW, PH, GROUND, speckle(), body, masthead(), footer()))
    ing = [[nm, u] for nm, u in ITEMS]
    dr = [[esc(r['name']), r['base'],
           sorted(set(IDX[i.strip().lower()] for i in r['ings']))] for r in DRINKS]
    html = (PAGE.replace('__SVG__', svg)
                .replace('__ING__', json.dumps(ing, separators=(',', ':')))
                .replace('__DR__', json.dumps(dr, separators=(',', ':')))
                .replace('__SHELF_LINE__', SHELF_LINE)
                .replace('__HUE__', json.dumps(HUE, separators=(',', ':')))
                .replace('__INDEX__', index_section())
                .replace('__ICON__', ICON))
    os.makedirs(SITE, exist_ok=True)
    path = os.path.join(SITE, 'index.html')
    open(path, 'w', encoding='utf-8').write(html)
    print('wrote %s  %d kB  ·  %d ingredients, %d drinks'
          % (path, len(html) // 1024, len(ing), len(dr)))
    return path


if __name__ == '__main__':
    build()
