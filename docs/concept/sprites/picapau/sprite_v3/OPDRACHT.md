# Opdracht maker: Picapau sprite v3 (Gemini r5 namaken), 19 nov

Lees eerst: `docs/lessen/SPRITE_KERN.md` (verplicht), `docs/lessen/SPRITE_WERKWIJZE.md` → "Gemini-model namaken", `docs/lessen/GEMINI.md`.

**MODEL OVERNEMEN, NIET TEKENEN.** De sprite is de verkleining van het model zelf: natief raster terughalen → verkleinen (vlakgemiddelde + dichtstbijzijnde modelkleur) → alleen technisch opschonen (buitenlijn, ruis, ≤3 tinten per kleurgroep) en per pixel repareren wat de reductie kapotmaakt (oog, snavel, kuifpunten, tenen), steeds naar het model. Meld per zone hoeveel pixels afwijken van de kale reductie en benoem elke pixel die niet uit het model komt. Voorbeeld-scripts: `docs/concept/sprites/octillery_evo/sprite3/natief.py`, `half2.py`; meetgereedschap `poedelmot/kleur_r19/stappen/px.py`, `poedelmot/kleur_r20/stappen/box1x.py`.

## Model
`gemini/r5_verbeter.png` (= `referenties/gemini_gekozen_r5.png`), 1024×1024, Gemini-pixelraster. Jordi koos dit: hoek en pose zijn goed. Eindformaat 64×64, Pokémon onderaan gecentreerd zoals andere frontsprites. Huidige sprite ter vergelijking (alleen formaat/palet): `af/picapau.png`.

## Jordi letterlijk (19 nov)
- "die moet gewoon driekwart staan en voor de rest precies hetzelfde"
- "de hoek en pose vind ik prima. In de sprite betekent dat dat er 1 of 2 pixels max aan zwart oog boven de snavel uit komt."
- "alleen de vleugels/staart moeten pikachu kleuren krijgen, de rest mag je volledig hetzelfde palet aanhouden als picapau, dat was al een erg goed design" · "dus de vleugels moeten juist niet terug naar het origineel"
- Keuze: vleugels in Pikachu's bruin, staart roodbruin met Pikachu's donker roodbruin als schaduw.

## Kleuren (kleur mag van het model afwijken; vorm niet)
- Palet = `af/normal.pal` (Picapau): geel, rood wang, grijs snavel/poten, crème stippen, zwart, wit glans, enz.
- Vleugels: Pikachu-bruin `156 82 0` (licht) en `98 49 8` (donker) uit `graphics/pokemon/pikachu/normal.pal`; stippen crème `240 232 184` van Picapau.
- Staart: roodbruin (Picapau's staarttinten `200 130 72` / `186 96 44`) met Pikachu's `123 41 8` als schaduw.
- Max 16 kleuren incl. transparant (index 0 = `152 208 160`). Zet ongebruikte Picapau-wingtinten eruit om ruimte te maken.
- Licht linksboven, Gen 3-contrast (stappen ±30–40), gekleurde selout aan de lichtkant, zwart aan de schaduwkant.

## Oplevering per ronde
`sprite_v3/rN/picapau.png` (indexed, 64×64) + `normal.pal` + `vel.png` (rN | rN-1 | model verkleind op 8×, close-up kop op 12× naast het model, 1× op licht en donker). Commit niet zelf; rapporteer kort: afwijkingen per zone, eigen zwakke punten.
