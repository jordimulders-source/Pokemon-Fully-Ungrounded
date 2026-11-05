# Eindkeuring kolibrie pre-evo, kleur r10 (verse, onafhankelijke keurder, 5 nov)

Gekeurd: `kolibrie_pre.png` (64×64, P-modus, 15 kleuren + transparant, 606 px, box x12–45 × y13–45).
Vel: `eindkeuring_vel.png` (r10 | r10 + voorgestelde reparatie | eindvorm | Taillow, Starly, Fletchling, Natu, Pidgey, Pichu; 3× en 1×, licht en donker).
Werkwijze: eerst zelf gekeurd (raster, palet, vel); pas daarna SPEC.md/NOTITIES.md gelezen om vaste besluiten van Jordi niet als FAIL te tellen.

## 1. Blinde eerste indruk
- **4×:** een klein, zittend zangvogeltje (jong/uitvlieger) in lila, kop schuin omhoog, snaveltje open met gele mondhoek: bedelt. Leest direct als een vogel en als nette Gen 3-sprite (Starly/Natu-school). Vleugel is een donkerder blauwviolette plaat, staartstompje rechtsonder, twee pootjes.
- **1×:** leest als "klein lila vogeltje dat piept"; bek, oog, vleugel en buik zijn te onderscheiden. Naast Taillow/Fletchling/Natu is hij wel het **vlakst**: alle echte sprites hebben een sterk kleuraccent (rode keel, oranje kop, groen/rood); hier is het accent alleen 11 px oranje/geel. Geen fout, wel het zwakste punt op 1× (zie Voor Jordi).

## 2. Vergelijking met echte sprites
| | px | box (x × y) | onderkant y |
|---|---|---|---|
| **kolibrie_pre r10** | **606** | 34 × 33 | **45** |
| Natu | 431 | 30 × 28 | 46 |
| Fletchling | 606 | 34 × 39 | 50 |
| Pichu | 565 | 26 × 37 | 49 |
| Starly | 767 | 34 × 39 | 51 |
| Taillow | 838 | 40 × 36 | 52 |
Formaat past bij een kleine eerste fase (Natu/Fletchling). Hij staat **4–6 px hoger** in het frame dan de referenties; dat is een kwestie van de y-offset in de soortdata (of de sprite 4 px omlaag schuiven bij de inbouw), geen pixel-FAIL.

## 3. Kleur
**Palet (15 gebruikte indexen):**
| idx | RGB | L | hue | sat | gebruik |
|---|---|---|---|---|---|
| 1 | 20,14,30 | 16 | 262 | 53 | omlijning schaduwkant |
| 2 | 66,48,98 | 55 | 262 | 51 | omlijningsbasis / selout lichtkant |
| 3 | 108,90,156 | 99 | 256 | 42 | lijf schaduw |
| 4 | 150,134,200 | 142 | 255 | 33 | lijf basis |
| 5 | 186,176,224 | 182 | 252 | 21 | lijf licht / buikschaduw |
| 6 | 224,220,244 | 223 | 250 | 10 | buik |
| 7 | 255,255,255 | 255 | – | 0 | glans buik + oog |
| 10 / 14 | 62,52,128 / 66,56,126 | 60 / 63 | 248 | 57 | vleugel schaduw / achterkop |
| 8 / 11 | 96,82,170 / 102,90,172 | 91 / 98 | 250 | 50 | vleugel / kruin |
| 12,13,9,15 | geel → bruin | 210–70 | 47→24 | 71–82 | mondhoek, pootjes |

- **Helderheidsstappen** hoofdramp 1→7: 39, 44, 43, 40, 41, 32: gelijkmatig, ±40 per stap. Taillow (blauw 42/72/106, dan wit) ±30–34; Starly 25–38. Contrast is dus **gelijk aan of iets ruimer dan** de maatstaf: PASS.
- **Hue shifting:** 262 (schaduw) → 250 (licht), schaduwen iets roder/paarser, lichten iets blauwer; 12°. Klein, maar Taillow (220–229) en Starly (vrijwel 0) shiften ook nauwelijks; verzadiging daalt netjes met de helderheid (53 → 10). PASS.
- **Leesbaarheid 1×:** PASS op licht en donker; de lichte borst draagt het silhouet, de vleugel leest door de blauwere, verzadigder plaat.
- **Mild t.o.v. de eindvorm:** eindvorm hue 242–269, sat 34–61, fluweelzwarte kop, teal accent; pre-evo sat 10–53, lichter, geen teal, oranje gaap/pootjes. Herkenbaar dezelfde violetfamilie, duidelijk milder en jonger: PASS (past bij "mild lila").
- **Paletzuinigheid (opmerking, geen FAIL):** 10/14 (ΔL 3) en 8/11 (ΔL 7) zijn vrijwel gelijk; effectief 13 kleuren. Alleen nuttig als kruin en vleugel bij de shiny apart moeten kunnen; anders kunnen ze samen en komen er 2 slots vrij.
- **Omlijning donker-aandeel:** 0,67 van de randpixels bijna-zwart (Taillow 0,62, Starly 0,75): PASS.

