# Pitahaya-draak fase 3, sprite r10 (maker): Jordi op r9

- **Basis:** `../sprite_r9/pitahaya3_r9.png` (= `../af/pitahaya_draak_fase3.png`). Palet gelijk; in B wordt de ongebruikte dubbele zwart-index 13 (`q`) het teju-grijs (155,154,159).
- **Script:** `python3 maak_r10.py` schrijft `pitahaya3_r10_A.png`, `pitahaya3_r10_B.png` en `pitahaya3_r10_afwijkingen.txt` (elke pixel met assert op de oude kleur). `python3 vel.py <tijdelijke map>` maakt `vel.png`.
- **Vel:** A | B | r9 | model op 8×; close-ups 12× van knots + been (r10 | r9 | model) en kop (A | B | r9 | model); 1× en 2× op licht en donker naast Salamence, Tyranitar, Sceptile.

## Controle
- A: 18 px t.o.v. r9, B: 22 px. A en B verschillen alleen in de bek (6 px, x 8-11, y 26-29).
- Silhouet: alfa-diff 0 t.o.v. r9 (geen pixel geweken). Kop buiten de bekbinnenkant en buikzone pixelgelijk (asserts).
- ≤ 16 kleuren incl. transparant (index 0).

## Per punt
| punt | px | wat |
|---|---|---|
| 1 schutblad rechtsboven de knots | 7 | Gemeten in het model: één spits licht blad met de **punt omhoog** op x 27 (y 51-53), links een donkere lijn tegen het roze, rechts het donkere verre been tot de buitenlijn, eronder de roze lob. In r9 stond het blad omgekeerd (brede lichte voet bovenaan, direct tegen het been), daardoor liepen blad en been in elkaar over. Nu: (27,51) H, (27,52) H, (27,53) h; (26,51-52) g en (26,53) d links; (28,51-52) g rechts; (27,54) r. |
| 1 onderkant been | 2 | (22,50) h→g en (22,51) G→r: de beenonderkant is nu één doorlopende donkere lijn tegen de knots, geen groene brug meer tussen been en knots. |
| 3 verre achterbeen | 9 | Midden x 21-25 (y 46-49) naar G; g alleen nog als sikkel rechts (x 26-28) en als onderlijn tegen de knots. Daarmee h-G-g zoals de verre arm, maar met minder h en meer g: één tintstap terug in plaats van twee. |
| 2A bek | 1 | Pitje op (9,29) (model heeft daar een pit). Zichtbaar nu 2 losse pitjes + (11,28) dat tegen de rand valt, dus 3 in totaal. Een vierde op (11,26) niet gedaan: dat gaf met (11,28) een stippellijn langs de rand. |
| 2B bek | 5 | Pitjes als r9. Bovenrij (y 26) in schaduw van de bovenkaak: x 8-10 w, x 11 q (donkerder grijs, achterin); (11,27) w. Zoals de teju: boven/achter grijs, voor wit. |

## Eerlijk oordeel
- Knots: op 8× en 2× is rechtsboven nu een licht spits blad tussen twee donkere lijnen, met het donkere been erboven/erachter. Op 1× blijft het een paar pixels; het leest als blad, niet meer als been.
- Bek: elke wit pixel in de bek raakt een rand (het vlak is 15 px), dus "niet tegen de rand" kan niet volledig. A leest als vruchtvlees met pitjes, maar de twee zichtbare pitjes staan onder elkaar (9,27)/(9,29). B leest meer als mondholte (diepte), het vlees zelf blijft met één pitje mager. Combinatie A+B kan ook (pitje (9,29) + grijze bovenrij).
- Schaduw, lijnen, kleuren (gemeten tegen Sceptile/Tyranitar/Salamence): zwart 13 % van de pixels (Salamence 13, Sceptile 18, Tyranitar 19), zwart binnenin 4 % (4-9 %), rand zwart 52 % (56-62 %): binnen de norm. Groen in 4 tinten met stappen ±35/43/69 helderheid (hooglicht H springt het verst, zoals bij Sceptile). Licht linksboven klopt over lijf, staart en ledematen. Restpunten die ik zie maar niet heb aangeraakt (bevroren of buiten de opdracht): de pitjes op de buik staan vrij regelmatig (buikzone, bevroren); de binnenlijnen tussen nabije arm en dij zijn zwart waar Sceptile vaker donkergroen gebruikt, maar het aandeel zit binnen de Gen 3-marge.
