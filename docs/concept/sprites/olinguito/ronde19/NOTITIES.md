# Olinguito ronde 19: één oog, kop en snuit als één vorm, kleiner

Vertrekpunt ronde 18 (kop = ronde 16, staart = ronde 17). Jordi: "De meeste sprites hebben maar 1 oog in beeld ... het hoofd is wat te groot, misschien de hele sprite wel." En over ronde 18: "Je schuift het neusje op, maar laat het stuk hoofd dat de snuit/neus moet voorstellen intact. Prutswerk." Daarom is de kop deze keer als geheel opnieuw getekend (schedel, snuit, neus, kaak), met het masker, de oren, het oog en de grijns van ronde 16 als stijl.

## Studie (`studie.png`, frame 1, kopkader rood)
| sprite | oppervlak | kop | wat er met het verre oog gebeurt |
|---|---|---|---|
| Poochyena | 989 | 402 (41 %), 24×23 incl. oren | weg achter de neusbrug; neus x10, oog x17–20 = 7 px achter de neuspunt, 2 rijen erboven; oor recht boven het oog |
| Cyndaquil | 903 | 334 (37 %) | weg; spitse snuit, oog(spleet) 9 px achter de neuspunt |
| Typhlosion | 1941 | – | weg; snuit wijst schuin naar links-onder, verre kant van de snuit valt weg |
| Dragonair | 1176 | – | weg; kop klein t.o.v. lijf |
| Kabutops | 1321 | – | één oog, kop half van opzij |
| Rhyhorn | 1375 | – | weg achter de lange snuit + hoorn |
| Rhydon | 1947 | – | weg; snuit 3/4 |
| olinguito r18 | 1118 | 481 (43 %), 31×21 | twee ogen naast een korte snuit |
| **olinguito r19** | **994** (frame 2: 1006) | **355 (36 %), 25×18** | **weg achter de crème neusbrug** |

Conclusie: bij een snuitdier in 3/4 is de snuit één vorm die schuin naar links(-onder) wijst; de neuspunt is het meest linkse punt, het nabije oog zit 7–9 px daarachter, het oor er recht boven en het verre oog valt weg achter de neusbrug. Fase-1-koppen zijn 35–41 % van het oppervlak, het totaal ±900–990 px.

## Wat er veranderde
- **Kop (`bron/kop19.txt`, 26×18, met de hand in een tekstraster):** ronde schedel, verre oor klein links, nabije oor groter rechts met crème binnenkant (ronde 16). Eén amandeloog (`eec1e/dd11d/ddd`, zwart bovenlid, glans: letterlijk ronde 16), crème wenkbrauwboogje erboven. Masker: band over het oog met de vleugel naar het oor en de golvende onderrand; aan de verre kant alleen een randje langs de crème neusbrug. Snuit: brug x2→x1→x0 schuin naar links-onder, neus (zwart, met glanspixel) aan het eind, crème tussen neus en masker (les §28). Grijns: mondlijn onder de neus die naar achteren omhoog in het masker loopt, met tandje; kin rondt af naar de borst.
- **Lijf:** ronde 18, met de nek opnieuw ingevuld tussen kop en schouder, en kolom 40–41 (romp, dij, verre achterpoot) eruit geknipt: −2 px lengte. Voorpoten, klauwen, achterpoten en staart (hangende J) zijn verder pixel voor pixel ronde 18.
- **Frame 2:** zelfde beweging als ronde 18: kop, voorpoten en klauwen 1 rij omhoog, achterpoten stil, staart uit ronde 18 frame 2 (`bron/frame2.py`).
- **Palet** byte voor byte gelijk aan ronde 16–18.
- Bouwen: `cd bron && sh bouw.sh`; daarna `python3 vergelijk19.py` voor studie.png/compare.png. `maak.py` controleert open randen (0 in beide frames).

## §0-checklist (SPRITING.md)
1. 3/4 links-voor, lijf én blik: ok; de snuit wijst nu ook die kant op (was het probleem van r18).
2. Ledematen/oren/ogen: 4 poten, 2 oren, 1 oog (verre oog bewust weg achter de neusbrug), staart; alles verbonden. Verre achterpoot raakt na de knip de dij, maar met een omlijning ertussen.
3. Geen rechte lijnen: schedel en rug zijn trapjes 1-1-2…; resterend recht stuk: bovenlid (6 px, letterlijk ronde 16) en de bovenrand van het masker (5 px).
4. Ogen: één oog in ronde 16-stijl (donker bovenlid, iris donkergoud boven/goud onder, glans); geen bril meer.
5. Silhouet 1×: leest als dezelfde marter/olinguito met kleinere kop (compare.png).
6. Formaat: 994 px, tussen Cyndaquil (903) en Poochyena (989); boven het doel 850–950 (zie "Wat nog niet klopt").
7. Pose: ongewijzigd t.o.v. ronde 18 (poten niet gelijk, gewicht naar voren).

