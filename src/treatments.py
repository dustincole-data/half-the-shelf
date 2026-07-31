# Drawn treatments of the eight archetypes. Same data, same layout, same encoding — only the
# drawing changes. Each treatment owns its silhouette hand, its line, its interior and its shadow.
#
# Hard constraint every treatment is judged against: the object must read at 130px (the top shelf)
# AND at 37px (the tail of ninety). Below ~35px interior detail is gone, so the differentiation has
# to live in the silhouette and in whatever signature the treatment puts across the whole fence.
from layout import *

GROUND = '#FFFFFF'
INK = '#2E2A24'
FAINT = '#A8A296'
CORK = '#C08A4E'

# ---------------------------------------------------------------- shared silhouettes
# (aspect = width/height, right-half profile bottom -> top as (x/half-width, y/height)).
# Re-cut from the shipped set: the four bottle kinds now differ by footprint, shoulder and cap,
# which are the only three things still legible at 37px.
PROFILES = {
    'tall':  (0.32, [(1.00, 0.00), (1.00, 0.46), (0.96, 0.56), (0.60, 0.67), (0.40, 0.73),
                     (0.40, 0.895), (0.52, 0.915), (0.52, 1.00)]),
    'short': (0.50, [(1.00, 0.00), (1.00, 0.50), (0.94, 0.62), (0.55, 0.72), (0.44, 0.78),
                     (0.44, 0.895), (0.56, 0.92), (0.56, 1.00)]),
    'dash':  (0.26, [(1.00, 0.00), (1.00, 0.54), (0.88, 0.64), (0.42, 0.73), (0.42, 0.90),
                     (0.78, 0.945), (0.70, 1.00)]),
    'jar':   (0.66, [(1.00, 0.00), (1.00, 0.62), (0.96, 0.72), (0.78, 0.80), (0.78, 0.86),
                     (0.88, 0.875), (0.88, 1.00)]),
    'can':   (0.46, [(0.92, 0.00), (1.00, 0.07), (1.00, 0.90), (0.90, 0.945), (0.90, 1.00)]),
}
BOTTLES = tuple(PROFILES)
KINDS = ('tall', 'short', 'dash', 'jar', 'can', 'citrus', 'cherry', 'sprig')
R_CITRUS, R_CHERRY = 0.44, 0.34


def width_of(kind, h):
    if kind in PROFILES:
        return h * PROFILES[kind][0]
    if kind == 'citrus':
        return h * R_CITRUS * 2
    if kind == 'cherry':
        return h * R_CHERRY * 2
    return h * 0.40                                   # sprig


def body(cx, by, h, kind, q, amp=None, smooth=True, sx=1.0, sy=1.0, dy=0.0):
    """The silhouette, mirrored off one half-profile. sx/sy/dy inset a second copy of the same
    shape for washes and label grounds — an inset copy can never be a different shape."""
    asp, prof = PROFILES[kind]
    w = h * asp
    amp = amp if amp is not None else max(0.35, w * 0.020)
    pts = [(cx + u * w / 2 * sx, by - v * h * sy - dy) for u, v in prof]
    pts += [(cx - u * w / 2 * sx, by - v * h * sy - dy) for u, v in reversed(prof)]
    return spath(wob(pts, amp, q), close=True, smooth=smooth), w


def leaf(cx, by, h, q, amp=None):
    w = h * 0.40
    p = [(cx, by), (cx - w * 0.10, by - h * 0.40), (cx - w * 0.34, by - h * 0.72),
         (cx - w * 0.30, by - h * 0.94), (cx + w * 0.04, by - h),
         (cx + w * 0.34, by - h * 0.76), (cx + w * 0.22, by - h * 0.44)]
    return spath(wob(p, amp if amp is not None else max(0.35, w * 0.03), q), close=True), w


def stem(cx, by, h, q):
    r = h * R_CHERRY
    return rough_line(cx + r * 0.10, by - r * 1.9, cx + r * 0.75, by - h * 0.99, 0.5, q)


def clipped(cid, d, inner):
    return ('<clipPath id="%s"><path d="%s"/></clipPath><g clip-path="url(#%s)">%s</g>'
            % (cid, d, cid, ''.join(inner)))


