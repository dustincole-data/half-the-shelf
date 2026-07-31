# Half the Shelf

A data graphic about what a cocktail canon is actually made of.

**The finding, and the whole point of the piece:** these 143 classic cocktails call for 177 different
ingredients, and **90 of them appear in exactly one drink and nothing else** — 51% of the bottles, 16%
of the pour. Two in five of the drinks (59 of 143) need at least one ingredient no other drink uses,
and the thirty best-chosen bottles you could buy would still complete only 22 of the 143.

Every number on the page is computed from the source at build time. Nothing is asserted by hand.

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
| Used once only | 90 |
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
and the shade is rationed a second time by tier, so the ninety stay quieter than the top shelf
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
130px, at 37px, and a real slice of the ninety at 37px and half chroma — the only test that matters
being whether the tail stays a picket fence.

**Cut paper won, and was then finished.** All six live on in `src/treatments.py`, the previously
shipped drawing among them as `current`, so the comparison is rebuildable rather than remembered.

## Open

- **Interaction.** The piece is a static SVG. Hovering an ingredient to reveal the drinks that use it
  (and ghosting the rest of the shelf) is designed but not built.
- **Ground.** White, chosen 2026-07-31 over the warm cream it was drafted on.
