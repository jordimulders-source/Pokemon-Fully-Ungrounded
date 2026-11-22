# Pinsir-evolutie (Bug/Ground) frontsprite, ronde 4: kleurronde over de hele sprite + 3 oogvarianten

Jordi op r3: "ogen niet goed en beetje zelfde probleem als pitahaya fase 3 had" · "als in hele sprite blurry".

Bestanden: `pinsir_evo_r4_A.png`, `_B.png`, `_C.png` (64×64, geïndexeerd, index 0 transparant, 14 kleuren incl. transparant), `bouw.py`, `onderlijf.txt` (handmatige tinten onderlijf), `vel.png` (A | r3 | model op 8×; kop A/B/C op 12×; 1× naast Gen 3 Pinsir/Heracross/Scizor op wit en donker). Bouwen: `cd pinsir_evo && python3 sprite_r4/bouw.py`.

## Controle (script, `bouw.py` + `gereedschap/controle.py`)
- Silhouet-diff met r3: **0** (A, B en C). Buiten het ooggebied (x14–25, y26–28) zijn A, B en C pixelgelijk (diff 0).
- Zwarte posities: 17 px anders dan r3 buiten de ogen (zwarte streepjes in het lijf waar het model < 20 % lijn in de cel heeft → vulling; 1 px zwart tussen twee lichte vlakken → donkerste vultint; 1 lijnpixel tussen onderarmstrook en dij x41 y47 → tint 2). Zwart 27,0 % (r3 28,1 %).
- Tintvlekjes < 3 px: **63** (r3 153). Lichte kleur op de buitenrand: alleen de klauwpunten (y ≥ 53, zoals r3) en de kaakbovenrand in de kaakmiddentint (gekleurde selout).
- Pixels anders dan r3: ±495 (vrijwel alles vulling).

## Vultinten per kleurgroep: vóór (r3) en na (r4), helderheid = (R+G+B)/3, zwart = 15
| groep | r3 | stappen r3 | r4 | stappen r4 | donkerste vultint boven zwart r3 → r4 |
|---|---|---|---|---|---|
| lijf (pantser) | 43 / 69 / 99 / 135 | 26 / 30 / 36 | 61 / 95 / 131 / 175 (glans) | 34 / 36 / 44 | 28 → **46** |
| kaak | 51 / 82 / 115 | 31 / 33 | 57 / 91 / 135 | 34 / 44 | 36 → **42** |
| dekschild | 45 / 106 / 152 | 61 / 46 | 56 / 106 / 157 | 50 / 51 | 30 → **41** |
| oog/tand | 215 / 152 | | 221 / 144 | | |

Gen 3-referenties (gemeten uit `graphics/pokemon/*/anim_front.png`, vultinten donker → licht; donkerste vultint boven de lijnkleur):
- Pinsir bruin 68 / 106 / 136 / 169 (+208): stappen 38 / 30 / 33; 68 boven zwart (0).
- Heracross blauw 67 / 101 / 147 / 192: 34 / 46 / 45; 51 boven zwart (16).
- Scizor rood 59 / 80 / 107 / 149: 21 / 27 / 42; 43 boven zwart.
- Tyranitar groen 72 / 120 / 173 / 213: 48 / 53 / 40.
r4 zit nu in hetzelfde bereik (stappen 34–51, donkerste tint 41–46 boven zwart); r3 lag met de lijftint 2 maar 28 boven zwart, waardoor vlakken in de lijnen opgingen. Tintgebruik lijf r3 → r4: 2: 271 → 339, 3: 309 → 339, 4: 149 → 164, 5: 111 → 12 (glans alleen nog op de modelglans).

