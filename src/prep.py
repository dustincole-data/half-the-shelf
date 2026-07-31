import json, glob, collections, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data')

drinks = {}
for f in glob.glob(os.path.join(DATA, 'raw', 'L_*.json')):
    for x in (json.load(open(f, encoding='utf-8')).get('drinks') or []):
        drinks[x['idDrink']] = x

alc = [x for x in drinks.values() if x['strAlcoholic'] == 'Alcoholic']
SET = {x['idDrink']: x for x in alc if x['strIBA'] or x['strCategory'] == 'Cocktail'}

# --- base spirit, derived from the ingredient list by substring match, first match wins ---
RULES = [
    ('Whisky',  ['scotch', 'bourbon', 'whiskey', 'whisky', 'rye ', 'jack daniels', 'wild turkey', 'crown royal']),
    ('Tequila', ['tequila', 'mezcal']),
    ('Rum',     ['rum', 'cachaca', 'cachaça', 'bacardi']),
    ('Gin',     ['gin']),
    ('Vodka',   ['vodka']),
    ('Brandy',  ['cognac', 'brandy', 'applejack', 'calvados', 'pisco', 'armagnac']),
    ('Wine',    ['champagne', 'prosecco', 'vermouth', 'sherry', 'port', 'wine', 'lillet', 'sparkling']),
]
def ingredients(d):
    out = []
    for i in range(1, 16):
        v = (d.get('strIngredient%d' % i) or '').strip()
        if v:
            out.append(v)
    return out

def base_of(ings):
    low = [i.lower() for i in ings]
    for name, keys in RULES:
        for k in keys:
            for ing in low:
                if k in ing:
                    # 'gin' must not match 'ginger'
                    if k == 'gin' and 'ginger' in ing:
                        continue
                    return name
    return 'Liqueur'

GLASS = {
    'cocktail glass': 'Coupe / cocktail', 'cocktail Glass': 'Coupe / cocktail',
    'martini glass': 'Coupe / cocktail', 'coupe glass': 'Coupe / cocktail',
    'nick and nora glass': 'Coupe / cocktail', 'margarita/coupette glass': 'Coupe / cocktail',
    'margarita glass': 'Coupe / cocktail', 'champagne flute': 'Flute',
    'highball glass': 'Highball', 'collins glass': 'Highball', 'pint glass': 'Highball',
    'old-fashioned glass': 'Rocks', 'whiskey glass': 'Rocks', 'copper mug': 'Rocks',
    'mason jar': 'Rocks', 'jar': 'Rocks',
    'shot glass': 'Shot', 'cordial glass': 'Shot', 'pousse cafe glass': 'Shot',
    'whiskey sour glass': 'Sour', 'hurricane glass': 'Tall / tiki',
    'beer mug': 'Tall / tiki', 'beer glass': 'Tall / tiki', 'beer pilsner': 'Tall / tiki',
    'punch bowl': 'Bowl / pitcher', 'pitcher': 'Bowl / pitcher',
    'coffee mug': 'Mug', 'irish coffee cup': 'Mug',
    'brandy snifter': 'Snifter', 'balloon glass': 'Snifter',
    'wine glass': 'Wine', 'white wine glass': 'Wine',
}

rows = []
for d in SET.values():
    ings = ingredients(d)
    g = GLASS.get(d['strGlass'].strip().lower(), 'Other')
    rows.append({
        'id': d['idDrink'],
        'name': d['strDrink'],
        'base': base_of(ings),
        'glass_raw': d['strGlass'],
        'glass': g,
        'ings': ings,
        'n': len(ings),
        'iba': d['strIBA'],
        'cat': d['strCategory'],
    })
rows.sort(key=lambda r: r['name'])

# --- counts, all verified here and printed ---
bc = collections.Counter(r['base'] for r in rows)
gc = collections.Counter(r['glass'] for r in rows)
# An ingredient is counted once per drink that calls for it, not once per slot: three drinks
# (Kiwi Martini, Mango Mojito, Whiskey Sour) list the same ingredient twice, and the piece says
# "how many of the 143 drinks call for it", which is a count of drinks.
ic = collections.Counter()
for r in rows:
    for i in set(x.strip().lower() for x in r['ings']):
        ic[i] += 1
pour = collections.Counter()                    # slots, for the share-of-the-pour line
for r in rows:
    for i in r['ings']:
        pour[i.strip().lower()] += 1
nc = collections.Counter(r['n'] for r in rows)
ibac = collections.Counter(r['iba'] for r in rows)

# ingredient -> set of drinks, for the network
ing_drinks = collections.defaultdict(list)
for r in rows:
    for i in sorted(set(x.strip().lower() for x in r['ings'])):
        ing_drinks[i].append(r['id'])

# --- how far a shelf actually gets you ---
# At each step take the bottle that finishes the most drinks next, ties broken by how many drinks
# the bottle appears in at all. This is a greedy lower bound on the best possible thirty, not a
# proof of optimality, so the wording on the page claims only what this computes.
sets = [set(i.strip().lower() for i in r['ings']) for r in rows]
own, curve = set(), []
for _ in range(40):
    pick, pg, pf = None, -1, -1
    for k in ic:
        if k in own:
            continue
        own.add(k)
        g = sum(1 for s in sets if s <= own)
        own.discard(k)
        if g > pg or (g == pg and ic[k] > pf):
            pick, pg, pf = k, g, ic[k]
    own.add(pick)
    curve.append([pick, pg])

stats = {
    'n_drinks': len(rows),
    'greedy': curve,
    'base': bc.most_common(),
    'glass': gc.most_common(),
    'n_ingredients_distinct': len(ic),
    'ingredient_top': ic.most_common(40),
    'ingredients_shared': sum(1 for k, v in ic.items() if v > 1),
    'slots': sum(pour.values()),
    'pour_single': sum(pour[k] for k, v in ic.items() if v == 1),
    'ings_per_drink': sorted(nc.items()),
    'iba': ibac.most_common(),
}
json.dump({'rows': rows, 'ing_drinks': {k: v for k, v in ing_drinks.items()}, 'stats': stats},
          open(os.path.join(DATA, 'cocktails.json'), 'w', encoding='utf-8'), indent=1)

for k, v in stats.items():
    print(k, '=', v)
