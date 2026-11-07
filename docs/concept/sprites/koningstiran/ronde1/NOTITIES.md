# Sapa Inca – kleurronde 1 (maker)

Bestanden: `sapa_inca.png` (64×64, geïndexeerd, index 0 transparant), `sapa_inca.txt` (tekstraster `y x0 tekens` + palet), `bouw.py` (raster → PNG + controles, schrijft `dump.txt`), `vel.py` → `vel.png`, `kijk.py` (eigen kijkvel), `labels.py`/`labels.txt` (hulp: welk onderdeel van het 3D-poppetje op welke pixel ligt; alleen als kaart gebruikt).
Draaien vanuit de repo-root: `python3 docs/concept/sprites/koningstiran/ronde1/bouw.py` en `.../vel.py`.

## Game Freak-studie (8×, bovenste frame + normal.pal)
| | Honchkrow | Noctowl | Empoleon | Decidueye | Talonflame |
|---|---|---|---|---|---|
| Tinten per groep | blauw 4 (40/64→72/96/152 + licht), wit 3, rood 2 | bruin 4, crème 3, geel 2 | marine 3 + felblauw 3, wit 3, goud 3 | groen 4, bruin/crème 3, oranje 2 | rood 3, grijs 3, goud 2 |
| Selout lichtkant | lichtere blauwtint op de bovenrand van hoed en vleugel | bruin-oker, geen zwart bovenaan de "hoorns" | **felblauwe rand** om de donkere flippers aan de lichtkant | groene middentint | lichte grijstint op de bovenvleugel |
| Zwart | alleen onder-/rechtskant, poten | buitenkant schaduwzijde | onderkant flippers en lijf | onderkant cape | onderkant, klauwen |
| Donkere veren volume | brede banden middentint over de basis, kleine schaduwkern | – | grote vlakken; volume zit vooral in de lichte rand | lange pennen met tintstreep per pen | pennen met lichte voorrand |
| Oog op donkere kop | klein rood oog met witte glans in een wit vlak, zwart erboven | rode iris, zwart bovenlid, wit glans | klein, in het gele masker | gekleurd oog in een donkere kap | geel oog in zwart masker |
| Kuif/kroon | hoedrand: lichte bovenrand, zwarte onderrand | "hoorns": crème vlak, oker scheidingen, geen ruis | gouden kroon: 3 tinten, licht linksboven | – | – |

Overgenomen: grote rustige vlakken, scheidingen in de schaduwtint van de groep (niet zwart) in het lichte deel, zwart pas aan de schaduwkant, lichtere selout op donkere delen aan de lichtkant (Empoleon), klein oog = zwart bovenlid + glans + lichte tint tegenover de glans.

## Palet (15 + transparant)
K zwart · d/m/l zwartbruin (schaduw/basis/licht) · r/R/o oranjerood (schaduw = omlijningsbasis, basis, licht) · p/v lavendel · a/g/y goud (oker-omlijning, basis, licht; gedeeld door borst, oorschijf, poten) · b/w snavel blauwgrijs (w ook oogglans) · t roestbruin (staart). Rood gezicht deelt R/r met de kroon.

## Hoe de kroon is opgebouwd
Negen brede veren die uit de kopbasis waaieren (scheidingslijnen geconstrueerd op hoeken 20°…160°, met de hand ingekleurd): links lichte veren (o, scheiding R), midden R/o, rechts schaduw (r, scheiding K kort). Per veer één zwarte vlek van 2 px net binnen de rand en één stip halverwege (= rijen stippen langs de veren). Rand: lavendel v aan de lichtkant, p aan de schaduwkant, omlijning p linksboven en K rechts/onder, veerpunten met p-streepjes. Links hangt een kwastje (oranjerode steel, lavendel/zwarte punt); rechts alleen een puntje lavendel/zwart onder de elleboog en een stukje naast de vleugel.

## Pixeldiff (alpha) met `silhouet_v1_1x.png`
- Totaal 1560 px = silhouet 1560 px; **erbij 0, eraf 0**.
- Zone a (vleugel/kroonrand, x39–55 y17–23): **0 px** gewijzigd; gescheiden met omlijning: de kroonrand loopt daar door in lavendel p, de vleugel heeft een zwarte voorrand (K) ertegen.
- Zone b (standbeen/staart, x28–38 y53–62): **0 px** gewijzigd; opgelost met kleur: de 1-px "staartstrook" links van het standbeen (x29–30) is als dij/scheen ingekleurd, zodat de staart alleen rechts achter het been zichtbaar is, met een zwarte scheiding tussen been en staart. Achterteen + klauw rechts aan de voet (x32–34, y61–62).
- Buiten de zones: 0 px.