## Wat er gedaan is
1. **Palet gespreid** (tabel hierboven). Kleurfamilies gelijk aan het model (khaki/grijsbruin pantser, donker roodbruin kaak, okerbruin dekschild).
2. **Platen uit het model**: de zwarte modellijnen verdelen het lijf in platen; elke spritepixel krijgt zijn plaat (meerderheid in de cel) en de mediane modelhelderheid van die plaat: donkere plaat (romp, schenen, staart: tint 2 met 3 aan de rand linksboven), middenplaat (kopschild, rug, gezicht: 3 met 4 linksboven en 2 rechtsonder), lichte plaat (dij, knie, onderarmstrook, klauwen: 4 met glans 5 linksboven waar het model ≥ 75 is en 3 rechtsonder).
3. **Licht linksboven per vorm**: afstand tot de plaatrand in de richtingen linksboven en rechtsonder (stralen die stoppen op een lijn of een andere plaat).
4. **Verre ledematen één stap donkerder** (linkerarm, -hand, -knie, -been; links = ver, zoals het verre oog).
5. **Onderlijf met de hand** (`onderlijf.txt`, 74 regels): de automatische verdeling liet daar nog vlekken; per onderdeel naar het model (20× naast elkaar): onderarmstrook en dij licht met glans, knie licht, romp en schenen donker met lichte rand, verre arm/hand/knie op 3/4, klauwen licht aan de lichtkant, staart bovenband 3/4 en verder 2.
6. **Kaken en dekschild**: kaak 3 tinten met licht op de bovenkant en schaduw onder; dekschild houdt de modeltekening (vlek/midden/licht) met licht/schaduw per vorm erbovenop.
7. **Buitenrand**: lichte tinten op de rand → middentint (gekleurde selout), behalve klauwpunten.

## Ogen (x14–25, y26–28; buiten dit gebied A = B = C)
Model (40× bekeken): beide ogen onder de zwarte kopschildrand (y26), lichte spleet die naar binnen (naar de neus) zakt; de donkere pupil zit **aan de binnenkant onderaan** (inkeping tussen een klein en een groot licht stuk); zwarte wenkbrauwband erboven. Gen 3-Pinsir doet hetzelfde: wit, zwarte pupil binnen-onder, brauw die aan de binnenkant schuin naar beneden loopt.
- **A** (Pinsir Gen 3 overgenomen, onderste twee rijen van zijn oog): nabij rij 27 `K T T T`, rij 28 `K T K T t` (brauw zakt naar binnen, pupil binnen-onder); ver: rij 27 `T T K`, rij 28 `T K`.
- **B** (dichtst bij het model): nabij rij 27 `K K T T` (spleet hoger aan de buitenkant), rij 28 `T K T T` (klein stukje, pupil, groot stukje); ver: rij 27 `T T K`, rij 28 `K` (pupil onder de binnenhoek).
- **C** (groter wit, pupil tegen de brauwpunt): nabij brauw 4 breed (x22–25), rij 27 `K T T T`, rij 28 `K K T T`; verre oog gelijk aan A.

## Afwijkingen van het model (benoemd)
- Kleur: alles lichter en met meer contrast dan het (zeer donkere) model; de romp blijft wel de donkerste massa.
- Ogen: 2 rijen hoog i.p.v. ±1 modelrij, anders lezen ze op 64 px niet (zelfde reden als r2).
- 17 zwarte pixels weg/verplaatst (zie Controle); verder lijnposities = r3.
- Lijnpixel x41 y47 (tussen onderarmstrook en dij) is tint 2 i.p.v. lijf 3, zodat strook en dij los lezen.

## Zelf geziene zwakke punten
- **Onderlijf is nog druk** (minder dan r3: 63 vs 153 vlekjes, platen lezen beter), vooral rond de middelste hand en de verre voet (x20–38, y50–59): veel kleine zwarte lijnstukjes uit r3 die op modellijnen liggen. Verder opschonen = zwarte binnenlijnen inkorten, en dat raakt lijnposities.
- **Kopschild** is een groot egaal middenvlak met lichte rand linksboven; het model heeft daar een paar facetten (lichtere bovenkant, donkerdere voorrand). Leest netjes maar vlak.
- **Dekschild** houdt de gevlekte modeltekening; op 1× leest het als tekening, op 8× nog wat vlekkerig.
- Losse zwarte pixel (24, 56) aan de verre voet (uit r3).
Na 3 interne rondes gestopt; een verse keurder is nodig vóór Jordi.
