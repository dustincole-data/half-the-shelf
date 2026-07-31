# Half the Shelf

A data graphic about what a cocktail canon is actually made of.

**The finding, and the whole point of the piece:** these 143 classic cocktails call for 177 different
ingredients, and **92 of them appear in exactly one drink and nothing else** — 52% of the bottles, 16%
of the pour. More than two in five of the drinks (61 of 143) need at least one ingredient no other
drink uses, and thirty bottles, each chosen to unlock the most drinks, still make only 28 of the 143.

Every number on the page is computed from the source at build time. Nothing is asserted by hand.
That was not true until 2026-07-31, and it cost the piece five numbers. See **The audit** below.

## The audit

Two rounds of it, both on 2026-07-31.

**The thirty-bottle figure was a hand-typed `22`,** and wrong on either reading — the thirty
*most-used* bottles finish 21, thirty *greedily-chosen* ones finish 28. It is now computed in
`prep.py` and read by both surfaces. The pick is greedy, which is a lower bound and not a proof of
optimality, so the sentence claims only what the code computes.

**Then the bigger one: the piece was counting pours, not drinks,** while saying out loud that it
counted drinks. Three drinks list the same ingredient in two slots — *Kiwi Martini* (kiwi),
*Mango Mojito* (mango), *Whiskey Sour* (lemon) — and every count was built on slots. The stated
encoding ("its height is how many of the 143 drinks call for it") was false for those three, and
five published numbers were wrong:

| | stated | true |
|---|---|---|
| appear in exactly one drink | 90 | **92** |
| as a share of the bottles | 51% | **52%** |
| drinks needing a bottle nothing else uses | 59 | **61** |
| the *two to four* shelf | 53 | **51** |
| the *one drink* shelf | 90 | **92** |

`USE` now counts drinks and `POUR` keeps the slot count, which is what the share-of-the-pour line
actually wants (that one was right at 16%). Kiwi and mango moved down a shelf, where they belong.
Every remaining sentence — the deck, the red annotation, the source line — is now computed in
`layout.py` rather than typed, and `site.py` asserts at build time that the index and the poster
describe the same set, so the two can never disagree again.

## Where it came from

Spun out of [design-inspo](../design-inspo/) on 2026-07-31. That project is about *how* to design a
premium data graphic; this was its practice dataset, and the illustrated version was good enough to
finish on its own terms. The design-inspo work continues separately and does not depend on this repo.

## Run it

```
python src/fetch.py          # 26 requests to TheCocktailDB, no key needed  -> data/raw/
python src/prep.py           # derive the set and print every count         -> data/cocktails.json
python src/shelf.py          # the poster                                   -> out/shelf.svg
python src/render.py shelf 1000 1250                                     #  -> out/shelf.png
python src/options.py        # every art treatment, judged side by side     -> out/options.png
python src/site.py           # the same piece, interactive                  -> out/site/index.html
```

`TREATMENT=<key> SHELF_OUT=<name> python src/shelf.py` draws the poster with any of the treatments
in `src/treatments.py` instead of the shipped one.

`src/constellation.py` builds the alternate treatment of the same finding as a force-directed
constellation — the version that lost the pick but is worth keeping.

## The data, and what it is not

Source: **TheCocktailDB** free API v1, `search.php?f=a..z`. 426 unique drinks come back; 380 are
alcoholic. The set is the **143** that are either on the **IBA official list** (61) or in
TheCocktailDB's own **Cocktail** category. Verified counts, printed by `prep.py` on every run:

| | |
|---|---|
| Drinks | 143 |
| Base spirits | Gin 41 · Rum 29 · Vodka 24 · Whisky 17 · Liqueur 10 · Tequila 8 · Wine 7 · Brandy 7 |
| Glass families | 11 |
| Distinct ingredients | 177, across 579 ingredient slots |
| Used in one drink only | 92 |
| Ingredients per drink | 2 to 7 (median 4) |
| IBA classes | Unforgettables 25 · Contemporary Classics 22 · New Era Drinks 14 |

**Base spirit is derived**, not a field — read from the ingredient list by first match, spirits before
liqueurs, with the residual `Liqueur` bucket placed last and allowed to stay large.

Two things the source does not carry, stated rather than worked around:

- **No era of invention.** The IBA three-band class (*Unforgettables* / *Contemporary Classics* /
  *New Era Drinks*) is the only time-like axis, and it covers 61 of the 143. There is no year field.
- **No ABV.** Deriving it would need an invented per-ingredient strength table, so the piece uses
  ingredient count as its quantity instead.

## How the drawing works

Every mark is a **drawn object**, not a plotted shape: bottle, jar, dash bottle, can, citrus wheel,
cherry, sprig. Which one an ingredient gets is decided by keyword (`kind_of` in `src/layout.py`), and
its colour is the colour the thing actually is (`col_of`). Every path is wobbled off true, so nothing
in the piece is a perfect primitive.

**Height is the encoding:** `h = 20 + 17·√(drinks using it)` — 37px at one drink, 130px at forty-two.