## §0-checklist en harde eisen
1. Lijf/blik 3/4 naar links: ok volgens het bevroren silhouet (lijf 44°, kop 76°); verre oog kleiner aan de linkerrand, snavel links van het midden.
2. Ledematen geteld: 2 vleugels (opgeheven nabije rechts, verre als cape links in de schaduwtint d met selout m), 2 poten met voeten en klauwen, staart, kop met 2 ogen, oorschijf, kroon met kwastje: ok.
3. Rechte lijnen: de onderrand van de kroon (y22) is ±10 px recht links en 7 px rechts van de kop; dat zit in het bevroren silhouet. Niet opgelost met kleur (zie zwakke punten).
4. Ogen geïntegreerd: zwart bovenlid, witte glans, warme okertint tegenover de glans, rood gezicht eromheen: technisch ok; leesbaarheid zie zwakke punten.
5. Silhouet op 1×: leest als vogel met een waaierkroon (zie vel).
6. Formaat: bevroren (1560 px; Gen 3-eindvormvogels 1033–1825).
7. Pose: contrapposto uit het silhouet; niet stijf.
- Omlijning per kleurgroep: kroon r/p aan de lichtkant, K aan de schaduwkant; borst a; snavel b; donkere delen l/m aan de lichtkant, K aan de schaduwkant. Licht linksboven.
- Open randen (script): 3 px: de linkerkant van de 2 px dunne linkerscheen (x24, y57–59) is g naast transparant = bewuste pseudo-omlijning (Dragonfly Cave: delen van 1–2 px niet omlijnen); met a erop leest de poot bruin in plaats van oranjegeel.
- Kleuren: 15 + transparant. Aandeel zwart 0,15 (binnen de band 0,10–0,25).
- Losse pixels: alleen bedoelde enkelingen (stippen, glans, oogtint, oorschijf, kwastpunt).

## Eerlijk: wat nog niet klopt
- **Gezicht te klein en druk op 1×**: de kop is maar 11×9 px onder een kroon van 40 px; op 1× lees je "rood masker + bleke snavelstreep", de ogen zijn net zichtbare puntjes. De snavel leest op 4× eerder als een verticale balk dan als haaksnavel (de haak is maar 1 px).
- **Blik kan streng/boos lezen**: de zwarte oogleden staan in één rij met de zwarte kroononderrand.
- **Opgeheven vleugel leest als donkere knots/arm**, nauwelijks als gesloten vleugelblad: de pennen-scheidingen in d zijn op 1× weg; geen kartelpunt die leest. Volume op het donkere lijf is vlakker dan bij Honchkrow/Empoleon (die hebben veel meer middentint en een lichte rand).
- **Borst is een vlakke gele ovaal** ("ei op een zwart lijf"); een poging tot veermarkeringen vormde een gezichtje en is teruggedraaid.
- **Kroon**: de zwarte stippen/vlekken zijn op 4× wat streperig (2-px vlekken als streepjes), de schaduwkant rechts heeft korte zwarte scheidingen die op 1× als ruis kunnen lezen; de rechte onderrand blijft zichtbaar.
- **Staart** leest nauwelijks (smalle roestbruine strook achter het standbeen); kwastje rechts is maar een puntje.
- Poten zijn 2 px dun (zoals het silhouet); de linkerscheen heeft een pseudo-omlijning.

Volgens SPRITE_NORM is elk punt hierboven een fail; dit is daarom **geen versie voor Jordi** maar een eerste kleurronde voor de coördinator.

## Lessen
- Een waaier met vlakke tintblokken (licht/basis/schaduw als sectoren) leest als paddenstoel/lieveheersbeestje; dezelfde kleuren in **radiale veren** (9 scheidingen uit de kopbasis, één vlek + één stip per veer) lezen meteen als veren.
- Twee korte markeringen naast elkaar plus een streepje eronder op een lichte ovaal = een gezichtje (pareidolie); textuur op een borst nooit in zo'n driehoek zetten.
- Een zwarte kroononderrand direct boven zwarte oogleden maakt één zwarte balk en een boze blik; laat een rij gezichtskleur tussen kroon en lid.
- `bouw.py | head` breekt de pijp vóór het opslaan: controleer de uitvoer via een bestand, niet met head.
