# Eindkeuring kolibrie pre-evo, kleur r6 (variant S)

Keurder: vers en onafhankelijk (5 nov). Eerst zelf geoordeeld op de pixels; NOTITIES.md en SPEC.md pas daarna gelezen.
Bestand: `kolibrie_pre_S.png` (605 px, box 34×33, 15 kleuren + transparant).
Vel: `eindkeuring_vel.png` (r6 S, mijn voorstel R1–R8, voorstel + R9, naast Taillow/Starly/Pidove; 5× en 1×, licht en donker).
Coördinaten zijn (x,y) in het 64×64-vlak. Indexen: 1 zwart, 2 donkerlila (omlijning), 3/4/5 lila, 5/6/7 buik, 8/A vleugel, B/E kap, 9/D/C oranje, F grijs.

## 1. Blinde eerste indruk
- **1×:** een klein, zacht lila zangvogeltje dat zit en schuin omhoog naar links kijkt. Het leest als Pokémon, maar zachter en fletser dan elke vogel ernaast. Het open bekje leest op 1× **niet** als snavel, eerder als twee sprietjes of snorharen voor het gezicht.
- **4×:** ronde borst, een donkere vleugelplaat, een staartje en twee oranje stipjes als pootjes. De onderkant en de staart ogen zwaar en donker; de vleugelrand is een harde, overal even donkere lijn.

## 2. Vergelijking met echte sprites
Bekeken op licht en donker: taillow, starly, fletchling, pidgey, swablu, wingull, natu, zigzagoon, pichu, chikorita, pidove, spearow, hoothoot, torchic, rufflet, pikipek, rookidee.
- **Formaat:** 605 px, gelijk aan Fletchling (606) en Torchic (602), tussen Pikipek (520) en Taillow (838). PASS.
- **Omlijning bij de referenties:** Taillow en Starly hebben een gesloten zwarte buitenlijn die nergens dikker wordt dan 1 px; aan de lichtkant (Pidove, Swablu) een donkere tint van het vlak. Binnenlijnen (vleugel Taillow, Pidove) volgen één vorm, zijn op het belichte stuk lichter of dunner en lopen dood in de buitenlijn. Bij geen enkele referentie wisselen 1 en 2 elkaar pixel om pixel af op dezelfde rand.
- **Snavels:** bij alle referenties een gevuld vormpje met omlijning (Pidove open: roze binnenkant). Een snavel van alleen haarlijnen komt bij Gen 3 niet voor.
- **Contrast:** alle referenties hebben een veel grotere helderheidsspreiding; dit is de bewuste keuze voor mild lila (geen FAIL), zie "Voor Jordi".

## 3. Belijning in detail (de vraag van de eigenaar)
**Wat goed is:** de buitenlijn is overal 1 px; geen gaten; links/boven (lichtkant) donkerlila `2`, rechts en onder zwart `1`, met de overgang linksonder op (22,38)→(22,39); de borstcurve links (x16…25, rij 22–43) loopt netjes; de kin-inham (21,28) met de getrapte tint `5` op (21–22,27),(22,28) is een geslaagde, tapse "kop over borst"-lijn; de bovenrand van de vleugel (35–38,27) → (33–34,28) → x32/x31 loopt als nette curve (4-2-v2-v3).

| # | Plek | Bevinding | Oordeel |
|---|---|---|---|
| L1 | rug/schaduwkant, (31,22)→(39,27) | buitenlijn wisselt kleur: 1,**2**,1,**2,2**,1,1,**2**,1 op (31,22),(32,23),(33,23),(34,24),(35,24),(36,24),(37,25),(38,26),(39,26). Aan de schaduwkant hoort één kleur zwart; dit is precies de "willekeurige streep". Daarnaast trap 2-3-**1**-2 (jaggie op (37,25)); alleen met alpha te repareren, en het silhouet is bevroren. | FAIL |
| L2 | kruin (26,14) | losse `2` in een zwarte rand: (25,13)=1, (26,14)=2, (27,14)=1. | FAIL |
| L3 | staart (42–44, 37–40) | `2` twee kolommen breed tegen de zwarte rand: 1+2+2 = 3 px donker. Leest als dikke klont lijn, niet als schaduw. | FAIL |
| L4 | onderkant (32–37, 40–42) | de vleugelvoorrand loopt onderaan uit in een blok `2` van 3×5 (rij 40–42) boven de zwarte rand op rij 43: 3 px donker, "niet mooi afgewerkt". | FAIL |
| L5 | snavel (15,17),(15,20) | lichtgrijs `F` op de buitenrand (raakt transparant): anti-aliasing aan de buitenkant, geeft op elke achtergrond een los grijs puntje; daardoor wisselen de snavellijnen 1/2/F/2 en lezen ze als losse streepjes. Ligt in de bevroren snavelzone (x≤20, y13–22); alleen een indexwissel, de vorm blijft. | FAIL |
| L6 | vleugelvoorrand x31–32, rij 29–35 | binnenlijn overal in omlijningskleur `2` (luma 59) direct tegen de lichte flank: niet taps, niet in een tint van het vlak; dit is wat de eigenaar "te hard" noemde. | FAIL |
| – | kop linksboven (22–24,13)→(18,15) | trap 4-3-1-1 (de 2 ontbreekt); klein, alleen met alpha te repareren. | opmerking |
| – | vleugelpunt (38–40,42–43) | vlakke onderkant van 3 px met haakse hoeken; silhouet bevroren. | opmerking |