**Colour is rationed by tier, not by count.** The top two shelves run at full chroma; the 2-to-4 shelf
is mixed 74% toward the ground; the one-drink shelf 50%. Half the page is deliberately almost colourless,
which is what makes the finding visible before any label is read.

**The objects are cut paper.** No outline anywhere. Each one is three or four flat papers — the
body, its closure, and a shadow laid over everything to the right of a single straight cut — and the
cast shadow does the job a keyline used to. Every tone is a *shade of the already-rationed colour*,
and the shade is rationed a second time by tier, so the tail stays quieter than the top shelf
instead of being dragged back up by their own shadows. A flat disc gets a crescent rather than a
straight cut, because that is what a disc lit from the left actually does.

Two craft rules are enforced in code rather than by eye, because both were shipped wrong first:

- **Interior detail is clipped to its own silhouette.** Shadow and closure papers are cut oversize
  and trimmed by the object's own outline, so they physically cannot escape it at any size.
- **Type never starts until it clears the object's baseline, its cast shadow and its own cap height.**
  Labels wrap to two lines rather than truncate; the count sits on a fixed baseline so a wrapped name
  cannot push its number out of line.

### The art was judged as options before it was chosen

The open item on this piece was a second pass on the object art. On 2026-07-31 five drawn treatments
of the same eight archetypes were built against the same data, layout and encoding — **cut paper**,
**botanical plate** (ink contour, inset wash, engraved hatch), **glass & liquid** (glass vessel,
colour is the liquid, a waterline across the shelf), **riso two-plate** (colour block off-register
under an ink key) and **apothecary label** (pale glass, colour carried by a label band). Each was
judged on one screen: the whole poster as a thumbnail, plus a 1:1 strip of the eight archetypes at
130px, at 37px, and a real slice of the tail at 37px and half chroma — the only test that matters
being whether the tail stays a picket fence.

**Cut paper won, and was then finished.** All six live on in `src/treatments.py`, the previously
shipped drawing among them as `current`, so the comparison is rebuildable rather than remembered.

## The interactive one

`out/site/index.html` — one file, no build step, no dependencies, no network. Same data, same
geometry, same cut-paper art; `src/shelfgrid.py` holds the placement both of them read, so a bottle
cannot move on one and not the other.

It exists because of a limit the recipe names outright: a shelf is a distribution, and the
ingredient-to-drink structure is a genuine bipartite graph that a static page cannot show. So the
page shows it.

- **Point at a bottle.** The other 176 ghost, and a card names every drink that calls for it. Point
  at something in the tail and the card says *pours one drink, nothing else*, names that drink, and
  lists what else you would have to own to make it.
- **Then jump the graph.** Click a drink and it lights every bottle it needs, wherever they are on
  the page. Click one of those and you are back on the ingredient side.
- **Buy the shelf.** The page empties and you fill it a bottle at a time, or let it pick greedily
  for you. The counter is the finding, self-administered: thirty bottles, thirty lit marks scattered
  across a page of 177, and 28 drinks.
- **The ninety-two.** Below the poster, every single-use bottle filed under the one drink it exists
  for, worst offenders first — *Michelada* wants beer, hot sauce, soy sauce and Worcestershire;
  *Penicillin* wants two scotches and two syrups. Click any bottle and the page finds it back on the
  shelf and opens its card.

**The card is anchored to the bottle, not parked at the top of the page.** The first build put one
readout in the masthead, which meant that pointing at anything in the tail — 900px down, and the
entire point of the piece — put the answer off screen. The card now sits against the mark it
describes; below 720px it becomes a bottom sheet that is always in frame.

Anchoring reads each object's real drawn box out of `data-x/y/h/w`, **not** `getBBox()`: the
cut-paper shadow and closure papers are cut oversize and clipped away, and `getBBox()` still sees
them, which threw the card more than fifty pixels off the tallest bottles. Placement prefers above,
and when the poster is scaled down far enough that the tallest bottles leave no room, it goes
**beside** the mark rather than below it — flipping under sent gin's card three hundred pixels down
the page, nowhere near the bottle it was describing. Swept all 177 marks at 1280px and at 745px: none
covers its own bottle, leaves the page, or scrolls sideways.

Selection is bound to `pointerup`, never `click`, and hover is enabled only behind
`(hover:hover) and (pointer:fine)` — on iOS the first tap on a mark whose `pointerenter` mutates the
DOM gets swallowed, and the piece would need two taps to answer. Widths use `min(100%, …)` and never
`100vw`, which counts the scrollbar and hands you a horizontal one.

## Open

- **Phone tail.** At 390px the tail bottles are about 7px wide, so it is a pinch-zoom job and the
  page says so. Full-width is kept deliberately: squeezing the shelf is what makes the silhouette
  readable, and that silhouette is the whole argument.
- **Ground.** White, chosen 2026-07-31 over the warm cream it was drafted on.
- **Reproducibility.** Object seeds come from `hash(name)`, which Python salts per process, so every
  rebuild reshuffles the wobble. Same design, different hand. A one-line fix (`zlib.crc32`) that
  changes every path on the page, so it has not been taken.
