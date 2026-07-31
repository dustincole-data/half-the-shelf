"""Pull the whole free tier of TheCocktailDB, one request per starting letter. No key, no rate limit
worth worrying about, 26 requests. Writes data/raw/L_<letter>.json; prep.py turns those into
data/cocktails.json."""
import json, os, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, 'data', 'raw')
URL = 'https://www.thecocktaildb.com/api/json/v1/1/search.php?f=%s'

os.makedirs(RAW, exist_ok=True)
total = 0
for letter in 'abcdefghijklmnopqrstuvwxyz':
    with urllib.request.urlopen(URL % letter, timeout=30) as r:
        body = r.read().decode('utf-8')
    open(os.path.join(RAW, 'L_%s.json' % letter), 'w', encoding='utf-8').write(body)
    n = len(json.loads(body).get('drinks') or [])
    total += n
    print('%s %3d' % (letter, n))
print('fetched %d drink records (before de-duplication)' % total)
