# Onweerswolk-Altaria frontsprite, ronde 3: op het kop×1,5-dy10-model

**Model:** `../model_kop/natief_kop15_dy10.png` (kop ×1,5 t.o.v. het origineel, 10 natieve px in hals/wolk gezakt; `kop13.py 1.5 10`). Jordi: "let er bij altaria op dat het linkeroog ook zichtbaar moet zijn voor de sprite om mooi te worden, als dat niet past is het hoofd nog steeds te klein". Verder (letterlijk): "iets minder detail is niet erg tov het model, zolang die niet blurry wordt"; "De belijning moet juist zachter en niet zwart"; "het ligt aan dat er meer dan 2 kleurtinten moeten zijn om minder blur te hebben".

**Silhouet:** `basis.py` = de r2-basis (r1-regels) op het nieuwe model, `KOP=(50,75,60,106)`, `KUIF=(48,70)`, 3 rijen gepad → `basis_kop15.png`. Figuur x3–61, y5–62, 1953 px. **Alpha-diff sprite ↔ basis = 0** (`controle.py`). Alleen kop/kuif verschillen van r2; wolk, hals en static-plekken zijn dezelfde modelpixels.

Bestanden: `altaria_r3.png` (64×64, geïndexeerd, index 0 transparant, 13 kleuren incl. transparant), `altaria_r3_8x.png` (wit), `vel.png` (r3 | r2 | nieuw model op schaal | game-Altaria, 8× / kop-close-up 16×: r3 | natief model | game-Altaria-kop / 1× op wit, crème, donker, zwart + model + game), `bouw.py` (`python3 sprite_r3/bouw.py`, vanuit `altaria/`), `basis.py`, `controle.py`, `vel3.py` (`python3 sprite_r3/vel3.py sprite_r3/altaria_r3.png sprite_r3/vel.png sprite_r2/altaria_r2.png model_kop/natief_kop15_dy10.png 3`).

## Palet (13 incl. transparant)
| | selout | donker | midden | licht | hooglicht |
|---|---|---|---|---|---|
| wolk | (34,58,92) L55 | (46,80,112) L73 | (62,104,138) L95 | (84,134,166) L123 | (136,192,214) L178 |
| violet | (44,44,116) L53 | (66,68,160) L78 | (98,100,210) L112 | (144,146,236) L156 | |
Pupil (16,18,40) alleen in de ogen (5 px). Static (120,216,248) L191: even licht als het hooglicht maar veel verzadigder blauw (Jordi: "niet geel maar meer blauw"). Glans (240,244,255) 1 px. Wolktinten liggen dicht bij de modeltonen (L44/72/122/186); de selout is bewust lichter dan het model (L55 i.p.v. zwart/L30). Geen navy, geen zwart op de buitenrand.

## Wat de kale reductie is
Per spritepixel het 3×3-blok van het natieve model, ingedeeld in de vier modeltonen (wolk L<58 / <100 / <156 / ≥156; violet <85 / <130 / ≥130; K = zwart). Wolk: **kappen per modelbol** (licht+hooglicht ≥5/9 van het blok, per samenhangende modelkap gelabeld; raken twee kappen elkaar, dan blijft de pixel met de minste dekking lijftint), hooglicht waar ≥4/9 hooglicht; buiten de kappen donker als de blokhelderheid < 62, anders midden. Violet: gewogen modus. Dat is `kaal` in `bouw.py`; alles hieronder is per stap geteld t.o.v. die reductie.

## Afwijkingen van de kale reductie, per zone (spritepixels)
- **Wolk overig: 503 van 1449**, waarvan 171 op de buitenrand (buitenlijn = wolk-selout) en 332 binnen:
  - naden: doorlopende zwarte modellijnen (≥2 K in het blok, 8-samenhangend ≥3 px) → wolk-selout (o.a. de twee lagen van de onderrok en de rand tussen bolwolk en rok, Y51–55);
  - ontkorrelen: tintvlakjes < 4 px (hooglicht < 3) naar de buurtint, 1-px-uitsteeksels weg;
  - kapvolume (102): hooglicht alleen linksboven in een kap; de 2 px aan de rechteronderrand van elke kap worden licht (anders was de grote voorste bol een vlak hooglichtblok van ±50 px);
  - onderbogen (69): waar een lichtere bol direct boven een donker dal ligt, wordt de bovenste dalpixel selout, alleen stukken ≥3 px (gebogen lijn onder de modelbol, MOET 2);
  - losse pixels (4) en halsrand (41, zie hals).
- **Kop: 76 van 136** (`KOPGRID` in `bouw.py`, Y19–28, X19–33), alles naar de modelblokken:
  - **ver oog** 1×2 zwart op (22,22–23). Model-oog: natief x65–69, rij 54–59 = X20,7–21,7, Y22,8; de koprand ligt op X20. Om lijn | kopkleur | oog te krijgen staat het oog **1 px rechts van het model** (X20 violet-selout, X21 midden-violet, X22 oog), kopkleur ook erboven (22,21). Dat is de enige verschuiving in het gezicht; het silhouet bleef gelijk (pixel (19,22) is achtergrond, dus de lijn kon niet naar links).
  - **nabij oog** 2×2 op (27–28,22–23) met glans linksboven (27,22) (model x85–88, rij 54–59; game-Altaria: nabij oog met glanspixel).
  - **snavel** X19–26, Y24–27 (model: licht teal L136–206): Y24 hooglicht met licht aan de randen, Y25 hooglicht/licht, Y26 licht met de mondlijn (24–26,26) in wolk-selout naar de mondhoek (27,26) (model rij 66–67 x77–84 zwart), Y27 onderkaak licht/midden (model rij 69–70 L155–169), omlijnd in wolk-selout (snavelpunt (19,25), onder (20–21,26–27), (22–23,28)). Geen zwart.
  - **wang** X28–31, Y25–26 (model L148–196): hooglicht (29–30,25), rest licht/midden.
  - kopvolume: lichtviolet linksboven (zoals de modelglans, Y19–21 X22–27), rechterrand X32 en onder de wang (Y27) donkerviolet (model L60), omlijning violet-selout; Y16–18 wolk-selout uit de reductie in de kopzone → violet-selout.