def drop(d, h, op=0.13, ox=None, oy=None):
    return ('<path d="%s" fill="%s" opacity="%.2f" transform="translate(%.1f,%.1f)"/>'
            % (d, INK, op,
               max(1.1, h * 0.028) if ox is None else ox,
               max(0.9, h * 0.020) if oy is None else oy))


# ---------------------------------------------------------------- treatment base
class Treatment(object):
    key = title = note = ''
    smooth = True
    amp = None

    @classmethod
    def width(cls, kind, h):
        return width_of(kind, h)

    @classmethod
    def render(cls, name, h, cx, by, chroma, seed, fine=True):
        """Returns (svg, width). `fine` is the small stuff that only pays above ~46px; a
        treatment's own signature is drawn at every size, because that is what has to hold the
        fence together at 37px."""
        q = random.Random(seed)
        kind = kind_of(name)
        raw = col_of(name)
        col = mix(raw, GROUND, 1 - chroma)
        cid = 'c%d' % (seed * 7 + int(cx) * 13 + int(by))
        return cls.paint(kind, raw, col, chroma, cx, by, h, q, cid, fine)


# ---------------------------------------------------------------- 0 · current (the control)
class Current(Treatment):
    key, title = 'current', 'Previous — the drawing this replaced'
    note = ('Eight archetypes, one white label patch, a highlight bar and an ink keyline. '
            'The control the five were judged against.')

    @classmethod
    def width(cls, kind, h):
        if kind == 'citrus':
            return h * 0.42 * 2
        if kind == 'cherry':
            return h * 0.36 * 2
        return h * {'tall': 0.34, 'short': 0.46, 'dash': 0.30, 'jar': 0.62,
                    'can': 0.44, 'sprig': 0.40}[kind]

    @classmethod
    def paint(cls, kind, raw, col, chroma, cx, by, h, q, cid, fine):
        w = cls.width(kind, h)
        if kind == 'tall':
            nk = w * 0.17
            p = [(cx - w / 2, by), (cx - w / 2, by - h * 0.50), (cx - w * 0.40, by - h * 0.60),
                 (cx - nk, by - h * 0.70), (cx - nk, by - h * 0.955), (cx - nk * 1.25, by - h * 0.975),
                 (cx - nk * 1.25, by - h), (cx + nk * 1.25, by - h), (cx + nk * 1.25, by - h * 0.975),
                 (cx + nk, by - h * 0.955), (cx + nk, by - h * 0.70), (cx + w * 0.40, by - h * 0.60),
                 (cx + w / 2, by - h * 0.50), (cx + w / 2, by)]
        elif kind == 'short':
            nk = w * 0.22
            p = [(cx - w / 2, by), (cx - w / 2, by - h * 0.58), (cx - w * 0.36, by - h * 0.70),
                 (cx - nk, by - h * 0.78), (cx - nk, by - h * 0.95), (cx - nk * 1.3, by - h * 0.97),
                 (cx - nk * 1.3, by - h), (cx + nk * 1.3, by - h), (cx + nk * 1.3, by - h * 0.97),
                 (cx + nk, by - h * 0.95), (cx + nk, by - h * 0.78), (cx + w * 0.36, by - h * 0.70),
                 (cx + w / 2, by - h * 0.58), (cx + w / 2, by)]
        elif kind == 'dash':
            nk = w * 0.26
            p = [(cx - w / 2, by), (cx - w / 2, by - h * 0.62), (cx - nk, by - h * 0.76),
                 (cx - nk, by - h * 0.92), (cx - nk * 1.5, by - h * 0.94), (cx - nk * 1.5, by - h),
                 (cx + nk * 1.5, by - h), (cx + nk * 1.5, by - h * 0.94), (cx + nk, by - h * 0.92),
                 (cx + nk, by - h * 0.76), (cx + w / 2, by - h * 0.62), (cx + w / 2, by)]
        elif kind == 'jar':
            p = [(cx - w / 2, by), (cx - w / 2, by - h * 0.74), (cx - w * 0.40, by - h * 0.84),
                 (cx - w * 0.40, by - h * 0.94), (cx - w * 0.46, by - h), (cx + w * 0.46, by - h),
                 (cx + w * 0.40, by - h * 0.94), (cx + w * 0.40, by - h * 0.84),
                 (cx + w / 2, by - h * 0.74), (cx + w / 2, by)]
        elif kind == 'can':
            p = [(cx - w / 2, by - h * 0.06), (cx - w * 0.46, by), (cx + w * 0.46, by),
                 (cx + w / 2, by - h * 0.06), (cx + w / 2, by - h * 0.94), (cx + w * 0.44, by - h),
                 (cx - w * 0.44, by - h), (cx - w / 2, by - h * 0.94)]
        elif kind == 'sprig':
            sw = h * 0.40
            p = [(cx, by), (cx - sw * 0.14, by - h * 0.42), (cx, by - h * 0.72),
                 (cx + sw * 0.30, by - h * 0.92), (cx + sw * 0.10, by - h),
                 (cx - sw * 0.34, by - h * 0.80), (cx - sw * 0.16, by - h * 0.50)]
        else:
            r = h * (0.42 if kind == 'citrus' else 0.36)
            d = rough_circle(cx, by - r, r, rng=q)
            p = None
        if p is not None:
            amp = {'tall': 0.022, 'short': 0.022, 'dash': 0.024, 'jar': 0.020,
                   'can': 0.020, 'sprig': 0.03}[kind]
            d = spath(wob(p, max(0.4, w * amp), q), close=True)
        g = [drop(d, h, 0.14, max(1.2, h * 0.030), max(1.0, h * 0.022)),
             '<path d="%s" fill="%s"/>' % (d, col)]
        if fine and h > 46:
            inner = []
            if kind in BOTTLES:
                inner.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" '
                             'fill="#FFFFFF" opacity="0.26"/>'
                             % (cx - w * 0.44, by - h * 0.56, max(1.6, w * 0.09), h * 0.48,
                                max(0.8, w * 0.045)))
                ly, lh = by - h * 0.31, h * 0.10
                inner.append('<path d="%s" fill="%s" opacity="0.92"/>'
                             % (rbox(cx - w * 0.28, ly - lh, cx + w * 0.28, ly + lh, 0.35, q),
                                mix(GROUND, '#FFFFFF', 0.55)))
            if kind == 'citrus':
                r = h * 0.42
                inner.append('<path d="%s" fill="#FFF6E0" opacity="0.55"/>'
                             % rough_circle(cx, by - r, r * 0.80, rng=q))
                inner.append('<path d="%s" fill="%s"/>' % (rough_circle(cx, by - r, r * 0.72, rng=q), col))
                for i in range(7):
                    a = i * math.pi / 3.5 + q.uniform(-0.08, 0.08)
                    inner.append('<path d="%s" stroke="#FFF6E0" stroke-width="%.1f" fill="none" '
                                 'opacity="0.9"/>'
                                 % (rough_line(cx, by - r, cx + r * 0.70 * math.cos(a),
                                               by - r + r * 0.70 * math.sin(a), 0.5, q),
                                    max(1.0, r * 0.11)))
            if inner:
                g.append(clipped(cid, d, inner))
        g.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.1f" opacity="0.9"/>'
                 % (d, INK if chroma > 0.7 else FAINT, 1.0 + 0.9 * min(1.0, h / 90)))
        return ''.join(g), w


