# The shelf geometry the poster and the page both stand on. Placement only, no drawing, so the
# static piece and the interactive one cannot drift apart — if a bottle moves, it moves in both.
from layout import *


def h_of(u):
    return 20 + 17.0 * math.sqrt(u)          # 37 at one drink, 130 at forty-two


ITEMS = sorted(USE.items(), key=lambda kv: (-kv[1], kv[0]))
TIER1 = [x for x in ITEMS if x[1] >= 12]
TIER2 = [x for x in ITEMS if 5 <= x[1] < 12]
TIER3 = [x for x in ITEMS if 2 <= x[1] < 5]
TIER4 = [x for x in ITEMS if x[1] == 1]


def place(row, T):
    """Centre a row of ingredients across the content width, each object standing on its own
    footprint. Returns [(cx, name, uses, width)] and the gap the row settled on."""
    ws = [T.width(kind_of(nm), h_of(u)) for nm, u in row]
    gap = (CW - sum(ws)) / max(1, len(row) - 1)
    used = sum(ws) + gap * (len(row) - 1)
    x = ML + (CW - used) / 2
    out = []
    for (nm, u), w in zip(row, ws):
        out.append((x + w / 2, nm, u, w))
        x += w + gap
    return out, gap


def seed_of(name):
    return hash(name) & 0xffff


# Where each band sits on the 1000x1250 page. The poster and the page read the same numbers, so
# the interactive version is the printed one with the lights on, not a second composition.
STACK = [
    # (section head y, shelf baselines, chroma, label style, heading, note)
    (352, [504],        1.00, 'flat',   'IN TWELVE DRINKS OR MORE'),
    (586, [690],        1.00, 'turned', 'IN FIVE TO ELEVEN'),
    (828, [900, 956],   0.74, None,     'IN TWO TO FOUR'),
    (992, [1048, 1092], 0.50, None,     'IN ONE DRINK, AND NOTHING ELSE'),
]
TIERS = [TIER1, TIER2, TIER3, TIER4]
SPLIT = {2: 27, 3: 45}                     # where a tier breaks across two shelves
