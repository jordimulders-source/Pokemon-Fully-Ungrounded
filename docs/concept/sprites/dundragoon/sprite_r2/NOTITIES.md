# Dundragoon frontsprite, ronde 2 (r1 + drie benoemde reparaties)

Bestanden: `dundragoon_r2.png` (64×64, geïndexeerd, index 0 transparant, 12 kleuren incl. transparant), `bouw.py` (kopie van r1 met de drie wijzigingen; schrijft dezelfde kale reductie als r1, die staat in `../sprite_r1/kaal.png`), `vel.png` (r2 8× | r1 8× | model 8× / close-ups 12× kop+oog+hoorns, vleugels, pootjes, boor naast het model / 1× op wit, crème, donker, zwart + model 1×).
Bouwen: `cd dundragoon && python3 sprite_r2/bouw.py`. Schaal, raster, palet en reductie ongewijzigd t.o.v. r1 (zie `../sprite_r1/NOTITIES.md`).

## Opdracht (coördinator)
1. Lijf-lichtband: geen streep/naad; hooglicht dat de rugbolling volgt (gebogen, smaller, alleen bovenaan de romp tussen kop en vleugels), of weg.
2. Oogring: hele ring middenblauw, alleen een donkere buitenrand; ooglijn ongewijzigd.
3. Boor: geen lichtband die de spiraallijnen kruist; per segment schaduw onder/links → midden → licht bovenop; lijnen op hun modelplek.

## Wat er veranderde (r2 t.o.v. r1: 109 px; silhouet-diff 0, buiten oog/lijf/boor 0 px)
- **Oog (29 px t.o.v. r1):** ringpixels blijven dezelfde modelpixels (≥ 45 % blauwe modeldekking); alle ringpixels middenblauw, daarna donkerblauw op elke ringpixel met een 4-buur buiten de ring (flood fill van buitenaf). Resultaat: overal 1 px donkere buitenrand + 1 px (links 2 px) middenblauw. Ooglijn (olijf + zwart) niet aangeraakt.
- **Lijf (48 px t.o.v. r1):** de rechte band (37 px) is weg. Nieuw hooglicht van 13 px: per rij 2–3 px links van de blauwe rugband, dus de bolling langs de modelrand volgend, rijen 20–26, smal aan de uiteinden: (27–28,20) (27–29,21) (28–29,22) (28–29,23) (28–29,24) (30,25) (30,26). Alleen op middengeel; het model is daar vlak middengeel (eigen kleurtoevoeging, geen vorm).
- **Boor (32 px t.o.v. r1):** de spiraallijnen staan op dezelfde plek (uit de natieve olijfclusters van het model). Vultinten nu per winding: t = dwars over de kegel (0 onder/links, 1 boven/rechts), u = langs de as binnen de winding (0 = lijn aan de lijfkant). Schaduw waar t < 0,36 of (u > 0,7 en t < 0,6), licht waar 0,52 ≤ t < 0,86 en u < 0,5, anders midden. In het model lopen de lijnen niet tot de rechterrand (de windingen hangen daar aan elkaar); om per winding te kunnen kleuren wordt elke lijn alleen bij het indelen virtueel verlengd tot de buitenlijn (niet getekend; die pixels nemen de tint van de winding erboven). Elke winding heeft nu een korte lichte streep net onder zijn lijn rechtsboven en schaduw links/onder; geen licht kruist een lijn.

## Afwijkingen t.o.v. de kale reductie: 227 px (`zones.py ../sprite_r1/kaal.png dundragoon_r2.png`)
kop+oog+hoorns 76, vleugels+hoorn rechts 34, lijf 64, pootjes 5, boor 48. Per stap: buitenlijn 73, ontkorrelen 77, losse zwarte pixel 1, oog 41, boor 45, lijfhooglicht 13. Pixels die niet uit het model komen (kleur, geen vorm): lijfhooglicht 13 px, boorlicht en -schaduw per winding; verder niets.

## Controle (`controle.py`)
64×64, P, transparency 0, 12 kleuren incl. transparant, ≤ 3 tinten per groep + lijn; geen lichte buitenrand; geen losse zwarte pixels; zwart 13,6 %. Kleine stukjes: licht (30,25) (staart van het rughooglicht, 2 px) en (53,44) (lichtstreep van de bovenste winding, 2 px); de rest zijn lijnen of modelplekken, zoals in r1.

## Resterende twijfels
- Het rughooglicht ligt vlak naast de blauwe rugband; op 1× leest het als glans op de bolling, maar het is klein (13 px). Zonder: het lijf is vlak middengeel zoals het model.
- Boor: in de derde winding staan 2 schaduwpixels midden in de winding (53–54,50) en (53,51), onder de lijn erboven (u > 0,7); dat is bedoeld als schaduw onder de draad, maar het kan als vlekje lezen. De punt (laatste winding) heeft geen licht (te smal).