# ---------------------------------------------------------------- A · cut paper  (the shipped art)
class CutPaper(Treatment):
    key, title = 'cutpaper', 'A · Cut paper — chosen, and shipped'
    note = ('No outline anywhere. Three or four papers per object — body, closure, and a shadow '
            'laid over everything to the right of one straight cut. The cast shadow does the work '
            'the keyline used to.')

    LIGHT = 0.78                                     # the shadow paper, as a shade of the body
    CAP = 0.66                                       # the closure paper
    CAPY = {'jar': 0.86, 'can': 0.90}                # where the closure starts; default below

    @classmethod
    def paint(cls, kind, raw, col, chroma, cx, by, h, q, cid, fine):
        # Every tone is a shade of the *rationed* colour, and the shade itself is rationed by tier
        # as well: a full-strength shadow paper on all ninety would make the quiet half of the page
        # heavier than the top shelf, which is the one thing the encoding cannot afford.
        light = cls.LIGHT + (1 - cls.LIGHT) * 0.62 * (1 - chroma)
        sh = shade(col, light)
        far = h * 1.4
        if kind in PROFILES:
            d, w = body(cx, by, h, kind, q, amp=max(0.5, h * 0.010), smooth=False)
        elif kind == 'sprig':
            d, w = leaf(cx, by, h, q)
        else:
            r = h * (R_CITRUS if kind == 'citrus' else R_CHERRY)
            d, w = rough_circle(cx, by - r, r, amp=max(0.5, r * 0.035),
                                n=max(7, int(r / 3.4) + 6), rng=q), r * 2

        def cut(pts, fill, op=None):
            return ('<path d="%s" fill="%s"%s/>'
                    % (spath(pts, close=True, smooth=False), fill,
                       '' if op is None else ' opacity="%.2f"' % op))

        g = ['<g transform="rotate(%.2f %.1f %.1f)">' % (q.uniform(-1.1, 1.1), cx, by),
             drop(d, h, 0.16 * (0.55 + 0.45 * chroma)),
             '<path d="%s" fill="%s"/>' % (d, col)]
        inner = []

        if kind in BOTTLES:
            xs = cx + w * q.uniform(0.06, 0.15)                   # the one straight cut
            cap = shade(col, cls.CAP + (1 - cls.CAP) * 0.58 * (1 - chroma))
            cy = by - h * cls.CAPY.get(kind, 0.885)
            e = max(0.35, h * 0.008)                              # the closure cut, off true
            cyl, cyr = cy + q.uniform(-e, e), cy + q.uniform(-e, e)
            cym = cyl + (cyr - cyl) * ((xs - (cx - far)) / (2 * far))
            inner.append(cut([(xs, by + far), (cx + far, by + far), (cx + far, cyr), (xs, cym)], sh))
            inner.append(cut([(cx - far, cyl), (cx + far, cyr), (cx + far, by - far),
                              (cx - far, by - far)], cap))
            inner.append(cut([(xs, cym), (cx + far, cyr), (cx + far, by - far), (xs, by - far)],
                             shade(cap, light)))
        elif kind == 'sprig':
            xs = cx + w * q.uniform(0.02, 0.12)
            inner.append(cut([(xs, by + far), (cx + far, by + far), (cx + far, by - far),
                              (xs, by - far)], sh))
            if fine and h > 46:                                   # the vein, cut out of the leaf
                inner.append('<path d="%s" stroke="%s" stroke-width="%.1f" fill="none"/>'
                             % (rough_line(cx - w * 0.04, by - h * 0.06, cx + w * 0.06,
                                           by - h * 0.94, 0.4, q), GROUND, max(0.9, w * 0.075)))
        else:
            r = h * (R_CITRUS if kind == 'citrus' else R_CHERRY)
            if kind == 'citrus':                                  # rind, then flesh, then segments
                inner.append('<path d="%s" fill="%s"/>'
                             % (rough_circle(cx, by - r, r * 0.78, amp=max(0.4, r * 0.030),
                                             n=max(7, int(r / 3.4) + 6), rng=q),
                                mix(col, GROUND, 0.52)))
                if fine and h > 46:
                    for i in range(8):
                        a0 = i * math.pi / 4 + q.uniform(-0.05, 0.05)
                        inner.append(cut([(cx, by - r),
                                          (cx + r * 0.84 * math.cos(a0 - 0.055),
                                           by - r + r * 0.84 * math.sin(a0 - 0.055)),
                                          (cx + r * 0.84 * math.cos(a0 + 0.055),
                                           by - r + r * 0.84 * math.sin(a0 + 0.055))], col))
            # a flat disc lit from the left keeps its shadow as a crescent, not a straight cut
            inner.append('<path d="%s %s" fill-rule="evenodd" fill="%s"/>'
                         % (d, rough_circle(cx - r * 0.30, by - r, r, amp=max(0.4, r * 0.030),
                                            n=max(7, int(r / 3.4) + 6), rng=q), sh))

        g.append(clipped(cid, d, inner))
        g.append('</g>')
        return ''.join(g), w


