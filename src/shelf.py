# A (round 2) — illustrated organic. Every ingredient in the dataset drawn as the object it is,
# stood on shelves, sorted by how many drinks call for it. The finding is the silhouette.
#
# The object art itself is a swappable treatment (src/treatments.py); TREATMENT picks one, and
# SHELF_OUT names the file. Everything else — data, layout, encoding, type — is identical.
from layout import *
import treatments
from treatments import GROUND, INK, FAINT

T = treatments.get()
OUT_NAME = os.environ.get('SHELF_OUT') or 'shelf'

rng = random.Random(5)
items = sorted(USE.items(), key=lambda kv: (-kv[1], kv[0]))


def h_of(u):
    return 20 + 17.0 * math.sqrt(u)          # 37 at one drink, 130 at forty-two


def draw(name, uses, cx, by, chroma, seed, detail=True):
    return T.render(name, h_of(uses), cx, by, chroma, seed, fine=detail)


# ---------------------------------------------------------------- the stack
out = [paper(9, 3600, col='#4A4234', op=0.032, w=PW, h=PH, rmax=1.3)]

tier1 = [x for x in items if x[1] >= 12]
tier2 = [x for x in items if 5 <= x[1] < 12]
tier3 = [x for x in items if 2 <= x[1] < 5]
tier4 = [x for x in items if x[1] == 1]
print('tiers %d / %d / %d / %d = %d' % (len(tier1), len(tier2), len(tier3), len(tier4),
                                        len(tier1) + len(tier2) + len(tier3) + len(tier4)))


CHW = 0.60                                   # Century Gothic average advance, in ems


def fit(label, maxw, size):
    """Wrap a label to at most two lines inside maxw, shrinking the type only if wrapping fails."""
    def w(t, fs):
        return len(t) * CHW * fs
    if w(label, size) <= maxw:
        return [label], size
    words = label.split()
    for cut in range(len(words) - 1, 0, -1):
        a, b = ' '.join(words[:cut]), ' '.join(words[cut:])
        if max(w(a, size), w(b, size)) <= maxw:
            return [a, b], size
    if len(words) > 1:
        a, b = words[0], ' '.join(words[1:])
        fs = min(size, maxw / (max(len(a), len(b)) * CHW))
        return [a, b], max(7.6, fs)
    return [label], max(7.2, maxw / (len(label) * CHW))


def widths(row):
    return [T.width(kind_of(nm), h_of(u)) for nm, u in row]


def shelf(row, by, chroma, label):
    ws = widths(row)
    gap = (CW - sum(ws)) / max(1, len(row) - 1)
    used = sum(ws) + gap * (len(row) - 1)
    x = ML + (CW - used) / 2
    body, centres = [], []
    for (nm, u), w in zip(row, ws):
        cx = x + w / 2
        centres.append((cx, nm, u, w))
        sv, _ = draw(nm, u, cx, by, chroma, hash(nm) & 0xffff, detail=chroma >= 0.95)
        body.append(sv)
        x += w + gap
    body.insert(0, '<path d="%s" stroke="%s" stroke-width="%.1f" fill="none" opacity="%.2f" '
                   'stroke-linecap="round"/>'
                   % (rough_line(ML - 8, by + 3, PW - MR + 8, by + 4, 1.3, rng), INK,
                      3.0 if chroma > 0.7 else 1.8, 0.85 if chroma > 0.7 else 0.40))
    if label == 'flat':
        slot = (CW - gap * 0.5) / len(row) if len(row) > 1 else CW
        for cx, nm, u, w in centres:
            lines, fs = fit(nice(nm), slot - 6, T_MICRO)
            for li, ln in enumerate(lines):
                body.append(txt(cx, by + 23 + li * (fs + 2.4), ln, fs, INK, 'middle', 0.85))
            body.append(txt(cx, by + 53, str(u), T_LABEL, INK, 'middle', 0.48))
    elif label == 'turned':
        for cx, nm, u, w in centres:
            t = '%s &#183; %d' % (nice(nm), u)
            fs = min(9.8, 122.0 / (len(nice(nm)) + 4) / CHW)
            body.append('<text x="%.1f" y="%.1f" text-anchor="end" font-family="%s" font-size="%.1f" '
                        'fill="%s" opacity="0.82" transform="rotate(-90 %.1f %.1f)">%s</text>'
                        % (cx + 3.4, by + 19, SANS, fs, INK, cx + 3.4, by + 19, t))
    return ''.join(body)