- **Kuif: 115 van 170**: vorm = silhouet van de reductie (geen pixel bij of weg). Alleen opnieuw ingekleurd (MOET 5): onderkant/schaduwkant van een streng die daar ≥2 dik is → violet-selout; pixels zonder achtergrondbuur → lichtviolet; rand en takjes van 1 px → midden-violet. Twee hoofdstrengen lopen door (A: Y9–17 boven, B: Y13–19 onder), de vorken zijn die van het model (A: omhoog bij X31–36 Y4–8 en rechts X42–47 Y6–12; B: rechts X46–51 Y13–17). Geen lichte kleur op de buitenrand.
- **Hals: 44 van 83** (Y29–40): doorlopende violet-selout waar de hals aan de wolk grenst (model: donkere halsrand), de wolk-selout ernaast weg (geen dubbele lijn), lichtviolet langs de linker- en donkerviolet langs de rechterrand (volume, licht linksboven). Halspuntje (23,41) onder de wolkrand → wolklijn.
- **Static: 115 px** (5,9 %), op de modelplekken uit `statisch()`: blok met ≥2 static-modelpixels, plus blokken met 1 die aansluiten; 2×2-klontjes uitgedund; **alleen lijnen ≥10 px** (weinig, langere zigzaglijnen, MOET 6), de losse boogjes naast de vleugels (model, links x3–5 en rechts x59–61) ≥4 px. Op de buitenrand alleen die boogjes; elders blijft de wolklijn. Resultaat: 8 stukken van 6–35 px; geen stukje < 4 px (8-samenhangend). Het rechterboogje (x59–61) is opgegaan in de lange lijn langs de rechtervleugel.

## Controle (`controle.py`)
13 kleuren incl. transparant; alpha-diff 0; zwart alleen in de pupillen (5 px); geen lichte kleur op de buitenrand; pixels zonder 8-buur van dezelfde tint: 9 (oogglans, kuiftakpunten (31,7) (35,9) (46,10), wang/snavelschaduw (26,25) (31,26), statichoekjes (53,18) (52,20), (22,32) wolkpixel naast de halsrand). Aandeel van de figuur: selout 16,5 %, donker 14,5 %, midden 26 %, licht 13,2 %, hooglicht 5,5 %, static 5,9 % (r2: wolk-donker ±40 %).

## Keuring r2 (MOETEN) → r3
1. Buitenlijn: wolk-selout L55 rondom, violet-selout L53 op kop/hals/kuif; geen navy/zwart. ✔
2. Bollen: kappen per modelbol, hooglicht linksboven, onderbogen; donker ±15 % i.p.v. 40 %. Beter dan r2, zie twijfels.
3. Vleugelrand: silhouet = reductie (niet gladgestreken); de rand heeft de golfjes die de reductie geeft (rechtervleugel Y17 inham bij X54). Zie twijfels.
4. Onderrok: de twee modellijnen (Y51–55 en de lichtere onderste laag Y55–58) staan als selout-lijn/lichtere laag. ✔ (meer lagen dan dat geeft de reductie niet)
5. Kuif: twee doorlopende strengen, selout alleen onder, vorken van het model. ✔
6. Static: eigen blauw, 8 stukken (6 lijnen van 11–35 px, het boogje links 7 px en een door de buitenlijn afgesplitst eind van 6 px); geen stukjes < 4 px. ✔
7. Ver oog: lijn | kopkleur | oog. ✔ (1 px rechts van het model, zie boven)

## Eerlijke twijfels
- **Wolk:** leest als bollen met kappen en onderbogen, maar de kapranden zijn op 64 px nog wat hoekig (vooral de grote voorste kap X21–34, Y40–45 en de linkervleugeltop); ronder kan alleen door te tekenen. De vleugeltoppen zijn lichter en vlakker dan in het model.
- **Vleugelrand (MOET 3):** ik heb het silhouet bevroren gelaten (= reductie, zoals de opdracht). De linkervleugel-bovenrand loopt in trapjes 1‑3‑1‑2‑2; meer golf zou 1 px in/uit per bol aan het silhouet vragen (alpha-wijziging), dat heb ik niet gedaan.
- **Static** is fel en op 1× het eerste wat opvalt (vooral de boog langs de rechtervleugelrand, 35 px). Minder (alleen ≥14 px) kan met `SMIN=14`; dan verdwijnt de static op de linkervleugel.
- **Ver oog** staat 1 px rechts van het model; daardoor zijn de ogen 1 px dichter bij elkaar dan in het model.
- Snavel is (zoals het model) een brede teal snuit; op 1× leest hij goed, op 8× is hij iets donkerder dan de modelsnavel (hooglicht L178 i.p.v. L196–206).