# ---------------------------------------------------------------- B · botanical plate
class Plate(Treatment):
    key, title = 'plate', 'B · Botanical plate'
    note = ('A fine ink contour at one weight, a wash sitting inset so a hairline of paper shows '
            'inside the line, and engraved hatch on the shoulder. Line-led: the tail becomes a '
            'fence of ink, not of colour.')

    @classmethod
    def paint(cls, kind, raw, col, chroma, cx, by, h, q, cid, fine):
        line = mix(INK, GROUND, 0.0 if chroma > 0.7 else 0.42)
        lw = 0.9 + 0.7 * min(1.0, h / 110)
        if kind in PROFILES:
            d, w = body(cx, by, h, kind, q)
            wash, _ = body(cx, by, h, kind, random.Random(q.random() * 1e6),
                           sx=0.94, sy=0.972, dy=-h * 0.008)
        elif kind == 'sprig':
            d, w = leaf(cx, by, h, q)
            wash = d
        else:
            r = h * (R_CITRUS if kind == 'citrus' else R_CHERRY)
            d, w = rough_circle(cx, by - r, r, rng=q), r * 2
            wash = rough_circle(cx, by - r, r * 0.90, rng=q)
        g = ['<path d="%s" fill="%s" opacity="0.82"/>' % (wash, col)]
        inner = []
        if fine and h > 46:
            if kind in BOTTLES:
                n = int(h / 13)
                for i in range(n):                                  # engraved shoulder hatch
                    yy = by - h * (0.30 + 0.030 * i)
                    inner.append('<path d="%s" stroke="%s" stroke-width="%.1f" fill="none" '
                                 'opacity="0.20"/>'
                                 % (rough_line(cx + w * 0.16, yy, cx + w * 0.46, yy - h * 0.018,
                                               0.35, q), line, max(0.6, lw * 0.55)))
            if kind == 'citrus':
                r = h * R_CITRUS
                inner.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.1f" '
                             'opacity="0.55"/>' % (rough_circle(cx, by - r, r * 0.74, rng=q),
                                                   line, max(0.6, lw * 0.7)))
                for i in range(8):
                    a = i * math.pi / 4 + q.uniform(-0.06, 0.06)
                    inner.append('<path d="%s" stroke="%s" stroke-width="%.1f" fill="none" '
                                 'opacity="0.45"/>'
                                 % (rough_line(cx, by - r, cx + r * 0.72 * math.cos(a),
                                               by - r + r * 0.72 * math.sin(a), 0.4, q),
                                    line, max(0.55, lw * 0.6)))
        if inner:
            g.append(clipped(cid, d, inner))
        g.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.1f" opacity="0.92" '
                 'stroke-linejoin="round"/>' % (d, line, lw))
        if kind == 'cherry':
            g.append('<path d="%s" stroke="%s" stroke-width="%.1f" fill="none" opacity="0.8"/>'
                     % (stem(cx, by, h, q), line, max(0.7, lw * 0.8)))
        return ''.join(g), w


