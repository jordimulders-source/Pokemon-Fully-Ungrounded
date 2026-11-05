# Nachtaap fase 2: kleursprite ronde 7 (kené dik, zoals het poppetje)

Basis is ronde 6. Alleen de rug is veranderd (zone x 15–47, y 25–41). Handen, voeten, oortjes, kop, maan, staart en ogen zijn bevroren.

Jordi over ronde 6: "de lijnen zijn sowieso te dun, een patroon zou altijd dikker moeten".

## Bewijs (`bron/diff_uitvoer.txt`, `bron/bouw_uitvoer.txt`)
- **Alpha-diff:** 0 (1459 px, zowel tegen de `.txt` als tegen de `.npy`).
- **Open randen:** 0.
- **Palet:** gelijk aan ronde 6.
- **Diff buiten de rugzone t.o.v. ronde 6:** 0. In de rugzone zijn 148 px gewijzigd: de meander weg, de banden erin, en de vacht rond de rugband.
- **Nagemeten tegen het poppetje** (onderlaag 4:1, lichte patroonpixels): 102 px. Ronde 7 heeft 139 kené-pixels, waarvan 58 op dezelfde plek. Het verschil komt doordat elke band nu 3 px dik is, waar het poppetje 2–3 px heeft. Het silhouet is ook ±1 px ruimer dan de onderlaag.
- **Geen restjes:** de oude kené en de meander zijn uit het raster geschrapt. De vacht eronder is weer de vachtlaag van ronde 1, dus er zijn geen 1-px-lijntjes of krassen meer. Losse pixels in de rugzone: 0.

## Patroon (zoals het poppetje)
De banden staan per rij met de hand in `bron/kene.py` (`ROWS`). De regels die het script maakt, staan in `bron/kene_regels.txt` en zijn aan `raster.txt` toegevoegd.

| Band | Waar | Opbouw |
|---|---|---|
| Rugband | van achter de kop (x 17–20, y 30–32) over de rug (x 20–30, y 27–29) | gaat over in band A |
| Band A | x 26–32 | eerst een trede naar rechts (y 30–33), dan recht omlaag (x 30–32 tot y 40) |
| Band B | van de rug (x 33–37, y 28–29) | een trede (x 35–38, y 30–32), dan recht omlaag (x 37–39 tot y 39) |
| Band C | op het achterlijf | kort: twee treden (x 42–46, y 34–39) |

- Elke band is 3 px dik en de treden zijn 2–3 px. Er zijn geen diagonale streepjes en geen 1-px-lijnen.
- Tussen de banden zit 2–5 px vacht.

## Kleur en volume
- De kern van de band is idx 6 (`m`), met een eigen schaduwrand aan de onder- en rechterkant in idx 5 (`l`).
- Aan de lichtkant (x ≤ 30) heeft de band een lichtere rand linksboven in `n`.
- In de lijfschaduw (achterlijf, band C) is de band helemaal `l`. Zo buigt hij mee met de bol en wordt hij naar achteren donkerder.
- Er is geen wit; de band is rustiger dan de maan.
- **Vacht rond de rugband:** het hooglicht wijkt daar naar de basistint (`b`). Anders liep de band op het hooglicht weg. De rugband is zelf nu het lichtste deel bovenop, en dat geeft het hooglicht van de bol.

## Eerlijk
- Het patroon is minder fel dan in het poppetje (daar wit-lila), omdat het rustiger moet zijn dan de maan. Op 1× leest het als drie lichte getrapte banden over de rug, niet als ruis.

## Lessen
- **Een patroon moet ≥ 3 px dik zijn om op 1× als patroon te lezen.** Lijnen van 1 px lezen als krassen, ook als de vorm klopt (Jordi: "een patroon zou altijd dikker moeten").
- **Een licht patroon op een hooglicht valt weg.** Laat het hooglicht rond het patroon wijken, of maak het patroon daar een tint lichter.
- **Bepaal de ondergrond voor de kleurregels uit het raster zonder de oude laag, niet uit de vorige PNG.** Anders bepalen de oude lijnen nog steeds de kleuren.
