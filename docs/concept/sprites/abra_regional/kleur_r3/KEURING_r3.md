# Keuring regionale Abra, kleur_r3 (onafhankelijke keurder, 13 nov)

Getoetst: `abra_r3.png` tegen `../referenties/gemini_gekozen.png` via `../kleur_r1/natief.png` (spritepixel (x,y) = modelblok vanaf (2x−1, 2y−14)). Alleen de twee eisen: (1) trouw aan het model, vlekjes/streepjes inbegrepen; (2) een nette Gen 3-sprite. Vergeleken op 1×, 4× en 8× naast het model op dezelfde schaal en naast Abra, Kadabra, Sneasel, Mightyena, Poochyena en Zigzagoon (`graphics/pokemon/*/anim_front.png`). Vel: `keur.png` (links r3 met MOET-pixels in rood, midden het model, rechts een proef van de keurder met alle MOET-punten toegepast; die proef is alleen een indicatie, geen sprite).

## Hoofdvraag: is dit een mooie, nette Gen 3-sprite die trouw is aan het model?
**Nee, nog niet, maar wel dichtbij.**
- **Trouw:** silhouet, pose, verhoudingen, platen, oorkerf, staartloop en de zones kloppen op 1× en 8× met het model (het is een exacte 2×-reductie, silhouet-diff 0 buiten de 3 vingergaten). Kop en platen zijn netjes.
- **Wat het oordeel bepaalt:**
  1. **Gezicht:** het linkeroog loopt over in de zwarte kaaklijn en de donkere kaak. Het leest als één zwart blok onder de snuit, terwijl het model een los, gesloten oogstreepje heeft met lichte huid eronder. Dat komt door r2-handwerk (`(22,31)` b→1) dat van het model afwijkt.
  2. **Rechteronderarm en -hand:** in het model heeft de onderarm een doorlopende donkere linkerrand van elleboog tot vingers, en de vingers hebben zwarte scheidingslijnen. In r3 ontbreekt de onderarmrand: de arm valt weg in de romp. De vingerlijnen zijn als I-plooi (luma 90 naast s 130) en met onderbrekingen getekend. Op 8× leest de hand als een mozaïek van verticale stipjes, niet als vingers.
  3. **Vibe:** het vlekje op de rechterwang (model: 3 donkere pixels op (33–34, 27–28)) is weggevallen. Jordi vroeg de vlekjes te behouden.
- Op 1× leest hij als een slappe, ingezakte Abra. Netheid van boven (kop/platen) ≈ Gen 3; de onderhelft is drukker dan Abra of Kadabra van Game Freak, vooral door 2 en 3 hierboven.

## Per zone
- **Kop/oren/ogen:** omtrek en vlakken trouw. Het rechteroog (3 px schuin) klopt. Fout bij het linkeroog en de kaak (zie MOET 1). Op de linkerrand wisselen L en K elkaar af (MOET 8). De rechterhelft van het rechteroor is in het model schaduw (s), in r3 hooglicht (MOET 11). Wangvlekje weg (MOET 4). Het oorkerf-randje `(31,19)` L is waar het model licht is, maar dat is terecht de omlijning van de kerf: goed zo.
- **Platen/romp:** trouw. Twee lichte s-pixels in de plaatnaad waar het model 4/4 zwart is (MOET 5). De kop/plaat-lijn bolt 1 px uit op rij 26 (MOET 7).
- **Linkerarm/-hand:** trouw. De linkerrand heeft T op (22,41–42) tussen L-pixels: twee lijnkleuren op één rand (MAG b). De vingerplooien zijn in I; de lijnen zijn kort, dus dat leest nog. Het vingergat (20,52) is een verdedigbare techniekkeuze.
- **Rechteronderarm/-hand:** zie de hoofdvraag (MOET 2 en 3). Het lichte band van de onderarm zelf is goed.
- **Romp/dijen:** trouw. De lijn x 26 (y 44–48) ligt een halve modelpixel rechts van de modellijn; dat is acceptabel.
- **Benen/voeten:** de teenlijn breekt op (11,49) (b waar het model zwart heeft; MOET 9). De scheen-omtrek zigzagt (16,55)→(15,56)→(16,57), een spijkertje (MOET 10). Het hielvlekje (16,56) '2' is van het model en blijft.
- **Staart:** loop en dikte trouw. De punt (x 23–25, y 59–61) bestaat alleen uit gestapelde lijnen T/L/K, terwijl het model daar een lichte punt met zwarte onderrand heeft (MOET 6). Ringstreepjes van het model liggen grotendeels onder de T-rand (MAG c).