# ---------------------------------------------------------------- C · glass and liquid
class Glass(Treatment):
    key, title = 'glass', 'C · Glass & liquid'
    note = ('The vessel is glass and the colour is what is in it, filled to a level. Pale above, '
            'full below. Across ninety marks the fill line becomes a waterline running the shelf.')

    FILL = 0.66

    @classmethod
    def paint(cls, kind, raw, col, chroma, cx, by, h, q, cid, fine):
        pale = mix(raw, GROUND, 1 - chroma * 0.26)
        if kind in PROFILES:
            d, w = body(cx, by, h, kind, q)
        elif kind == 'sprig':
            d, w = leaf(cx, by, h, q)
        else:
            r = h * (R_CITRUS if kind == 'citrus' else R_CHERRY)
            d, w = rough_circle(cx, by - r, r, rng=q), r * 2
        g = [drop(d, h, 0.10)]
        if kind in BOTTLES:
            g.append('<path d="%s" fill="%s"/>' % (d, pale))
            lv = by - h * cls.FILL
            inner = ['<path d="%s" fill="%s"/>'                     # the liquid, with a meniscus
                     % (spath(wob([(cx - w, lv), (cx - w * 0.3, lv + q.uniform(-0.8, 0.4)),
                                   (cx + w * 0.3, lv + q.uniform(-0.4, 0.8)), (cx + w, lv),
                                   (cx + w, by + 3), (cx - w, by + 3)],
                                  max(0.3, h * 0.006), q), close=True), col)]
            capy = by - h * (0.86 if kind == 'jar' else 0.885)
            inner.append('<path d="%s" fill="%s"/>'                 # cork / foil closure
                         % (spath([(cx - w, capy), (cx + w, capy), (cx + w, by - h - 3),
                                   (cx - w, by - h - 3)], close=True, smooth=False),
                            mix(CORK if kind in ('tall', 'dash') else shade(raw, 0.70),
                                GROUND, 1 - chroma)))
            if fine and h > 46:
                inner.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" '
                             'fill="#FFFFFF" opacity="0.42"/>'
                             % (cx - w * 0.40, by - h * 0.60, max(1.6, w * 0.075), h * 0.44,
                                max(0.8, w * 0.04)))
            g.append(clipped(cid, d, inner))
        else:
            g.append('<path d="%s" fill="%s"/>' % (d, col))
            if fine and h > 46 and kind == 'citrus':
                r = h * R_CITRUS
                g.append(clipped(cid, d, [
                    '<path d="%s" fill="%s"/>' % (rough_circle(cx, by - r, r * 0.80, rng=q),
                                                  mix(col, GROUND, 0.55)),
                    '<path d="%s" fill="%s"/>' % (rough_circle(cx, by - r, r * 0.70, rng=q), col)]))
        g.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.1f" opacity="0.75"/>'
                 % (d, mix(shade(raw, 0.55), GROUND, 1 - chroma * 0.9),
                    0.9 + 0.8 * min(1.0, h / 110)))
        if kind == 'cherry':
            g.append('<path d="%s" stroke="%s" stroke-width="%.1f" fill="none" opacity="0.7"/>'
                     % (stem(cx, by, h, q), shade(raw, 0.5), max(0.7, h * 0.016)))
        return ''.join(g), w


