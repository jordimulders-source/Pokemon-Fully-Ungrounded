# Pitahaya-draak fase 3 (komododraak), sprite r1 (maker)

Methode: model overnemen, niets tekenen (fase 2-recept, aangepast aan een niet-gehele verkleining): natief raster → oppervlak-gewogen reductie met regels → lijnen uit het modelskelet (spooktrein-methode) → technisch opschonen. Elke gewijzigde pixel staat met stap in `pitahaya3_r1_afwijkingen.txt` (stap x y oud nieuw).

## Stappen (reproduceren)
```
python3 natief.py ../model/model.png natief.png                 # raster 3,998 px, fase 3,25 → natief 255×255, figuur 227×184
python3 natief.py ../model/model_zonder_tong.png natief_zonder_tong.png
python3 groepen.py                                              # controle groepen.png
python3 half.py kaal.png --zt .45 --pt .35 --vt .3 --ox 1.8 --oy 0
python3 half.py kaal_zonder_tong.png --nat natief_zonder_tong.png --ref natief.png --plaats 1,1,13,1 --zt .45 --pt .35 --vt .3 --ox 1.8 --oy 0
python3 maak_r1.py kaal.png natief.png pitahaya3_r1.png
python3 maak_r1.py kaal_zonder_tong.png natief_zonder_tong.png zonder_tong_pijplijn.png
python3 zonder_tong.py pitahaya3_r1.png zonder_tong_pijplijn.png pitahaya3_r1_zonder_tong.png
python3 controle.py pitahaya3_r1.png ; python3 vel.py
```
1. `natief.py`: pitchzoeker (3,9–4,1) vond **3,998 px** (pieken ook op 8 en 12 = veelvouden); op een uitvergrote oog-/bekuitsnede gecontroleerd: 1 cel = 4 modelpx.
2. `groepen.py`: bg (bijna-wit vanaf de rand + ingesloten gaten ≥ 6 px buiten bek/oog: staartgat), zwart (lum < 45), roze, groen (G ≥ R), wit/grijs (vlees, tanden, oogwit), pit (grijs/zwart in de bek), **geel = tong** (hue 30–62, alleen componenten ≥ 20 px; olijf/crème tongrand erbij, crème met achtergrondburen = halo). Lichte anti-aliasrand (wit met ≥ 3 achtergrondburen) = achtergrond.
3. `half.py`: factor **S = 3,661** (figuur 227 natief → 62 px), oppervlak-gewogen via 4× supersampling. Regels per spritepixel: achtergrond bij ≥ 50 % (behalve ≥ 30 % groen: dunne stekelpunt), zwart bij ≥ 45 % (alleen dichte zwarte vlakken; dunne lijnen komen in stap L), tong bij ≥ 30 % geel, pit ≥ 35 %, vlees ≥ 30 % wit, anders meerderheid → gemiddelde → dichtstbijzijnde modeltoon. Fase ox 1,8 / oy 0 gekozen uit 9 + 16 fases op het oog (wit + zwart, tanden, tong met vork).
4. `maak_r1.py` (volgorde):
   - **T** binnenvulling roze/groen uit de gladde modelhelderheid (σ 1,5 spritepx, zonder de donkere naad-/ribpixels), 3 vultonen op de eigen verdeling (30 % schaduw / 50 % midden / 20 % licht). Volume blijft, de ribvlekjes van de vlakreductie verdwijnen.
   - **L** lijnen: alle donkere modellijnen (zwart, donkergroen lum < 72, donkerroze lum < 62) → Zhang-Suen-skelet → per skeletpixel naar het spriteraster (`lijnen.py`). Zwart waar de skeletpixels echt zwart zijn, anders donkergroen (rib) / donkerroze (schubnaad); ribben alleen van modellijnen ≥ 25 natieve px; stukjes < 4 spritepx vervallen (zwart → vlaktint).
   - **A** lijnen 1 px dun (weghalen breekt geen verbinding en een 4-buur is minstens zo sterk) → vlaktint.
   - **SP** dunne uitsteeksels: natief silhouet min opening (schijf r 5) = stekel-/klauwpunten; hun skelet geprojecteerd; achtergrondpixels daarop naast de figuur worden groen.
   - **B** buitenlijn 1 px: richting uit de gradiënt van het gladde silhouet; naar licht linksboven = selout (roze (112,41,58), groen (48,80,35)), anders zwart; 1 px dunne groene punten houden een groene rand.
   - **C/C2** losse vulpixels → buurtint uit dezelfde groep.
   - **KOP/TONG/RECHT**: zie hieronder.
5. `zonder_tong.py`: hoofdversie + alleen de zone x 0–12, y 26–38 uit dezelfde pijplijn op `model_zonder_tong` (zelfde geometrie). **Assert: buiten de zone diff 0**; 31 px anders. Reden: het Gemini-model zonder tong is niet echt pixel-gelijk (overal ruis tot ±40 in RGB), dus een volledige tweede run gaf 281 px verschil door het hele lijf.

## Maat en palet
- **61×50 px, 1804 px** (zonder tong 1787), x 1–61, y 13–62 (onderste rij 62, 1 px marge). Kijkt naar links, niet gespiegeld.
- **16 kleuren incl. transparant** (zonder tong 13), allemaal modeltonen: zwart (8,11,3) · roze (112,41,58) (185,44,96) (229,76,130) (238,105,150) · groen (48,80,35) (74,109,62) (104,142,83) (133,169,106) · vlees grijs (188,189,193) wit (242,241,246) · tong olijf (122,100,25) midden (203,175,83) licht (250,222,143) · pit (79,69,76).
- Zwart binnen de figuur **8,3 %** (Gen 3 1–8 %); buitenrand 51 % zwart (Gen 3 45–68 %). Dambord 0.

