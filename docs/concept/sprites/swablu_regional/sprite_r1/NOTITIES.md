# Onweerswolk-Swablu (Electric/Flying) frontsprite, ronde 1 (kandidaat)

Bestanden: `swablu_r1.png` (64×64, geïndexeerd, index 0 transparant, 16 kleuren incl. transparant), `kaal.png` (kale reductie), `vel.png` (r1 8× | kale reductie 8× | model op dezelfde schaal 8× / close-ups 12× kop+voelsprieten en staartje+wolk rechts, steeds sprite | model / 1× op licht, crème, donker, zwart + model 1×), `bouw.py`.
Gereedschap (`../gereedschap/`, overgenomen van Gloom en aangepast): `pitch.py` (rastermeting), `natief.py` (natief raster → `natief.png`), `klassen.py` (modelpixels indelen), `gemeen.py` (schaal, palet, overlap), `frac.py` (nieuw: per spritepixel de modelfracties per klasse, om elke reparatie op een gemeten plek te zetten), `vel.py`, `raster.py` (spriteraster over het model), `controle.py` (Gen 3-metingen), `zones.py` (afwijkingen per zone).
Bouwen: `cd swablu_regional && python3 gereedschap/natief.py && python3 sprite_r1/bouw.py`.

## Metingen
- **Rasterpitch:** kammen op 8,53 en 12,81 (verhouding 2:3) → gemeenschappelijke cel **4,27 px** (1024/240), visueel bevestigd op oog en snavelrand. Verfijnd: x 4,267 fase 3,25; y 4,270 fase 3,00. Natief raster 239×130; figuur x74–163, y24–104 (**90×81**, 4825 px). Achtergrond = bijna-wit dat met de rand verbonden is (snavelwit en oogglans liggen binnen de figuur en tellen mee).
- **Formaat:** game-Swablu (bovenste frame) x8–55, y17–49 (48×33), 785 px. Schaal **34/81 = 0,420** (zelfde hoogte-orde, oppervlak vergelijkbaar): figuur **x13–50, y16–49 (38×34), 864 px**. Onderkant op y49 zoals de game-Swablu, horizontaal rond hetzelfde midden. Verhoudingen van het model ongewijzigd; niet gespiegeld.

## Wat uit het model komt (kale reductie)
Oppervlakteweging per spritepixel over het natieve raster: achtergrond als < ½ pixel figuur; geel (vonken) wint vanaf 25 %; zwart wint vanaf 30 %, of vanaf 15 % als de pixel de "rug" van een dunne lijn is (meeste lijn dwars op de lijn; zo vallen 1-natieve-px-lijnen niet in stippels uiteen); wit (L ≥ 205) vanaf 30 % (in snavel/oog snavelwit of glans, elders het lichtste wolkwit); anders vogel of wolk naar het grootste oppervlak, tint = dichtstbijzijnde paletkleur van die groep bij de gemiddelde modelkleur.
Wolkbollen, onderwolk, vogellijf, vleugel achter het lijf, snavel (wit boven, grijze onderkaak, zwarte mondlijn en onderrand), vonken, sprieten, staartje en de zwarte inkepingen onder het lijf komen hieruit.