def section(y, lab, n, note=''):
    o = [txt(ML, y, '%s' % lab, T_SECTION, INK, op=0.62, track=2.2),
         txt(PW - MR, y, '%d ingredients' % n, T_SECTION, INK, 'end', 0.45, track=1.4)]
    o.append('<path d="M%d %.1f L%d %.1f" stroke="%s" stroke-width="0.8" opacity="0.22"/>'
             % (ML, y + 9, PW - MR, y + 9, INK))
    if note:
        o.append(txt(ML, y + 26, note, T_MICRO, INK, op=0.55))
    return ''.join(o)


out.append(section(352, 'IN TWELVE DRINKS OR MORE', len(tier1)))
out.append(shelf(tier1, 504, 1.00, 'flat'))

out.append(section(586, 'IN FIVE TO ELEVEN', len(tier2)))
out.append(shelf(tier2, 690, 1.00, 'turned'))

out.append(section(828, 'IN TWO TO FOUR', len(tier3)))
out.append(shelf(tier3[:27], 900, 0.74, None))
out.append(shelf(tier3[27:], 956, 0.74, None))

out.append(section(992, 'IN ONE DRINK, AND NOTHING ELSE', len(tier4)))
out.append(shelf(tier4[:45], 1048, 0.50, None))
out.append(shelf(tier4[45:], 1092, 0.50, None))

# ---------------------------------------------------------------- masthead
out.append(txt(ML, MT + 52, HEADLINE_1, T_DISPLAY, INK))
out.append(txt(ML, MT + 112, HEADLINE_2, T_DISPLAY, INK))
DL = ['These 143 classic cocktails call for 177 different',
      'ingredients. Ninety of them appear in exactly one drink',
      'and nothing else &#8212; 51% of the bottles, 16% of the pour.']
for i, line in enumerate(DL):
    out.append(txt(ML, MT + 166 + i * 25, line, T_DECK, INK, op=0.74))

# teach the mark
tx = PW - MR - 300
out.append(txt(tx, MT + 20, 'HOW TO READ IT', T_SECTION, INK, op=0.7, track=2.2))
out.append('<path d="M%.1f %.1f L%.1f %.1f" stroke="%s" stroke-width="0.8" opacity="0.22"/>'
           % (tx, MT + 29, PW - MR, MT + 29, INK))
DEMO_Y = MT + 178
out.append('<path d="%s" stroke="%s" stroke-width="2.2" fill="none" opacity="0.55" '
           'stroke-linecap="round"/>'
           % (rough_line(tx + 8, DEMO_Y + 3, PW - MR, DEMO_Y + 4, 1.1, rng), INK))
for nm, dx in [('gin', tx + 46), ('angostura bitters', tx + 150), ('aperol', tx + 240)]:
    u = USE[nm]
    sv, w = draw(nm, u, dx, DEMO_Y, 1.0, hash(nm) & 0xffff)
    out.append(sv)
    out.append(txt(dx, DEMO_Y + 24, nice(nm).split()[0], T_MICRO, INK, 'middle', 0.8))
    out.append(txt(dx, DEMO_Y + 38, '%d drink%s' % (u, '' if u == 1 else 's'), T_MICRO, INK, 'middle', 0.5))
out.append(txt(tx, DEMO_Y + 58, 'One object per ingredient, drawn as the thing it is. Its',
               T_MICRO, INK, op=0.6))
out.append(txt(tx, DEMO_Y + 72, 'height is how many of the 143 drinks call for it.',
               T_MICRO, INK, op=0.6))

# ---------------------------------------------------------------- the annotation that names it
q = random.Random(77)
out.append('<path d="%s" stroke="#B23A26" stroke-width="2.6" fill="none" opacity="0.9" '
           'stroke-linecap="round"/>'
           % spath(wob([(ML - 22, 1008), (ML - 32, 1014), (ML - 32, 1046), (ML - 40, 1052),
                        (ML - 32, 1058), (ML - 32, 1090), (ML - 22, 1096)], 0.9, q)))
out.append(txt(ML, 1146, 'Fifty-nine of the 143 drinks &#8212; two in five &#8212; need at least one '
               'ingredient', T_DECK, '#B23A26', op=0.95))
out.append(txt(ML, 1170, 'that appears nowhere else on this page.', T_DECK, '#B23A26', op=0.95))
out.append(txt(ML, 1198, 'The thirty best-chosen bottles you could buy would still complete only 22 '
               'of the 143.', T_DECK, INK, op=0.6))

out.append(txt(ML, PH - 16, 'TheCocktailDB &#183; the 143 alcoholic cocktails on the IBA official list '
               'or in its Cocktail category &#183; 579 ingredient slots, 177 distinct.',
               T_MICRO, INK, op=0.45))

write(OUT_NAME + '.svg', ''.join(out), w=PW, h=PH, bg=GROUND)