# ---------------------------------------------------------------- D · riso two-plate
class Riso(Treatment):
    key, title = 'riso', 'D · Riso two-plate'
    note = ('Colour block printed off-register under an ink key drawing. Deliberate '
            'misregistration — reads as a print process at 130px; at 37px it doubles every edge.')

    @classmethod
    def paint(cls, kind, raw, col, chroma, cx, by, h, q, cid, fine):
        off = (max(2.0, h * 0.036), max(1.7, h * 0.031))
        if kind in PROFILES:
            d, w = body(cx, by, h, kind, q)
        elif kind == 'sprig':
            d, w = leaf(cx, by, h, q)
        else:
            r = h * (R_CITRUS if kind == 'citrus' else R_CHERRY)
            d, w = rough_circle(cx, by - r, r, rng=q), r * 2
        line = mix(INK, GROUND, 0.0 if chroma > 0.7 else 0.34)
        g = ['<path d="%s" fill="%s" opacity="0.92" transform="translate(%.1f,%.1f)"/>'
             % (d, col, off[0], off[1])]
        inner = []
        if fine and h > 46:
            if kind in BOTTLES:                                     # key drawing: shoulder + band
                sy = by - h * (0.68 if kind == 'tall' else 0.60)
                inner.append('<path d="%s" stroke="%s" stroke-width="%.1f" fill="none" '
                             'opacity="0.55"/>'
                             % (rough_line(cx - w * 0.46, sy, cx + w * 0.46, sy + 0.6, 0.5, q),
                                line, max(0.7, h * 0.012)))
                for i in range(int(h / 22)):
                    yy = by - h * (0.20 + 0.035 * i)
                    inner.append('<path d="%s" stroke="%s" stroke-width="%.1f" fill="none" '
                                 'opacity="0.24"/>'
                                 % (rough_line(cx - w * 0.40, yy, cx - w * 0.12, yy - h * 0.010,
                                               0.3, q), line, max(0.6, h * 0.009)))
            if kind == 'citrus':
                r = h * R_CITRUS
                for i in range(8):
                    a = i * math.pi / 4 + q.uniform(-0.05, 0.05)
                    inner.append('<path d="%s" stroke="%s" stroke-width="%.1f" fill="none" '
                                 'opacity="0.5"/>'
                                 % (rough_line(cx, by - r, cx + r * 0.78 * math.cos(a),
                                               by - r + r * 0.78 * math.sin(a), 0.4, q),
                                    line, max(0.6, r * 0.06)))
        if inner:
            g.append(clipped(cid, d, inner))
        g.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.1f" opacity="0.92" '
                 'stroke-linejoin="round"/>' % (d, line, 1.0 + 0.9 * min(1.0, h / 110)))
        if kind == 'cherry':
            g.append('<path d="%s" stroke="%s" stroke-width="%.1f" fill="none" opacity="0.85"/>'
                     % (stem(cx, by, h, q), line, max(0.7, h * 0.016)))
        return ''.join(g), w


