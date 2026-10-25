# Keuring olinguito v2, kleur ronde 3

Gekeurd: `olinguito.png`. Maatstaven:
- het gekozen ontwerp (`../../referenties/ONTWERP_GEKOZEN.png`, ONTWERP.md, SPEC.md);
- het silhouet van ronde 5;
- SPRITE_NORM, SPRITE_OPDRACHT §2, FAKEMON_CHECKLIST (viervoeter), SPRITING §0–§8 en FAKEMON_DESIGN.

Vergeleken met 11 echte sprites, telkens het eerste frame met `normal.pal`, op 1× en 4×, op licht en op donker: Linoone, Zigzagoon, Poochyena, Mightyena, Sentret, Furret, Rattata, Raticate, Sneasel, Meowth en Aipom.

Het vergelijkingsplaatje is `keuring_vgl.png`. Het toont:
- de sprite op 4× op licht en op donker;
- het ontwerp, Linoone en Zigzagoon;
- uitsneden van de kop en van de poten;
- alle 12 sprites op 1×.

Coördinaten staan als (x,y) op het 64×64-raster.

## Metingen
| | olinguito r3 | referenties |
|---|---|---|
| oppervlak | 1174 px | Zigzagoon 1127, Linoone 1089, Poochyena 989, Sentret 982 |
| kleuren (zonder index 0) | 15 | 11–15 |
| aandeel zeer donker | 0,20 | 0,14–0,19 (Mightyena 0,48) |
| gemiddelde helderheid | **72** | 88–147 (alleen Mightyena is even donker: 74) |
| alpha-diff met silhouet r5 | **0** | – |

## Hoofdvraag
**Herken je het ontwerp?** Ja. Je ziet de pose, de lange staart in een krul, het zwarte masker met het rode oog, het ene oor en de lichte klauwen linksonder.

**Leest hij als een echte Gen 3-sprite?** Nog niet, om twee redenen:
- **De kop leest als een helm met vizier.** Het masker is een dikke, rechte, horizontale balk. Daarboven ligt een lichte wig met een rechte diagonale naad naar de bruine kruin, en achteraan zit een rechte verticale donkere band.
- **De voorpoten lezen als één plank met een zwarte streep erin.**

Naast de referenties is hij ook de donkerste en vlakste sprite. Er is weinig hooglicht (R/S gebruikt juist veel hooglicht, SPRITING §5).

## SPRITE_NORM: harde eisen
| # | Eis | Oordeel | Zone en reden | Minimale reparatie |
|---|---|---|---|---|
| 1 | Leest op 1× als een Pokémon | **FAIL** | De kop leest als helm/vizier, de voorpoten als één plank (zie 3 en 5). | Zie de reparaties A–C. |
| 2 | 3/4 links-voor; lange snuit, dus één oog | PASS | Eén oog, de neus is het meest linkse punt van de kop, het lijf staat schuin. | – |
| 3 | Alle ledematen tellen op 1× | **FAIL** | De verre voorpoot is maar 1 px kleur (`b`) tussen twee zwarte lijnen (x 26–28, y 42–48: `KbK`). Op 1× zie je die als een zwarte streep in de nabije poot. Je telt 3 poten. | Reparatie B. |
| 4 | Geen Escher | PASS | De overlap klopt: de nabije poten liggen over de verre. | – |
| 5 | Geen rechte lijnen ≥ 4 px waar het dier rond is (kleurwerk) | **FAIL** | Zie de opsomming onder deze tabel. Het silhouet zelf toets ik niet (bevroren). | Reparaties A, C en D. |
| 6 | Kop 40–55% van de hoogte | PASS | y 17–41 van 4–59: 45%. | – |
| 7 | Ogen geïntegreerd | PASS | Het oog is 3×2 (x 20–22, y 32–33): glans linksboven, donkerrood erboven en ernaast, lichter rood midden-onder, en het masker als donker bovenlid. Het leest op 1× als een klein rood oog. | – |
| 8 | Kenmerken op 1× leesbaar | **FAIL** | Masker en staart lezen goed. **De klauwen niet**: het zijn twee rechte, evenwijdige stokjes (1-op-1-diagonaal, y 53–58) en ze lezen als een vork of eetstokjes, niet als Linoone-haken. | Reparatie C. |
| 9 | Omlijning: selout, licht linksboven, geen open randen | **FAIL** | De selout is goed (`b`/`s` aan de lichte kant, zwart aan de schaduwkant) en het licht komt van linksboven. Er zijn wel **open randen**, zie de opsomming onder deze tabel. | Reparatie E. |
| 10 | Geen "Chernobyl" | PASS | Geen misvorming en geen zwevende delen. Wel twee verdwaalde pixels, zie de technische toets. | – |

