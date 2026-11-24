# Eindkeuring Dragonfly Cave: Bibarel-evolutie `sprite_r13` → `sprite_r14` (24 nov)

Alleen de uitvoering gekeurd, geen herontwerp. Vorm, silhouet en onderdelen zijn bevroren (tanden, ogen, neus, potlood, staartvorm, tuinbroekvorm, klep). Gewijzigd zijn alleen lijnpixels en tinten. Het silhouet is alleen onder de staart aangepast (punt 4). Palet ongewijzigd (15 kleuren + transparant).
Jordi: "top, stuur maar naar de eindkeuring, let op lijnen, schaduwconsistentie, kleurtinten. Ook dat de bollen om het hoofd heen goed gelijnd zijn. Verder onder de staart een paar onnodige pixels".

## Gids, letterlijk (`docs/lessen/bronnen/dragonflycave_spriting_guide.txt`)
- r. 96–97: "The "outline shadows" are always black (or ever-so-slightly off-black) on Pokémon sprites".
- r. 112–113 (regel 3): "The outline base and outline highlight colors are also colors. When you're recoloring, you must also recolor the outlines."
- r. 117 (regel 4): "The outlines must be reasonably dark."
- r. 106–107 (regel 1): "the relative luminosity of the shades on the original sprite should always be maintained on the new one."
- r. 421–423: "we take the base outlining shade for every color and color all of the outline except the shadows in that color, and remove the clusters so that the outline is always one pixel wide."
- r. 427: "lighter pixels on the inside of the outline are a far better idea".
- r. 443–444: "the wing "shadow color" is really used where the front wing overlaps the back wing".
- r. 452–456: "Put some of the shadow/outline highlight color on the outlines in the very most highlighted parts [...] place pixels of the outline highlight color on the inside of the outline rather than the outside."
- r. 406: "It has a consistent light source and the shading is reasonably placed."

## Meting r13 (`meet.py`)
- Buitenrand schaduwkant: 91/91 zwart. Lichtkant: eigen tinten (b 39, e 24, g 12, D 10). De basis klopt.
- Om en om op de buitenrand: helmtop (33,6)K–(34,7)b–(35,7)K, staartboven (58,20)K–(59,21)g–(60,21)K. Kleppunt (19–20,12–13): dambord b/c, met lichte c op de buitenrand.
- Lijnklont 2×2 zwart: (42–43,23–24) tussen kraagbol en schouder.
- Zwarte binnenlijnen in de kraag: onderlijnen van de kraagbollen (20–22,29), (24,31), (25–28,32), (29,31). Officiële Bibarel: de onderlijnen van de vachtpluk over het lijf zijn donkerbruin, niet zwart. Voorbeeld uit een eerder gesprek: Gnomad, snor-onderlijn → eigen tint.
- Kraagbollen: links is de rand tegen de hand b-c-b-c (om en om); onder heeft de bol rechts van het midden geen onderlijn (het model heeft er wel een); rechts zijn de bollen één vlak zonder naden, met log-tint e en bijna-zwart (35,14), (20,15) als lijn.
- Tuinbroek linkerbuitenrand: b b b b D D D b (twee lijntinten op één rand). D (L145) is ook te licht voor een buitenlijn (regel 4).
- Onder de staart: zwevende zwarte pixel (54,49), nopje in de heuplijn (53,50) (staat niet in het model), staartstompje (52–53,46–47).
- Tinten: bruin f/d/c + b met stappen van 37/37/38 (goed). Crème C/M/S + D met stappen van 26/26/36 (iets onder ±30, niet aangepast, zie hieronder). Donker L/e + K (35/31). Oranje o/g. Geen banding of pillow shading.
- Schaduw: licht linksboven klopt op helm, klep, armen, tuinbroek (C links → M → S rechts), dijen, staart en log. Uitzondering: de bollen rechts van de snuit (één vlak d).

## Reparaties (56 px, `sprite_r14/bouw.py`; diff buiten de zones = 0, met assert bewezen)
| Zone | px | Wat |
|---|---|---|
| A staartonderkant (punt 4) | 7 | Zwevende pixel en heupnopje weg. Stompje weg: de staart sluit met een zwarte onderlijn op y46. Enige silhouetwijziging: (52,47), (53,47), (53,50), (54,49). |
| B helm en klep | 6 | Helmtop zwart vanaf x33. Kleppunt helemaal b (geen dambord, geen lichte buitenrand). Klep-onderlijn doorlopend b ((35,14) e→b, (38,15) c→b, (20,15) e→b). |
| C kraagbollen links | 7 | Rand bol/hand overal b. (21,21) D→e (snuitlijn), (21,22) D→d (bolvulling). |
| D kraagbollen onder | 17 | Zwarte onderlijnen → b. De bol onder rechts krijgt een onderlijn als boog (31,31)→(32–35,32)→(35,31)→(36,30), zoals in het model. (35,30) b→c voorkomt een lijnklont. |
| E kraagbollen rechts | 15 | Naad bol rechtsboven (39,16), (40,17), (40,18) sluit op de bestaande lijn. Naad tussen de middelste en de rechter bol (40,20), (40,21), (39,22). Schaduwsikkel aan de rechterkant van de middelste bol (3× d→c). Onderlijn e→b. 2×2-zwartklont → één lijn van 1 px (44,22)–(43,23)–(42,24). |
| F tuinbroek linkerrand | 3 | D→b. De buitenrand is nu één tint, donker genoeg. |
| G staart boven | 1 | (59,21) g→K. Geen om-en-om meer. |

Na r14: schaduwkant 92/92 zwart, lichtkant alleen eigen tinten (b 43, e 24, g 11, D 7 op het potlood). Geen om-en-om meer behalve (17,15) in de donkere hand (e/K, niet te zien). Geen 2×2-zwartklonten. Zwarte binnenpixels alleen nog in ogen, mond/tanden, vingers, logdetail en de lijf/staart-grens (schaduwkant van het lijf, net als bij Ursaring). Silhouet en tanden, ogen, neus, potlood en tuinbroekvorm zijn ongewijzigd.

## Oordeel: PASS na de reparaties (r14)
Op 8× (`vergelijk_gen3_8x.png`) en op 1× (licht en donker, onderaan `sprite_r14/vel.png`) leest hij naast Bibarel, Ursaring, Swampert, Linoone en Furret als Gen 3. Elke kraagbol heeft nu een eigen bruine omtrek, ook rechts. Onder de staart staat niets los meer.

## Ter info voor Jordi (niet gewijzigd)
- Crème-stappen C→M→S zijn 26/26 (Taillow ±30–40). Bijstellen kan alleen via het palet, en dat raakt ook de oogband en het potlood. Daarom niet gedaan.
- De potlood-bovenrand is D (L145), lichter dan een Gen 3-crèmelijn (Linoone ±L80–110). Het potlood is bevroren ("uitstekend"), dus niet aangeraakt.
- De zakrand heeft twee tinten: boven D, zijkanten S. Dit is goedgekeurd in r12/r13.

## Bestanden
- `meet.py`: meting r13/r14 en `kop_model_r13_r14.png` (model geprojecteerd op het spriteraster | r13 | r14, 16×).
- `vergelijk_gen3_8x.png`: r14 naast Bibarel, Linoone, Ursaring, Swampert en Furret.
- `../sprite_r14/`: `sprite.png`, `sprite_8x.png`, `vel.png` (r14 | r13 | model 8×; kop 12× met de gewijzigde pixels gemarkeerd; staartonderkant 12×; Gen 3; 1× licht/donker) en `bouw.py`.