## Pixels die afwijken van de kale reductie: 113 px
Per zone: **voelsprieten+vonken 30, wolk links 22, vleugel+wolk rechts 25, kop+oog+snavel 19, onderwolk+staartje 17.** Per stap:
- ontkorrelen (46 px): tintvlekjes < 3 px → meest voorkomende buurtint van dezelfde groep (wolk/vogel; lijnen, geel, wit niet).
- buitenlijn (55 px): geen open of lichte rand. Achtergrond rechts/onder → zwart; lichtkant → selout: lichte wolk → wolk midden (109,121,137), donkere wolk → wolk selout (56,70,84), vogel → vogel donker.
- vonkrand (11 px): geen lichtgeel op de buitenrand; rechts/onder oker (zoals de okerrand in het model), links/boven geel.
- oog (3 px): de reductie gaf een plusteken zonder glans. Terug naar het gemeten modelovaal (natief x109–113, y51–56): (28,27) zwart, (28,28) witte glans (model natief x110–111, y52–53), (29,28) zwart, (28,29) zwart, (29,29) zwart; (27,28) lijf (model K3v7).
- voelsprieten (11 px): de buitenlijnregel maakte de linker spriet zwart en de aansluiting een zwarte klont. Per pixel naar `frac.py`: linker spriet slate (25,19) (26,20) (26,21) (27,22) (27,23), zwarte rand rechts (27,21) (28,22); (26,22) K3w2 → lucht; rechter spriet slate (31,20) (30,21), zwarte onderrand (31,21); spriettop onder de vonk (33,18) slate (model C/E/D), (34,18) randje → lucht.
- kop (2 px): (28,24) kruin en (29,22) voet rechter spriet zijn slate in het model (K2v8, K2v4w3), de reductie had zwart.
- snavelrand (2 px): (21,29) (21,30) wolk midden: het model heeft links van het snavelwit een dunne donkergrijze rand (natief L 103–114) die op deze schaal wegviel (wit tegen lichtgrijs = open rand).
- staartje (8 px): de buitenlijnregel maakte de enige slate-rij zwart (staartje werd een zwarte streep). Slate terug (45–48,45) en de zwarte modellijn eronder (45–48,46; model K2).
- ruis wolk/kop (2 px): (22,25) (24,25) → wolk midden zoals (23,25) (drie tinten naast elkaar).

Geen pixel getekend: alles is modeltint op een gemeten modelplek of opschoning volgens de regels hierboven.

## Palet (index: kleur) = k-means-centra van de modelpixels per klasse
0 transparant (152,208,160) · 1 zwart (13,17,24) · wolk 2 selout (56,70,84) 3 donker (74,87,103) 4 midden (109,121,137) 5 licht (138,151,167) 6 lichter (156,169,184) 7 wit (194,202,214) · vogel 8 donker (72,93,111) 9 midden (107,130,150) 10 licht (137,159,175) · geel 11 oker (188,166,61) 12 geel (221,199,90) 13 licht (252,242,162) · 14 snavelwit (211,216,225) 15 glans (250,251,253).
Wolk = twee materialen zoals in het model: onderwolk 3/4/5 + selout 2, lichte bollen 5/6/7 + selout 4.

## Controle (`controle.py`)
- 16 kleuren incl. transparant; index 0 transparant; per materiaal ≤ 3 tinten + lijn/selout.
- Geen lichte kleur op de buitenrand; geen losse zwarte pixels. Zwart 15,3 % van de figuur.
- Tintvlekjes < 3 px die over zijn: selout-pixels op de buitenrand van de bollen (lijn), kopkruin-hooglicht (26,24), spriet-slate (1 px breed), vonktinten, oogglans.

## Resterende twijfels (eerlijk)
- **Onderwolk:** in het model hebben de bulten van de onderwolk eigen donkere scheidingslijnen en lichtere toppen; op 0,42× blijven alleen de lichtere bovenband en een paar lijnstukjes over, dus de onderwolk leest vlakker dan het model.
- **Vonken:** 1–2 px dik; de zigzagvorm komt uit de reductie maar de okerrand neemt veel van het geel in. Leesbaar op 1×, maar minder "flits" dan in het model.
- **Linker spriet en mondlijn** zijn 1 px; de snavelonderkant is zwart (2 px) + grijs (1 rij) waar het model grijs iets ruimer heeft.
- **Het vogellijf is wat donkerder/vlakker dan het model** (hooglicht 10 op maar 3 px; het model is daar zelf vrij vlak). Een Gen 3-lichtronde (hooglicht op de kop linksboven) zou een keuze voor Jordi/Claude zijn, niet in deze ronde gedaan.