**Rechte lijnen in het kleurwerk (eis 5):**
- Bovenrand van het masker: twee horizontale stukken van 8 px (y 31, de bruine `s`-lijn van x 10–17) en 7 px (y 30, x 18–24).
- Naad tussen grijs en de bruine kruin: een 1-op-1-diagonaal over 10 rijen (y 20–29).
- Verticale band `ddd` (x 25–27, y 28–38) en `bb` (x 27–28, y 22–29).
- Lichte strook op de dij: een 1-op-1-diagonaal van gelijke breedte (y 35–39).
- Klauwen: rechte 1-op-1-stokjes.

**Open randen (eis 9):**
- Onderkant van de snoet: `d` naast transparant op (19–21,39).
- Binnenkant van de staartkrul: `m` op (49–50,7).
- Bovenkant van het oor en de kruin: `G` op (24,18) en `m` op (18,18).
- Voorkant van de achterpoot: `l` op (38,46).
- Klauwen: `W` op (17,53) en `w` op (17–18,58).

## Kleurwerk zoals Game Freak
| Punt | Oordeel | Toelichting |
|---|---|---|
| Aantal tinten | PASS | Per groep 3 tinten: lijf `l/m/b`, kop `G/g/d`, roze `P/p`, klauw `W/w`, oog `r/R`. Daarbij komen selout `s` en zwart. **Wel een verspild slot:** maskerzwart `k` (36,23,18) en omlijning `K` (26,15,11) zijn op 1× niet te onderscheiden. |
| Selout | PASS | Op lijf, staart en kop zit de selout in de basistint aan de lichte kant en zwart aan de schaduwkant. Fout is alleen het bruine `s`-lijntje binnenin, boven het masker (zie Gezicht). |
| Geen kussenshading | PASS | Het licht komt consequent van linksboven, de schaduw zit rechtsonder. |
| Volume | **FAIL** | Het lijf is goed. **De kop is gefacetteerd** (een lichte wig, een vlak grijs veld en een donkere achterband, gescheiden door rechte naden) en leest daardoor als een harde schaal in plaats van een bolle schedel. De lichte strook op de dij leest als een streep, niet als een ronde dij. |
| Geen ruis | PASS | Bijna schoon. Twee verdwaalde pixels: zie de technische toets. |
| Palet past bij Dark | PASS (zie ook "voor Jordi") | Donkerbruin met een zwart masker en een rood oog werkt voor Dark. Het lijf en de grijze kop hebben bijna dezelfde helderheid (`m` 78 tegen `g` 89), dus de kop scheidt zich alleen door tint en masker van het lijf. |

## Gezicht
| Punt | Oordeel | Zone | Minimale reparatie |
|---|---|---|---|
| Oog en masker | **FAIL** | Het masker (y 30–35) is 5–6 rijen dik: ±22% van de kophoogte, tegen ±3 px in het ontwerp. Het loopt kaarsrecht horizontaal en eindigt achter het oog in een rechte verticale rand (x 24). In het ontwerp volgt de band de kop: hij is smaller, loopt licht schuin omhoog naar achteren en heeft een ronde kop om het oog. Het bruine `s`-lijntje (y 31, x 10–17) maakt er een vizierrand van. | Reparatie A. |
| Schattig én sinister | **FAIL** | Sinister ja: het rode oog in de zwarte band. Schattig nauwelijks: de ronde kop en de zachte snoet uit het ontwerp zijn verdwenen achter de helmvorm. | Komt mee met reparatie A. |
| Kop als eigen onderdeel, niet als helm | **FAIL** | Zie volume en masker. Daarbij leest de voorkant van het gezicht (x 7–8, y 32–39) als een plat vizier, omdat de snoet donker is (`d`) zonder lichte bovenrand. | Reparatie A. |
| Oor | PASS | Het dominante oor heeft een donkere `s`-rand en een lichte `G`-binnenkant. Het verre oor is een klein bultje. Klopt met de SPEC. |
| Neus en mond | PASS | De oudroze neus zit vooraan (x 8–9, y 36–38) met een mondlijntje `KK` (x 9–10, y 38). |

## Poten en klauwen (viervoeter, FAKEMON_CHECKLIST)
| # | Oordeel | Toelichting |
|---|---|---|
| C1 alles geteld | **FAIL** | Op 1× lees je 3 poten. De verre voorpoot leest als een streep. |
| C2 4 kolommen, 3–4 voethoogtes | **FAIL** | Voethoogtes zijn er 4 (y 52, 50, 48, 51). Maar de twee voorpoten delen één kolom, zonder lucht en zonder omlijningsbasis ertussen. |
| C3 / C5 aanhechting | PASS | – |
| C4 gewrichten | voor Jordi | De nabije voorpoot is een rechte 1-op-1-plank zonder elleboog. Dat komt uit het bevroren silhouet. |
| C6 nabij ≠ ver | PASS (achter), FAIL (voor) | De verre achterpoot staat goed in de schaduwtint. De verre voorpoot is te smal om te lezen. |
| E1 verre kant donkerder | PASS | – |
| E2 overlap in omlijningsbasis, niet zwart | **FAIL** | De nabije en verre voorpoot zijn gescheiden door twee zwarte lijnen (`KbK`). Juist dat maakt de plank met de zwarte streep. |
| Klauwen: twee, licht, Linoone, aan elkaar vast | **FAIL** | Ze zitten aan elkaar vast (één gedeelde `K`-lijn). Maar het zijn twee even dikke rechte stokjes, wit (`WW`) met maar één `w` per rij en zonder ronding. Ze lezen als een vork of eetstokjes. Linoone heeft korte, gebogen haken met een schaduwkant. |

