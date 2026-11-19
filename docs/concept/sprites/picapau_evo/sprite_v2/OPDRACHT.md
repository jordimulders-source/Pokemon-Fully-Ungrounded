# Opdracht maker: Picaraio sprite v2 (Gemini r9 namaken), 19 nov

Lees eerst: `docs/lessen/SPRITE_KERN.md` (verplicht), `docs/lessen/SPRITE_WERKWIJZE.md` → "Gemini-model namaken", `docs/lessen/GEMINI.md`.

**MODEL OVERNEMEN, NIET TEKENEN.** De sprite is de verkleining van het model zelf: (fijne) pixelraster meten → verkleinen naar 64×64 (vlakgemiddelde + dichtstbijzijnde modelkleur) → alleen technisch opschonen (buitenlijn, ruis, ≤3 tinten per kleurgroep) en per pixel repareren wat de reductie kapotmaakt (oog, snavel, kuifslierten, staartkoord, tenen, stippen), steeds naar het model. Meld per zone hoeveel pixels afwijken van de kale reductie en benoem elke pixel die niet uit het model komt. Voorbeeldscripts: `docs/concept/sprites/picapau/sprite_v3/r1/` (natief.py, reduce.py, schoon.py, repareer.py; net gebruikt voor Picapau), `octillery_evo/sprite3/`.

## Model
`gemini/r9_prompt_v6.png` (= `referenties/gemini_gekozen_r9.png`), 1024×1024, fijn gepixeld (geen 64-raster). Ontwerp = de illustratie `gemini/r7_prompt_v5_illustratie.png` (Jordi: "uitstekend, maar het is geen sprite"); r9 is daarvan de gepixelde versie. Bij twijfel over een vorm: r7 toont het ontwerp scherper.
Eindformaat 64×64, hele vogel incl. bliksem en staartlus binnen het kader (eindvorm: mag het kader groot vullen, marge ±1 px), onderaan/gecentreerd zoals andere frontsprites. Kijkt naar links.

## Jordi letterlijk (19 nov)
- Opdracht: "Picaraio mag iets meer de gen 1 Raichu pose, en de krullen bovenop het hoofd mogen iets natuurlijker naar beneden golven. Kleuren en staart verder prima, hoofd is een beetje knullig, snavel mag iets meer fearow achtig." Later: "schrap de fearow snavel" · "ik wil meer een vliegende achteroverleunende pose zoals het origineel" · "de krullen zijn wel eindelijk goed".
- Over r7: "uitstekend, maar het is geen sprite". Over r9: "kan je hier iets mee?"

## Aandachtspunten
- Dunne delen: kuifslierten en staartkoord als 1 px zwarte lijnen die vloeiend lopen (geen trapjes/onderbrekingen), krulletje aan de kuif leesbaar. Bliksem met zijn vorm en omlijning.
- Oog: het modeloog (rond, donker, glans) leesbaar op 64 px; wang rood eronder/erachter.
- Vleugelstippen: alle stippen van het model op hun plek, elk ≥ 2 px.
- Verre vleugel (achter de kop links) en poten met tenen zoals het model.
- Kleur mag naar Gen 3 (contrast, licht linksboven), vorm niet. Huidig palet ter vergelijking: `af/normal.pal`.
- Max 16 kleuren incl. transparant (index 0).

## Oplevering per ronde
`sprite_v2/rN/picaraio.png` (indexed 64×64) + `normal.pal` + `vel.png` (rN | rN-1 | model verkleind op 8×, close-up kop op 12× naast het model, 1× op licht en donker) + `picaraio_8x.png`. Commit niet; rapporteer kort.
