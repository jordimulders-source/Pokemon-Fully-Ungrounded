# Gloom (onderwater-Oddish-lijn, Water/Fire) frontsprite, ronde 1 (kandidaat)

Bestanden: `gloom_r1.png` (64×64, geïndexeerd, index 0 transparant, 15 kleuren incl. transparant), `kaal.png` (kale reductie), `vel.png` (r1 8× | model op dezelfde schaal 8× / close-ups 12× mond+kwijl, lavabrok, kelp links, kelp rechts naast het model / 1× op licht, crème, donker, zwart + model 1×), `bouw.py`.
Gereedschap (`../gereedschap/`): `pitch.py` (rastermeting), `natief.py` (natief raster), `klassen.py`, `gemeen.py` (schaal, palet, overlap), `vel.py`, `raster.py` (spriteraster over het model, voor plekmetingen), `controle.py` (Gen 3-metingen), `zones.py` (afwijkingen per zone).
Bouwen: `cd gloom_sprite && python3 r1/bouw.py` (standaard TG 0,25, TK 0,30, TD 0,18).

## Metingen
- **Rasterpitch:** randsterkte per kolom/rij gaf een kam op 13,65 én 6,83 met gelijke score; beide fases van 13,65 scoorden hoog → echte cel = **6,83 px** (1024/150), visueel bevestigd (modellijnen ±6,8 px dik). Verfijnd: pitch x 6,826 fase 5,85, y 6,824 fase 6,00. Natief raster 149×149, figuur x21–126, y20–121 (**106×102**, 6891 px).
- **Schaal: 42/102 = 0,412** (2,43 natieve px per spritepixel). Figuur in de sprite **x9–51, y11–52 (43×42), 1177 px** (game-Gloom: x7–54, y12–52, 48×41, 1118 px). Onderkant op y52 zoals de game-Gloom; horizontaal gecentreerd op dezelfde plek (midden x±30,5). Verhoudingen van het model ongewijzigd (hoger dan de game-Gloom, dus smaller).

## Wat uit het model komt (kale reductie, `kaal.png`)
Oppervlakteweging per spritepixel over het natieve raster:
- achtergrond als < ½ pixel figuur;
- **mondzone (x18–34, y32–41):** dunne donkere modellijnen (zwart + donker bordeaux, L < 55) winnen vanaf 18 % oppervlak ("donkerste wint", ijskomeet-regel): zo blijven de ovale mondring, de zwarte bovenlijn van de opening en de lipring op hun modelplek;
- **gloed wint** vanaf 25 % oppervlak (kieren, kwijl, kelpranden), daarna zwart vanaf 30 %;
- anders de groep (steen/lijf/kelp) met het grootste oppervlak, tint naar de gemiddelde modelhelderheid (steen 39/65/105 → drempels 52/74; lijf 70/103 → 88, lichtroze waar ≥ 35 % lichte modelpixels; gloed 128/162; kelp 88/126).
Ogen (twee schuine streepjes, 4 en 5 px), mond, kwijl met druppel, lavabrok met kieren en facetten, kelp links (1 punt) en rechts (2 punten), vinnetjes en de lichte vlekjes onderaan het lijf komen allemaal uit deze reductie. Niet gespiegeld (model frontaal; kelp links 1 verbrande punt, rechts 2, zoals het model).

## Pixels die afwijken van de kale reductie: 161 px
Per zone: **lavabrok 52, lijf+ogen+vinnen 57, kelp links 22, kelp rechts 24, mond+kwijl 6.** Per stap:
- kieren één tint (40 px, lavabrok/kelpranden): alle gloed buiten de mond → fel oranje (244,124,48); kieren waren 3 tinten door elkaar (diep/oranje/geel), nu één lijn zonder korrel. Mond en kwijl houden hun 3 gemeten gloedtinten.
- buitenlijn (74 px): geen open of lichte rand; steen altijd zwart; lijf/kelp zwart aan de schaduwkant (achtergrond rechts/onder), gekleurde selout (donker bordeaux / kelpbruin) aan de lichtkant. Gloedranden van de kelppunten blijven oranje (model: oranje rand om de houtskoolpunt).
- ontkorrelen (29 px): tintvlekjes < 3 px (hooglicht < 2) → buurtint van dezelfde groep.
- kelp: rood/steen in kelp (6 px): roodbruine verschroeide stukjes in de kelp → kelpbruin; roodoranje kierrandjes in de steen → kier.
- losse zwarte pixels (4 px) en losse tintpixels (5 px): steenmiddentint zonder steenbuur → zwart, 1 px lijfrood tussen mondring en gloed → ringlijn, losse diepe gloedpixel aan de kwijlrand → oranje.
- **hooglicht (5 px, kleur, géén vorm):** (19,27) (20,27) (21,27) (19,28) (20,28) middenrood → lichtroze. Het model is daar vlak middenrood; Gen 3 vraagt een hooglicht op de bolling (licht linksboven). Enige pixels die niet uit het model komen.

## Palet (index: kleur)
0 transparant (152,208,160) · 1 zwart (16,12,12) · steen 2 (44,42,44) 3 (74,72,74) 4 (116,114,110) · lijf 5 selout (88,28,40) 6 schaduw (128,48,64) 7 midden (166,76,88) 8 licht (198,108,116) · gloed 9 diep (204,74,40) 10 oranje (244,124,48) 11 geel (252,184,80) · kelp 12 bruin/selout (78,62,40) 13 olijf (116,100,70) 14 khaki (160,148,110).
Gloedkleuren = modelkleuren (gemeten 183,67,45 / 240,117,58 / 248,155,71–249,199,108), niet donkerder. Steentonen = modeltonen iets opgetild (stappen ±30–40 tegen zwart, zodat de brok facetten houdt tegen de zwarte buitenlijn).

## Controle (`controle.py`)
- 15 kleuren incl. transparant; index 0 transparant; per groep ≤ 3 tinten + lijn/selout.
- Geen lichte kleur op de buitenrand; geen losse zwarte pixels.
- Zwart 18,6 % van de figuur (bovenkant van Gen 3; het model heeft zwarte naden in de brok en tussen de kelpstrengen).
- Tintvlekjes < 3 px die over zijn: houtskool in de kelppunten (4×, modelplekken), lichtgrijze glans op de brok (1), lijnpixels van de mondring/vinnen (selout/schaduw, lijnen), glans geel in het kwijl (2), lip rechts en vin (lichtroze, 1 px glans), kelpstrenglijntjes (bruin/olijf, lijnen tussen strengen).

## Resterende twijfels (eerlijk)
- **Oranje op de buitenrand van de kelppunten:** het model heeft daar een oranje gloedrand met een dunne dieprode buitenste lijn; op deze maat is dat 1 px, en ik hield hem fel oranje (Jordi: fel, niet donkerder). Strikt genomen is dat een niet-zwarte, middenlichte buitenrand; alternatief = dieprood (204,74,40) aan de onder/rechterkant.
- **Kieren:** fel oranje en 1 px breed lezen sterker dan in het model (daar oranje met donkerrode randjes). Bewust (Fire leesbaar), maar de brok is daardoor drukker.
- **Hooglicht** (5 px) is een eigen kleurtoevoeging; zonder is het bovenlijf vlak middenrood zoals het model.
- **Kelp rechts:** de strengen staan op 1–2 px van elkaar; bovenste verbrande punt is 2 px hoog en leest op 1× als donker puntje met oranje.
- Linkervinnetje leest wat donker (selout boven + schaduw onder, alleen 2 px lichtroze).