# ---------------------------------------------------------------- E · apothecary label
class Apothecary(Treatment):
    key, title = 'apothecary', 'E · Apothecary label'
    note = ('Pale glass body, and the colour is carried by a full-width label band plus the '
            'closure. Across the tail the bands line up into a dashed rule at mid-height.')

    BAND = 0.34

    @classmethod
    def paint(cls, kind, raw, col, chroma, cx, by, h, q, cid, fine):
        pale = mix(raw, GROUND, 1 - chroma * 0.22)
        line = mix(shade(raw, 0.50), GROUND, 1 - chroma * 0.85)
        if kind in PROFILES:
            d, w = body(cx, by, h, kind, q)
        elif kind == 'sprig':
            d, w = leaf(cx, by, h, q)
        else:
            r = h * (R_CITRUS if kind == 'citrus' else R_CHERRY)
            d, w = rough_circle(cx, by - r, r, rng=q), r * 2
        g = [drop(d, h, 0.10)]
        if kind in BOTTLES:
            g.append('<path d="%s" fill="%s"/>' % (d, pale))
            b0 = by - h * 0.20
            b1 = b0 - max(5.0, h * cls.BAND)
            inner = ['<path d="%s" fill="%s"/>'
                     % (rbox(cx - w, b1, cx + w, b0, max(0.3, h * 0.007), q), col)]
            capy = by - h * (0.86 if kind == 'jar' else 0.885)
            inner.append('<path d="%s" fill="%s"/>'
                         % (spath([(cx - w, capy), (cx + w, capy), (cx + w, by - h - 3),
                                   (cx - w, by - h - 3)], close=True, smooth=False), col))
            if fine and h > 46:                                     # a rule of type on the label
                for i, fy in enumerate((0.34, 0.56, 0.72)):
                    ly = b1 + (b0 - b1) * fy
                    ww = w * (0.52 if i == 0 else 0.36 if i == 1 else 0.28)
                    inner.append('<path d="%s" stroke="%s" stroke-width="%.1f" fill="none" '
                                 'opacity="%.2f"/>'
                                 % (rough_line(cx - ww / 2, ly, cx + ww / 2, ly + 0.4, 0.3, q),
                                    GROUND, max(0.9, h * 0.014), 0.75 if i == 0 else 0.5))
            g.append(clipped(cid, d, inner))
        else:
            g.append('<path d="%s" fill="%s"/>' % (d, col))
            if fine and h > 46 and kind == 'citrus':
                r = h * R_CITRUS
                g.append(clipped(cid, d, [
                    '<path d="%s" fill="%s"/>' % (rough_circle(cx, by - r, r * 0.78, rng=q),
                                                  mix(col, GROUND, 0.60))]))
        g.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.1f" opacity="0.8"/>'
                 % (d, line, 0.9 + 0.8 * min(1.0, h / 110)))
        if kind == 'cherry':
            g.append('<path d="%s" stroke="%s" stroke-width="%.1f" fill="none" opacity="0.75"/>'
                     % (stem(cx, by, h, q), line, max(0.7, h * 0.016)))
        return ''.join(g), w


OPTIONS = [Current, CutPaper, Plate, Glass, Riso, Apothecary]
TREATMENTS = dict((t.key, t) for t in OPTIONS)


def get(key=None):
    return TREATMENTS[key or os.environ.get('TREATMENT') or 'cutpaper']
