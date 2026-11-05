# Nachtaap fase 3: kleurronde 2 (5 nov): één lichtverdeling + handpalm

Jordi: "nu mag je eerst alle shading en kleur op het lichaam gaan fixen en er een geheel van maken" + "en de shading en kleur in de handpalm".

Basis: `../ronde1s/nachtaap_fase3.png` + `normal.pal` (palet **ongewijzigd**: 15 kleuren + transparant). Uitgelezen naar `bron/basis_1s.txt`.
Bron: `bron/ronde2.py` (met de hand geschreven rijpatches + één blok voor romp/schouder) → `bron/ronde2.txt` + `nachtaap_fase3.png`. Controle: `bron/check.py` (uitvoer `bron/check_uitvoer.txt`). Vel: `bron/vel.py` → `vel.png`.

## Bewijs
- **Alpha-diff 0** (geen pixel transparant ↔ gevuld).
- **Bevroren 0 px diff** (589 px): gezicht (schild, ogen, snuit, mond, zwart binnen het gezicht), maan (D/E/F), gloed (A/B/C), staart (kol ≥ 49 rij 22–41 en de staartwortel kol 45–48 rij 22–34; spiraalspleten zijn transparant en dus ook vast), voetzool onderbeen (7).
- **Handomtrek**: alle 1/2-pixels van de handrand ongewijzigd. De check meldt 2 "omtrek"-pixels omdat ze diagonaal aan de gloed raken: (13,48) vingertop D→F en (20,51) top vierde vinger D→E; dat zijn vulpixels, geen rand.
- **Open randen: 0** (geen 3/4/5/D/E/F naast transparant).
- **Losse pixels**: 26 vachtpixels zonder gelijke 4-buur; allemaal diagonale banden (pixellijnen die 1 px verspringen: arm, staart, voet) of origineel (staart/voet/pols), geen spikkels. Vier echte losse pixels opgeruimd: (19,32), (24,32), (28,33), (33,46).
- 276 pixels van index veranderd t.o.v. 1s, alleen binnen vacht/omlijning/palm.

## Wat ik per zone deed (licht overal linksboven)
- **Kop-vacht**: kruin als bol, lichtband 5 op de bovenkant (rij 28–31), 4 eronder, rechterring 3 met één rand (2 binnen, 1 buiten) in plaats van de dubbele 2-2-kolom; de binnenkant van de maansikkel rustig 4 met één schaduwpixel rechts (was 4-3-4-4-3-4 ruis).
- **Vuistarm**: onderarm licht aan de bovenkant (band 5 onder de bovenrand), schaduw 3 aan de onderkant; bovenarm (steiler) licht links/midden, schaduw rechts, zoals het model. Omlijning omgedraaid naar de regel: bovenrand van de onderarm 2 (lichtkant), onderkant 1; rechterrand bovenarm 1. Vuist zelf ongewijzigd.
- **Opgeheven been**: band 2-5-5-4-4-3-1 overal gelijk (twee rijen met een 4 na de rand rechtgezet); de dij-lichtband loopt bij de heup zonder naad over in de lichte rugbovenkant.
- **Romp**: één bol; groot licht vlak 5 linksboven (rug/schouder rij 30–32 en een rond vlak kol 30–37 rij 33–39), 4 eromheen, schaduw 3 rechts (naar de staartwortel) en onder (buik). Het oude lichte rechthoekje bij de dijwortel en de losse lichte kolom zijn weg.
- **Genezersarm**: cilinder, licht links (5), 4, schaduw 3 rechts; één binnenlijn 2 waar de arm vóór de romp ligt (was dubbel 3-3); onder de romp de dubbele rand 2-1 → 3-1.
- **Schouder**: vuistarm en genezersarm lopen zonder streep in elkaar over; alleen een zachte schaduwpixel onder de vuistarm.
- **Onderbeen**: dij licht aan de bovenkant (5) direct onder de buikschaduw (vorm vóór vorm zonder lijn), 4 midden, 3 onderkant; de brede 2-band onderaan (rij 51–53) en de dubbele randen aan de scheen zijn 3 geworden met één zwarte buitenrand. Knie en scheen-lichtband gehouden.
- **Staart**: niet aangeraakt (Jordi: "staart is hier goed"); hij had al licht boven/links.
- **Handpalm** (binnen de vaste omtrek): vingers als kleine cilinders: top licht (F op de toppen van de eerste drie vingers), linkerkolom D, rechterkolom + scheiding E (handschaduwtint, geen zwart, geen horizontale lijnen = geen rooster); vierde vinger aan de schaduwkant D/E. Palm: licht midden met F-hooglicht (rij 54–55), duim met lichte top (F), de duimmuis als lichte bolling begrensd door een gebogen E-lijn (11,55)→(12,56)→(13,57); schaduw E naar de pols (onderkant) en de schaduwkant (rechts). De oude donkere 2-stukjes tussen de vingertoppen en de 2-lijnen bij de duim zijn E geworden.

## §0 / norm
1. 3/4 links-voor: ongewijzigd (alleen kleur). ok
2. Ledematen geteld en verbonden: ongewijzigd. ok
3. Geen rechte lijnen: omtrek ongewijzigd. ok
4. Ogen: bevroren. ok
5. Silhouet: ongewijzigd. ok
6. Formaat: ongewijzigd (1861 px vulling, gelijk aan 1s). ok
7. Pose: ongewijzigd. ok
- Omlijning: zwart aan de schaduwkant, 2 aan de lichtkant, geen dubbele randen meer aan kop-rechts, genezersarm, onderbeen. ok
- Licht linksboven op alle delen. ok

## Zelf bekeken (1×, 3×, 4×, naast 1s, model en primeape/medicham/alakazam)
- Op 4× en 3× leest het dier nu als één lichaam met één lichtbron: lichte rug/kruin/linkerkanten, schaduw rechts en onder. Duidelijk ronder dan 1s, waar elk deel een eigen lichtverdeling had.
- Op 1× lezen de vier vingers als lichte richels; de palm blijft vooral een lichte hand (met 3 palmtinten D/E/F en een vaste omtrek is meer contrast tussen vingers niet mogelijk zonder zwart).
- Om naar te kijken (geen twijfel over de lichtrichting, wel smaak): de lichte streep van de genezersarm en het lichte rompvlak liggen naast elkaar, gescheiden door de binnenlijn; de onderkant van het onderbeen is een groot rustig 3-vlak.

## Lessen
- Maak bij een "één geheel"-ronde eerst een tabel van de buitenranden per deel (lichtkant 2 / schaduwkant 1): hier stonden bij de vuistarm de 1 en de 2 precies omgekeerd, en op drie plekken zat een dubbele rand (2-2 of 2-1) die als klont las.
- Een diagonale cilinder onder ±45° krijgt bij licht linksboven het licht op de bovenkant zolang hij vlakker is dan 45°, en links/midden zodra hij steiler wordt; laat de lichtband geleidelijk verschuiven (onderarm → bovenarm) in plaats van per deel te kiezen.
- Vingers van 2 px met alleen een lichte scheiding (E tussen D) verdwijnen op 1×; licht links + schaduw rechts per vinger (D|E E|D) leest wel, zonder zwart.
- Check "omtrek" met de 1/2-randpixels, niet met "raakt de gloed diagonaal": vingertoppen raken de gloed ook.
