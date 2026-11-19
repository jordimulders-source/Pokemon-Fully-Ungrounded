# Opdracht kleur-/schaduwronde Palpaca (19 nov)

## Jordi (letterlijk)
- "dat de kop hoekig leest moet je oplossen met kleurgebruik en schaduwen"
- Over r2: "het schaduwwerk over de hele sprite heen is nog niet zo goed he, het is teveel zoals het model"
- Eerder: "Het design moet zo blijven alleen de pose moet natuurlijker, de hoek moet natuurlijker, hij moet netter" · "hij moet een cute starter zijn"

## Wat vastligt (bevroren)
- **Silhouet en lijnen van `r2/palpaca.png`**: de buitenomtrek blijft pixel voor pixel. Pootstand, kop, oren, kraag, handschoenen, staart blijven op hun plek. Controleer met een diff op het alfakanaal: 0 px afwijking.
- Ontwerp en kleurzones: crème wol, rode handschoenen met kleurige manchet, kleurige kraag, rode oorkwastjes, roze oorbinnenkant, donkerder grijsbeige verre achterpoot.

## Wat moet veranderen: alleen kleur, schaduw en volume, naar Gen 3 (niet naar het model)
- Schaduw zoals Game Freak in Emerald: licht linksboven, grote rustige vlakken, sikkelschaduw die de ronde vormen volgt (onder de kin, onder de buik, achterkant van de bil, verre kant van kop en hals), duidelijke stappen tussen de tinten, hooglicht linksboven op kop, borst en rug. Geen modelschaduw overtrekken, geen vlekken of ruis.
- De kop moet rond en zacht lezen door kleur en schaduw (zelfde omtrek), en de kuif als wollige krullen (enkele duidelijke krulvormen in licht/schaduw, geen donkere wenkbrauwlijn).
- De wol op het lijf: wollig door een paar grotere krulvormen in de schaduwtinten, geen dambord.
- Selout: gekleurde omlijning aan de lichtkant (donkere tint van de vlakkleur), donker aan de schaduwkant. Verre poten donkerder dan nabije (diepte).
- Palet: je mag de tinten van het oude palet bijstellen of ramps aanpassen (≤16 kleuren incl. transparant), zolang de kleuren herkenbaar dezelfde blijven.

## Referenties
- Gen 3-sprites (`graphics/pokemon/<naam>/anim_front.png` + `normal.pal`): mareep, skitty, ponyta, torchic, flaaffy, wooloo bestaat niet in Gen 3, dus vooral mareep/skitty (zachte wol/vacht) en ponyta (lijf/poten in 3/4).
- `docs/lessen/SPRITE_KERN.md` (eerst lezen), `docs/lessen/SPRITING.md`, `docs/lessen/bronnen/` (Dragonfly Cave Spriting Guide: shading, selout, dithering), `docs/lessen/FAKEMON_CHECKLIST.md`.
- Model `../model/model.png` alleen voor wat waar zit, niet voor de schaduw.

## Werkwijze
- Werk in `r3/`: `palpaca.png` (64×64, geïndexeerd, index 0 transparant), `normal.pal`, scripts, `NOTITIES.md` (wat je per zone deed, alfa-diff met r2 = 0, zwakke punten), `vel.png` (r3 8× | r2 8× | Mareep en Skitty 8× | 1× op licht en donker | close-up kop 12×).
- `im.convert('RGBA')` op een geïndexeerde afbeelding negeert transparantie: eerst opslaan met `transparency=0`.
- Zelfgenoemd zwak punt eerst zelf repareren. Geen git commit/push.
