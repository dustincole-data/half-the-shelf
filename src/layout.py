# Shared layout system for round 2. One grid, one type scale, one set of margins — both pieces obey it.
from draw import *

PW, PH = 1000, 1250
ML, MR, MT, MB = 76, 76, 72, 66
CW = PW - ML - MR                       # 848 content width
BL = 8                                  # baseline unit

T_DISPLAY, T_DECK, T_SECTION, T_LABEL, T_MICRO = 53, 17.5, 12, 12.5, 10.5
SANS = "'Century Gothic','Questrial','Futura',sans-serif"

# ---- the finding, computed once, used by both pieces ----
USE = collections.Counter()
for r in ROWS:
    for i in r['ings']:
        USE[i.strip().lower()] += 1
SLOTS = sum(USE.values())
SINGLE = set(k for k, v in USE.items() if v == 1)
SHARED = [k for k, v in USE.items() if v > 1]
N_WITH_SINGLE = sum(1 for r in ROWS if any(i.strip().lower() in SINGLE for i in r['ings']))

# How far a shelf actually gets you, computed in prep.py rather than asserted here. The pick is
# greedy, so this is what a good shopper can reach, not a proof that nobody could do better --
# which is exactly what the sentence on the page is allowed to claim.
GREEDY = S.get('greedy') or []
GREEDY_N = 30
GREEDY_MADE = GREEDY[GREEDY_N - 1][1] if len(GREEDY) >= GREEDY_N else 0
SHELF_LINE = ('Thirty bottles, each chosen to unlock the most drinks, still make only %d of the %d.'
              % (GREEDY_MADE, len(ROWS)))

HEADLINE_1 = 'Half the shelf'
HEADLINE_2 = 'pours one drink'
DECK = ('These 143 classic cocktails call for %d different ingredients. %d of them &#8212; more than '
        'half &#8212; appear in exactly one drink and' % (len(USE), len(SINGLE)))
DECK2 = ('nothing else. They are %d%% of the bottles and %d%% of what actually goes in a glass.'
         % (round(100 * len(SINGLE) / len(USE)), round(100 * len(SINGLE) / SLOTS)))


def txt(x, y, s, size=T_LABEL, fill='#2B251E', anchor='start', op=1.0, track=0, weight=None, fam=None):
    return ('<text x="%.1f" y="%.1f" text-anchor="%s" font-family="%s" font-size="%.1f" fill="%s"'
            '%s%s%s>%s</text>'
            % (x, y, anchor, fam or SANS, size, fill,
               ' opacity="%.2f"' % op if op < 1 else '',
               ' letter-spacing="%.1f"' % track if track else '',
               ' font-weight="%s"' % weight if weight else '', s))


# ---- what kind of object each ingredient is drawn as, and what colour it really is ----
KIND_RULES = [
    ('dash',   ['bitters', 'absinthe']),
    ('citrus', ['lemon', 'lime', 'orange', 'grapefruit']),
    ('sprig',  ['mint', 'basil', 'thyme', 'rosemary', 'cinnamon', 'nutmeg', 'clove', 'allspice',
                'ginger', 'pepper', 'salt', 'celery']),
    ('cherry', ['cherry', 'olive', 'berr', 'strawberr', 'raspberr', 'blackberr', 'grape']),
    ('jar',    ['syrup', 'sugar', 'honey', 'cream', 'milk', 'egg', 'butter', 'jam', 'chocolate',
                'coconut', 'yoghurt', 'ice']),
    ('can',    ['juice', 'soda', 'tonic', 'water', 'cola', 'ale', 'lemonade', 'beer', 'nectar',
                'puree', 'sauce']),
    ('short',  ['vermouth', 'liqueur', 'curacao', 'chartreuse', 'campari', 'aperol', 'schnapps',
                'creme de', 'triple sec', 'sec', 'kahlua', 'baileys', 'amaretto', 'sambuca',
                'galliano', 'benedictine', 'drambuie', 'grand marnier', 'cointreau', 'maraschino',
                'sherry', 'port', 'lillet', 'ricard', 'anis', 'amaro', 'jagermeister', 'goldschlager',
                'heering', 'midori', 'pisang', 'advocaat', 'chambord', 'frangelico', 'tia maria']),
]


def kind_of(name):
    n = name.lower()
    for k, keys in KIND_RULES:
        for key in keys:
            if key in n:
                return k
    return 'tall'                    # spirits, wines and anything else that comes in a bottle


COL_RULES = [
    ('#1F9E8E', ['gin']),            ('#8FBE2A', ['tequila', 'mezcal', 'agave', 'midori', 'chartreuse']),
    ('#E8A020', ['rum', 'cachaca', 'bourbon', 'honey']),
    ('#C9531D', ['whisk', 'scotch', 'rye', 'drambuie']),
    ('#9C2340', ['brandy', 'cognac', 'calvados', 'pisco', 'applejack', 'port']),
    ('#6E4DAE', ['wine', 'champagne', 'prosecco', 'vermouth', 'lillet', 'sherry', 'cassis']),
    ('#3E82D6', ['vodka', 'curacao', 'blue']),
    ('#D8383C', ['campari', 'cherry', 'grenadine', 'aperol', 'tomato', 'cranberr', 'raspberr',
                 'strawberr', 'heering', 'hot sauce']),
    ('#EFC02A', ['lemon', 'sugar', 'syrup', 'pineapple', 'banana', 'passion', 'apricot', 'mango']),
    ('#7FBE3F', ['lime', 'mint', 'basil', 'olive', 'apple', 'kiwi', 'melon', 'pisang']),
    ('#EF8B22', ['orange', 'peach', 'carrot', 'grand marnier', 'cointreau', 'triple sec']),
    ('#F3E4C4', ['cream', 'milk', 'egg', 'coconut', 'baileys', 'advocaat', 'yoghurt']),
    ('#6B4A2E', ['coffee', 'kahlua', 'cola', 'chocolate', 'cocoa', 'bitters', 'amaro', 'tia maria',
                 'jagermeister', 'benedictine', 'root beer']),
    ('#BFD8E8', ['soda', 'water', 'tonic', 'ice', 'sprite', 'lemonade', 'ginger ale']),
]


def col_of(name):
    n = name.lower()
    for c, keys in COL_RULES:
        for key in keys:
            if key in n:
                return c
    return '#B9A489'


def nice(name):
    s = name.strip()
    return esc(s[0].upper() + s[1:])