## MOET (op impact)
| # | zone | pixels (x,y) | nu → voorstel | reden |
|---|---|---|---|---|
| 1 | linkeroog/kaak | (22,31), (23,31) | 1 → b, K → b | model `bb/mb` en `3K/bs`: lichte huid tussen oog en kaak. Nu versmelt het oog met de kaaklijn tot één zwart blok; met deze 2 px wordt het oog een los gesloten streepje zoals in het model (getest in de proef) |
| 2 | rechteronderarm, linkerrand | (36,42), (36,43), (35,44), (34,45), (33,46), (33,47), (32,48), (32,49) | s/b/h → L | het model heeft een doorlopende donkere rand van de elleboog (37,41) tot de vingers (modelpixels K/1/2 op elk van deze blokken). Zonder die rand valt de arm weg in de romp. Sluit aan op K (37,41) en de vingerlijn (31,50) |
| 3 | rechterhand, vingerlijnen | I → L: (31,50), (31,51), (33,51), (34,50), (32,52), (34,52), (35,53), (35,55); s → L: (34,48), (35,49) | zie links | in het model zwarte, doorlopende lijnen; als I en onderbroken lezen ze als mozaïek. (34,48)/(35,49) trekken lijn 2 door naar boven zoals het model (2/4 zwart) |
| 4 | wangvlekje rechts | (34,27) | s → I | model: vlekje van 3 donkere pixels (luma 74–81) op (33–34, 27–28); Jordi: "behoud die vibe". Eventueel (35,27) erbij als het model op 8× een streepje van 2 px laat zien |
| 5 | schouder, plaatnaad | (44,32), (43,33) | s → K | model 4/4 zwart; nu een lichte stip in de naad |
| 6 | staartpunt | (24,60), (25,60) | L → b, L → s | model `bb/KK`, `ss/KK`: lichte punt met zwarte onderrand. Nu liggen T, L en K gestapeld (dubbele lijn, geen vulling) |
| 7 | kop/plaat-lijn | (37,26), (38,26) | s → K, K → 1 | model `KK/sK` en `11/K1`: de lijn loopt (37,25)→(37,26)→(38,27); nu bolt de kop 1 px de plaat in |
| 8 | kop, rand lichtkant | (21,19), (18,22), (19,24) | K → L | zwart en lijnkleur om en om op één rand (SPRITE_KERN: nooit). (21,19) is in het model zelfs grijs (`../2s`) |
| 9 | linkervoet, teenlijn | (11,49) | b → I | model `../KK`: de lijn (10,50)–(13,49) breekt nu op een lichte pixel |
| 10 | linkerscheen, omtrek | (15,55), (16,55) | . → K, K → s | zigzag-spijkertje in de omtrek. Model (15,55) `.K/..` steunt de rand op x 15 (alternatief: (15,56) K → . en (16,56) 2 → K, maar dan valt het hielvlekje weg). Let op: dit is 1 silhouetpixel erbij (`bewaak.py` meldt hem) |
| 11 | rechteroor | (34,17), (34,16) | h → s, h → b | model `ss/ss` en `hs/bs`: rechterhelft van het oor in schaduw (ook juist bij licht linksboven) |

## MAG
| # | pixels (x,y) | voorstel | reden |
|---|---|---|---|
| a | (30,58) | I → K | onderrand van de vingertop: T, I en K naast elkaar op één rand; model `KK/..` |
| b | (22,41), (22,42) | T → L | één lijnkleur op de linkerrand van de linkerarm (model grijs 2/3, tussen L en T in) |
| c | (52,52) | s → I | ringstreepje van de staart (model luma 83); de andere ringen van het model liggen in de T-rand |
| d | (22,50) | b → I | top van de vingerplooi links (model luma 57), sluit aan op (22,51) |
| e | (27,30), (13,50) | s → I | kleine modelvlekjes (luma 76 en 68) op de wang onder het rechteroog en op de scheen (vibe) |
| f | (53,52), (52,53) | b → s | de buitenkant van de staartbocht is in het model s (luma 127–130): schaduwkant |
| g | (28,20) b → s; (39,40) s → b | | vulling volgt de modelmediaan (129 resp. 183) |
| h | rechterhand, vullingen | per vinger één vultint (h/b/s) in plaats van een afwisseling per pixel | na MOET 2–3 nog drukker dan nodig; alleen waar het model per vinger één toon heeft |

## Controle op de proef (keurder, niet opgeleverd)
Alle MOET-punten toegepast op een kopie (scratchpad): `bewaak.py` geeft 11 kleuren, zwart 20,7 %, K+L 33,9 %, geen vulling op de buitenrand. De enige "fouten" zijn het wangvlekje (34,27) als losse lijnpixel (bedoeld) en de silhouetpixel (15,55) (MOET 10). Op 4× en 8× leest het linkeroog dan los, en de rechteronderarm is een eigen ledemaat. Zie rechts op `keur.png`.

## Ter info voor Jordi (geen fout)
- Zwart 20,9 %: net boven de Gen 3-norm, maar binnen E3 voor een Dark-type met donkere platen. Vooral de kaak en de platen zijn zwaar; dat volgt het model.
- De handen hebben in het model vingers van 1 px; op 1× blijven ze een lichte vlek met streepjes. Dat zit in het model, niet in de vertaling.
- De huidkleur is nog de grijze modeltoon (nog geen keuze van Jordi).