## 4. Dragonfly Cave-eisen, één voor één
| Eis | Oordeel | Toelichting |
|---|---|---|
| Omlijning 1 px, geen klonten | PASS | overal 1 px; geen zwarte klonten. |
| Selout (omlijning per kleurgroep) | PASS | lichtkant (kop voor, borst, buik links) in 2, schaduwkant (rug, vleugel, onderkant) in 1; vleugel/lijf intern gescheiden met 2/3. |
| Lichtbron linksboven | PASS | kop, borst en glans linksboven; vleugel en onderkant rechtsonder donker; slagschaduw van de kop op de hals (3). |
| Pillow shading | PASS | buik loopt links door tot de omlijning, schaduw alleen rechts/onder. |
| **Banding** | **FAIL** | onderbuik y37–41: banden 5 en 4 lopen als twee even brede trappetjes exact parallel aan de diagonale onderrand (5-grens x26→25→23, 4-grens x28→28→27→27→26). Op 3× zichtbaar als strepen. |
| Jaggies (omtrek) | PASS | rug en borst gladde curven; staartrand 2-2-3-2 is acceptabel. |
| Anti-aliasing | PASS | alleen binnen de omlijning; geen gekleurde puntjes buiten (0 lichte randpixels naast transparant). |
| Dithering | PASS | geen. |
| Clusters/ruis | PASS (1 kanttekening) | wezen alleen in oog, bek en pootjes, daar functioneel; zie pootje hieronder. |
| Open randen | PASS | 0 (elke randpixel is 1 of 2). |
| Losse pixels | PASS | geen zwevende delen; (12,15) snaveltip hangt diagonaal aan (13,16). |
| Volume | PASS | borst bol met glans, hals hol (vast besluit), vleugel als plaat over het lijf. |
| Oog | PASS (vast besluit) | Starly-oog S, zie Voor Jordi. |
| Snavel | PASS (vast besluit) | open naaldbekje met gele gaap; zie Voor Jordi. |
| Vleugel | PASS | eigen tintgroep, licht linksboven, sikkelschaduw rechtsonder, tip steekt onder het lijf uit en is gesloten. |
| **Pootjes** | **FAIL (1 px)** | vorm/perspectief goed (vast besluit), maar het lichtste geel (C) zit op (26,44), de **onderste**, van het licht afgekeerde teenpixel; licht hoort boven op het pootje (zoals Taillow/Starly). |
| Hooglicht hoeveelheid (R/S-stijl) | PASS | veel lichte tint (6: 110 px), kleine witte glans. |
| Overshading | PASS | per groep 3 tinten + omlijning; oranje 4 tinten op 11 px is net te veel maar onschuldig. |

## 5. FAILs en reparaties (8 px, alleen binnen de onderbuik en het nabije pootje)
1. **Banding onderbuik** (7 px): laat de 6 iets verder omlaag lopen en zet de 4 als smalle, onregelmatige overgang, zodat de banden niet meer parallel lopen:
   - (26,37) 5→6 · (25,38) 5→6 · (24,39) 5→6
   - (26,39) 5→4 · (25,40) 5→4 · (26,40) 5→4
   - (25,41) 5→3
2. **Pootje licht** (1 px): (26,44) 12 (C) → 13 (D).

Getest in het vel (kolom "r10+fix"): omtrek, oog, bek, hals en pootvorm blijven pixel voor pixel gelijk; de onderbuik leest ronder. Alpha-diff 0.

## Voor Jordi (smaak/ontwerp, niet als FAIL geteld)
- **Oog:** binnenin 2 lichte pixels (7 op (23,19), 5 op (23,20)) in een zwarte ring van 3×4. Op 3× leest het als een hol ringetje, niet als Starly's donkere kraal met één glanspunt. Als je het donkerder wilt: (23,20) 5→1 (1 px). Vast besluit, dus alleen ter overweging.
- **Bovensnavel:** (13,16) én (14,16) én (14,17) gevuld geven een klein haakje (dubbele pixel) in de 1-px-lijn; (14,16) → 0 maakt hem strakker. Snavelvorm is vastgesteld, dus alleen als je het wilt.
- **1×-accent:** naast Taillow/Fletchling/Natu is dit de vlakste sprite (alleen lila + 11 px oranje). Mild lila is besloten; een iets sterker accent (bijv. iets meer gele gaap) zou hem op 1× meer laten "poppen".
- **Paletdubbelingen** 10/14 en 8/11: samenvoegen als ze niet nodig zijn voor de shiny.
- **Plaatsing:** onderkant op y45, referenties op y46–52: y-offset in de data instellen.

## Eindoordeel: **TERUG** (2 kleine FAILs, 8 px)
Na de 8 pixels hierboven: GOED. Kleur, contrast, omlijning en lichtbron zijn op Gen 3-niveau en vergelijkbaar met Taillow/Starly.