## Afwijkingen van de kale reductie (1059 unieke px; per stap en zone)
| Stap | kop+tong | romp+rug | voorpoot/knots | dij/staart | totaal |
|---|---|---|---|---|---|
| T toonkaart | 105 | 299 | 32 | 160 | 596 |
| L lijnen uit modelskelet | 63 | 109 | 31 | 115 | 318 |
| A lijn dunner | 7 | 6 | 5 | 14 | 32 |
| SP stekelpunten | 3 | 4 | 2 | 0 | 9 |
| B buitenlijn | 49 | 70 | 50 | 91 | 260 |
| C/C2 losse pixels | 8 | 10 | 2 | 4 | 24 |
| KOP oog/bek | 9 | 0 | 0 | 0 | 9 |
| TONG tint | 2 | 0 | 2 | 0 | 4 |
| RECHT staartonderkant | 0 | 0 | 0 | 6 | 6 |

**Pixels die niet uit een regel komen (KOP, per pixel gemeten; model natief oog x 46–54, y 81–89: lid schuin (53,81)→(46,86), pupil = kolom 49, wit x 50–53):**
- (10,21) en (11,21) → zwart: ooglid (32 % en 24 % zwart in het venster).
- (10,22) → wit: oogwit 84 %, modeltint 252. (10,23) → grijs: onderkant oog, wit 52 % met modelgrijs 199–241. Pupil (9,22) zwart en (9,23) wit stonden al zo in de reductie. Het oog is dus lid | pupil (1 px, voor, onder het lid) | wit.
- (6,27) → wit: tand 2 (49 % wit). (13,25) → wit: hoektand in de mondhoek (43 % wit).
- Pitjes (9,27) (17 %, sterkste in het binnenvlak) en (11,28) (10 %); niet 8-naast elkaar, niet op dezelfde rij/kolom op 2 px (fase 2-regel). Het model heeft ±25 pitjes; het vleesvlak is maar ±4×4 px, meer gaf dambord.
- (9,30) → grijs (alleen met tong): tussen tong en onderlip; model is daar rood/wit gemengd; grijs volgens fase 2 (geen roze binnenin).
- **RECHT**: onderkant staart was 15 px recht (rij 62). Eindpixels met de hoogste achtergrondfractie weg: (36,62) 44 %, (50,62) 34 % en (49,62) 28 %, de pixel erboven wordt zwarte rand. Nu 12 px; het model is daar zelf vlak (de rest heeft < 25 % achtergrond).

## Tong
- **26 px** (19 midden, 4 licht, 3 olijf), ±2 px breed, van de bek (7–9,29) schuin naar linksonder tot de vork op (1–4,35–37): linkertand (1,35)–(1,36), onderste tand (3,36)–(3,37), met een achtergrondgat (2,36) ertussen (model 27 % geel daar).
- Tint per pixel uit de gemiddelde helderheid van de gele modelpixels (olijf < 140, licht ≥ 195): licht streepje linksboven op de steel (4,32) (3,34) (2,35), olijf op de rechteronderrand (8,30) (4,36) en het einde van de linkertand (1,35).
- Leest op 2× en groter als gele gespleten tong; op 1× als een geel streepje met een gaffeltje aan het eind. De gele kleur steekt goed af tegen roze en wit; de vork is 1 px per tand en blijft net leesbaar door het ene achtergrondpixel ertussen.

## Zelf vergeleken (vel.png: r1 | zonder tong | model op 8×, kop 12×, 1× en 2× op licht en donker)
- Leest als het model: groene komodo op twee poten, voorover, roze kop met groene schutbladen, roze rug met groene stekels, gele tong, roze pitahaya-knots aan de staart, gat tussen staart en dij.

## Zwakke punten (eerlijk)
- **Kop is druk**: de vele zwarte bracteeranden van het model worden op 20 px kop losse zwarte streepjes (vooral (14,15)–(14,19) en (17–19,19–23)); het gezicht leest op 1× vooral via oog en witte bek.
- **Stekels op de rug klein** (1–2 px puntjes): de modelstekels zijn 1–1,5 spritepx breed; SP voegde er maar 9 px aan toe. Ze lezen als kartelrand, niet als duidelijke punten.
- **Klauwen**: nabije hand (31–37,44–47) is een zwarte klont van de W-vormige modelklauwen; de voorste hand (10–17,40–45) heeft geen leesbare klauwen.
- **Ribben**: donkergroene lijnstukjes op dij en staart; geen zebra, maar op de romp/nek wisselen ze met zwarte lijnstukjes en dat geeft wat onrust.
- Losse pixels met opzet: oog, tanden, pitjes, tongpunt. Twee echte restjes: (30,47) groen en (20,58) roze, elk ingesloten door zwart.
- Staartonderkant nog 12 px recht (model vlak).
- Zwart binnen 8,3 %, net boven de Gen 3-band.
- Palet: tonen zijn modeltonen, nog geen Gen 3-kleurronde (Jordi: kleur mag afwijken); roze stappen 63/94/121/145 en groen 70/96/127/155 helderheid.