## Technisch
| Punt | Oordeel | Toelichting |
|---|---|---|
| 16 kleuren | PASS | Er zijn 16 slots en alle 15 kleuren worden gebruikt. |
| Index 0 transparant | PASS | `transparency=0`. Index 0 is (152,208,160) en komt niet in de figuur voor. |
| Alpha-diff met het silhouet | PASS | 0 px. |
| Open randen | **FAIL** | 11 px, zie eis 9. |
| Losse pixels | **FAIL** (klein) | `s` op (25,30) los tussen het masker en `ddd`, en `K` op (24,37) als een inkeping bij de kaak. De overige geïsoleerde pixels zijn bedoeld: glans, neushooglicht en de staartkrul. |
| Rechte lijnen in curven | **FAIL** | Zie eis 5. |

## Voor Jordi (smaak, geen afkeur)
- **Oppervlak 1174 px** ligt boven de norm voor fase 1 (700–950). Het silhouet is door Jordi bevroren; Zigzagoon is met 1127 px vergelijkbaar groot.
- **Helderheid:** gemiddeld 72, net zo donker als Mightyena en donkerder dan alle andere referenties. Past dat bij "een goede donkerbruine tint"? Een iets lichtere `l` (meer hooglicht volgens de R/S-stijl) maakt hem minder modderig zonder dat hij minder Dark wordt.
- **De nabije voorpoot is een rechte plank** zonder elleboog. Dat zit in het silhouet en is met kleur alleen beperkt op te lossen.
- **Snoetkleur:** de SPEC zegt "donker grijsbruin". In het ontwerp heeft de snoet een iets lichtere bovenkant. Hier is hij donkerder dan de rest van de kop, waardoor het gezicht terugwijkt.

## Oordeel: **NIET GOED**

Het silhouet is exact gevolgd en het lijf en de staart zijn netjes. Maar de kop leest als een helm, de voorpoten als één plank en de klauwen als eetstokjes. Op 1× is dat precies Jordi's kritiek: "niet zoals pokemon sprites".

## Reparatielijst (op prioriteit; alleen binnen het bevroren silhouet, alpha-diff 0)
1. **A. Kop en masker (±60–80 px).**
   - Masker terug naar ±3–4 rijen. Laat de band licht schuin omhoog naar achteren lopen, met ronde boven- en onderranden zonder rechte stukken > 3 px.
   - Rond de band achter het oog af tot een ronde oogvlek, in plaats van de rechte rand op x 24.
   - Haal het bruine `s`-lijntje boven het masker weg (y 31, x 10–17); vervang het door `g`.
   - Vervang de rechte naad tussen grijs en kruin door een boog die de schedel volgt.
   - Laat de lichte `G` als klein hooglicht linksboven op de schedel staan, niet als wig.
   - Vervang de verticale banden `ddd` (x 25–27) en `bb` (x 27–28) door een gebogen schaduwgrens op de "evenaar" van de kop.
   - Geef de snoet één rij `g` aan de bovenkant, direct onder het masker, zodat hij naar voren komt.
2. **B. Verre voorpoot (±25–40 px).**
   - Vervang de dubbele zwarte scheiding `KbK` door: nabije poot `bllm` + één scheidingslijn `b` (omlijningsbasis, E2) + verre poot 2 px (`m` en `b`) met `K` aan de buitenkant.
   - Het doel: op 1× tel je twee voorpoten, de verre in de schaduwtint.
3. **C. Klauwen (±10–15 px).**
   - Geef elke klauw `W` aan de bovenkant en `w` aan de onderkant (schaduwkant), en laat de gedeelde scheidingslijn 1 px meebuigen, zodat de punten haken worden.
   - De twee klauwen blijven aan elkaar vast.
4. **D. Dij (±8 px).** Breek de 1-op-1-strook licht op de dij in een gebogen hooglicht dat breder is bovenaan en smaller uitloopt, zoals de dij van Linoone of Raticate.
5. **E. Open randen (11 px).** Geef de omlijning `K` of `b` op (19–21,39), (49–50,7), (24,18), (18,18), (38,46), (17,53) en (17–18,58).
6. **F. Losse pixels (2 px).** (25,30) wordt `d` en (24,37) wordt `d` of `b`.
7. **Optioneel:** maak van `k` een maskertint die zichtbaar van `K` verschilt (bijv. ±(52,36,30)), zodat het masker op 1× niet met de omlijning versmelt.

Na de reparatie: vergelijk opnieuw op 1× naast Zigzagoon en Linoone. Je moet twee voorpoten tellen, een bolle kop zien met een band eroverheen (geen vizier) en twee haakjes als klauwen.