## 4. Overige punten
| Punt | Bevinding | Oordeel |
|---|---|---|
| Banding | kap: `E` loopt als 1–2 px band evenwijdig aan de buitenlijn van (29,17) tot (30,22), met daarnaast `3` en `4`: strepen 4│3│E│1 op de achterkop. | FAIL (K1) |
| Pillow shading | licht linksboven, donker rechtsonder, buik onderaan lichter aan de lichtkant: consistent. | PASS |
| Clusters/losse pixels | vleugel: `A` (35,34–35) met `8` (36,34–35) ernaast vormen twee strepen van 1 px in de dekveren (rommelig op 4×, onzichtbaar op 1×). | FAIL (K2) |
| Pootjes | lichtste oranje `C` onderaan (28,44), donkerder `D` erboven (28,43): licht van onderen. | FAIL (K3) |
| Open randen | alleen L5 (F aan de rand). | zie L5 |
| Contrast op 1× | leest, maar zacht (bewuste lila-keuze). | PASS, zie Jordi |
| Volume | borst bol, kop rond, nekschaduw `3` scheidt kop en rug. | PASS |
| Oog | ontwerpbesluit (Starly-oog zonder iris); niet gekeurd. | n.v.t. |
| Palet | 16 indexen, groepen ≤ 3 tinten + lijn; `F` alleen voor de 2 foute pixels van L5 (vrije slot na R7). | PASS |

## 5. Reparaties (alleen indexwissels; alpha-diff 0, 36 px in totaal)
Getest in het vel (`voorstel R1–R8` = 31 px, `+ R9` = 36 px).
- **R1 (L1):** (32,23)→1, (34,24)→1, (35,24)→1, (38,26)→1. Rug aan de schaduwkant één zwarte lijn.
- **R2 (L2):** (26,14)→1.
- **R3 (L3):** (43,37), (42,38), (43,38), (42,39), (43,39), (42,40), (43,40), (44,40) → 3. Staart = één vlak `3` met een 1-px zwarte rand.
- **R4 (L4):** (32,41), (33,41), (34,41), (35,41), (32,42), (33,42), (34,42), (35,42), (35,40) → 3. De vleugellijn eindigt dan taps in (36–37,40),(36,41) en loopt dood in de buitenlijn (36–37,42).
- **R5 (K2):** (35,34), (35,35), (35,36) → 8. Eén rustige grens 8/A (x38,38,38,37,37,36,36,36,35).
- **R6 (K1):** (29,17), (29,18) → B. De kapschaduw wordt een wig die pas op rij 19 begint in plaats van een band.
- **R7 (L5, bevroren zone: Claude moet akkoord geven):** (15,17)→2, (15,20)→2.
- **R8 (K3):** (28,43)→C, (28,44)→D.
- **R9 (L6):** (32,30), (31,31), (31,32), (31,33), (32,34) → 3. De lijn is donker waar de vleugel onder de rug steekt (rij 27–29) en in de schaduw onderaan, en lichter op het belichte stuk (het selout-principe uit de gids). Op het vel leest de vleugel nog als eigen plaat; wil de eigenaar meer scheiding, dan R9 overslaan.

## Voor Jordi (smaak/ontwerp, geen FAIL)
- **Snavel:** de vorm is jouw besluit, maar op 1× lezen de twee haarlijntjes als snorharen/sprietjes ("willekeurig geplaatste zwarte strepen"). Geen enkele Gen 3-vogel heeft een snavel van alleen lijnen; een vulling van 1 px in snavelkleur (`D`/`9`) langs de kaken zou hem als snavel laten lezen, met dezelfde vorm.
- **Contrast:** mild lila blijft op 1× flets naast Taillow/Starly; een iets donkerder `3` of zwarter `2` zou helpen, maar dat raakt de kleurkeuze.
- **Pootjes** (2×2 en 2×1) lezen op 1× als twee oranje stipjes, niet als tenen.
- **Silhouet (bevroren):** jaggie in de rug op (37,25), trap 4-3-1-1 linksboven op de kop, haakse vleugelpunt onderaan. Alleen oplosbaar met een alpha-wijziging van 2–4 px.

## Eindoordeel: **TERUG**
9 FAILs, waarvan 6 belijning (L1–L6). Alle reparaties zijn klein (36 px, alleen indexen, geen alpha) en staan hierboven met coördinaten. Na R1–R9 verwacht ik een nette, Gen 3-achtige afwerking; de leesbaarheid van de snavel blijft een ontwerpvraag.