## SPRITING.md §1–§8
1. Met de hand: kop als tekstraster getypt, nek/knip met losse pixelcorrecties (`fix.py`); geen vormfuncties of automatische shading.
2. Grof → glad per onderdeel: eerst schedel/oren, toen snuit en grijns, toen kin en nek, telkens op 12–14× bekeken.
3. Curven: schedel- en achterhoofdsrand 1 px per rij (x20→21→22→23→24); kin 1-2-1 naar de borst; geen spijkers.
4. Kleuren: geen nieuwe; palet ronde 16.
5. Licht linksboven: hooglicht (5) op voorhoofd links en schouder, schaduw (3) rechts achter het hoofd en als slagschaduw onder de kin.
6. Glans: witte glans in het oog, glanspixel op de neus; reflectie = gouden onderkant van de iris.
7. Vacht: geen extra textuur (zoals ronde 16).
8. Omlijning: bruin (2) boven/links, zwart (1) rechts/onder en rond neus/mond; 1 px; geen anti-aliasing aan de buitenkant; open randen 0.

## SPRITE_OPDRACHT.md §2
- Lijf en blik 3/4: ok. Eén oog, snuit als één vorm met de neus aan het eind: ok (kern van deze ronde).
- Alles geteld en verbonden, poten niet aan elkaar (omlijning tussen verre achterpoot en dij): ok.
- Pose niet stijf: ongewijzigd, ok. Lijf op skelet: lijf is dat van ronde 18 (Poochyena-skelet), alleen ingekort.
- Formaat fase 1: 994 px, kop 36 % (was 43 %): ok binnen de studie, net boven het opgegeven doel.
- Kenmerken op 1×: masker, oren, haakstaart lezen nog; de grijns is op 1× klein.
- Geen rechte lijnen: zie §0.3. Ogen geïntegreerd: ok. Omlijning per kleurgroep, licht linksboven, geen open randen: ok.
- Kleur vs. Dark-types: palet ongewijzigd (eerder goedgekeurd).
- Goedgekeurde delen: oog, oren, maskerstijl, grijnsstijl en palet uit ronde 16 overgenomen; de kopconstructie zelf moest volgens de opdracht opnieuw. Lijf/poten/staart pixel voor pixel ronde 18 behalve de knip en de nek.
- Met de hand, geen automatische vormen: ok.

## Wat nog niet klopt (eerlijk, na 1× en 3× naast ronde 18 en Poochyena)
- **Uitdrukking:** met één oog leest de blik zijdelingser en iets lodderiger/sluwer dan in ronde 18; het masker is nu één donkere vlek rond het oog in plaats van een band over twee ogen. Het is herkenbaar dezelfde olinguito, maar Jordi moet beoordelen of hij even schattig is.
- **Snuit:** kort (3 px voor het masker uit); leest als snuit, maar de neus is een zwart blokje van 3×3 dat op 1× vooral als "puntje" leest.
- **Grijns:** werkt op 3×, op 1× nauwelijks zichtbaar (was in r18 al klein).
- **Oppervlak 994** (frame 2: 1006): gelijk aan Poochyena, maar boven het doel 850–950. Verder krimpen kan met een tweede knip in de romp of een kortere staart; niet gedaan om de goedgekeurde staart en pose niet te raken.
- Onder de kin ligt een brede schaduwzone (rij 37–38) en een zwarte armlijn; op 3× wat zwaar.

## Lessen
- **Eén oog bij een snuitdier = de snuit herbouwen, niet het oog weghalen:** de snuitbrug moet schuin naar de neuspunt lopen (1 px per rij) en het verre oog zit achter die brug. Crème brug tussen neus en masker houdt de neus leesbaar.
- **Verkleinen zonder schalen:** een kop opnieuw typen in de gemeten verhouding (kop ±35–40 %) en het lijf inkorten door 1–2 kolommen te knippen waar romp en dij recht doorlopen; daarna alleen de knipnaad repareren (omlijning dij/achterpoot).
- **Frame 2 per pixel afleiden uit de beweging van de vorige ronde** (welke pixels schoven, welke bleven staan) en de verre achterpoot expliciet stil houden; anders ontstaan halve poten op de knipnaad.
- **Studie meten met kopkaders op 3×** (studie.png) geeft in één blik of een kop te groot is: 43 % → 36 %.
