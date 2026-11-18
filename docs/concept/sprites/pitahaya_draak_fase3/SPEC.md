# Pitahaya-draak fase 3 (komododraak; werknaam open), frontsprite naar Gemini-model

- Lijn: pitahayahoofd met cactusrank-lijf (fase 1, `../pitahaya_draak/af/`) → teju (fase 2, `../pitahaya_draak_fase2/af/`) → **komododraak (deze)**. Pseudo-legendary eindvorm, waarschijnlijk Grass/Dragon.
- **Model (bevroren ontwerp):** `model/model.png` (= `gemini/r4a_tong.png`, met tong). Zonder tong: `model/model_zonder_tong.png` (= `gemini/r4b_zonder_tong.png`, verder pixel-gelijk). Kijkt al naar links, niet spiegelen. Prompts: `gemini/PROMPT.md` v1–v4.

## Jordi (letterlijk)
- 16 nov: "dan is fase 2 een teju en fase 3 mag op 2 poten staan, maar voorover leunend, komodo draak"
- 17 nov over r1: "beetje too much overdesigned, plus qua ontwerp vertaalt die niet lekker naar een sprite. Ik zou het nog vet vinden als we nog iets van een dragonfruit bloem erin verwerken en de staart een knots heeft als een dragonfruit" · "en het lichaam dan wat groener misschien?"
- Over r2: "pose, staart en hoofd zijn prima" · "roze op de rug en cactusribben in het lijf"
- Over r3: "de bloem moet weg en de tong vraag ik me af hoe die naar sprite vertaalt"
- Over r4: "probeer maar met tong en kijk hoe dat vertaalt, en of de tong bij het concept past"

## Keuzes Claude (niet besproken)
- Maat: eindvorm, vult het 64×64-vlak (model ±900×740 → ±62 px breed), op de bodem.
- Tong: echte komodovaranen hebben een gele gespleten tong; past dus bij het komodo-deel van het concept.
- Over de sprite (17 nov): "Maak nog een extra versie ernaast waar de buik de kleur krijgt van het vruchtvlees. Dus wit met zwarte spikkels" → variant `_buik` (op de versie met tong).

## Af (18 nov), ronde 6
- `af/pitahaya_draak_fase3.png` (A, met tong), `_zonder_tong.png` (B), `_buik.png` (C: buik in vruchtvlees wit met pitjes, op A); elk ook `_8x`; samen `af/keuze_8x.png`. Keuze A/B/C aan Jordi.
- Rondes in `sprite_r1/`–`sprite_r6/` (3 makers; keurder na r4: arm/keel FAIL; keurder + Dragonfly Cave na r5: A en B PASS, C 3 technische punten → r6 gerepareerd). Palet = teju (fase 2). 61×50 px.
- Buikzone door de maker vastgesteld (model heeft geen buikkleur); keurder ter info: leest op 1× ook als witte bef/sjerp omdat de nabije arm de onderbuik bedekt.

## Jordi (18 nov), reactie op A/B/C
- "de tong lijkt zo niet echt op een tong, dus haal die maar weg. Daarnaast vind ik rechts de beste, maar ik heb nog wel wat kritiek. Er is geen belijning tussen de achterpoot en de staart, lijkt net een blur. Plus het schaduw en kleur gebruik is in de hele sprite nog niet optimaal. Kan je daar nog aan werken? Hoofd en de vruchtvlees buik zijn nog het beste, maar verder mist die al het contrast dat sprites normaal wel hebben"
- → basis = C (buik) zonder tong; ronde 7: lijn achterpoot/staart, schaduw en kleur/contrast in de hele sprite; kop en buik zijn het beste.
- Jordi (18 nov), tijdens r8: "de dynamiek in de staart dragonfruit moet ook behouden blijven, dus de groene rafels"
- Jordi (18 nov): "degene aan het uiteinde is te groot en aan de beenzijde zijn ze verdwenen" (rafels knots)

## Af (18 nov), ronde 9
- `af/pitahaya_draak_fase3.png` (+ `_8x`) = r9: buik vruchtvlees, zonder tong; lijn achterpoot/staart, contrast op Sceptile-niveau, rafels knots naar het model. Keurder r8 FAIL (klein) → r9 PASS. Vergelijking `af/af_vs_r6_8x.png`; de drie r6-versies in `af/oud_r6/`.
- Ter info (keurder, optioneel): verre achterbeen staat twee tintstappen onder de verre arm (Gen 3-norm één stap).

## Jordi (18 nov), reactie op r9
- "hij is al iets beter, maar de knots staart vind ik nog niet perfect. Hij is nog niet genoeg los van het been, het is onduidelijk te zien of rechtsbovenin de staartknots of dat nou een rafel is of het been. De binnenkant van de mond is ook een beetje slordig met maar 1 zwarte pixel. Of we moeten iets bedenken hoe we daar 1 of 2 pixels kunnen toevoegen zodat het duidelijk vruchtvlees is, of we moeten de kleur aanpassen. Kloppen de schaduwen, lijnen en kleuren verder goed?"
- → r10: knots los van het been (rechtsboven duidelijk rafel óf been); bek in twee varianten (A: 1–2 pitjes erbij, B: andere kleur binnenkant).
- Jordi (18 nov) over r10: "de binnenkant van de mond is niet verbeterd, 2 stipjes onder elkaar geeft niet het juiste effect. Doe de stipjes op de buik ook onregelmatiger" → r11: bek in 3 varianten, buikpitjes onregelmatig.
- Jordi (18 nov) over r11: "d is het beste, maar deze rechte lijn die ik geel getekend heb aan sprites ziet er een beetje gek uit, in de mond kan dat onderdeel van het wit worden en buiten de mond kan die misschien iets minder rechtlijning worden" (screenshot `sprite_r11/jordi_feedback_D.png`; lijn = rij y30, x7–16)
- Jordi (18 nov) over r12: "check bij de 5 pixels die ik gelijnd heb of de schaduwkleur nog klopt" (`sprite_r12/jordi_feedback_schaduw.png`; (8–10,30) grijs vlees, (8–9,31) ondertanden). Claude: grijs onderin vooraan is geen logische schaduw bij licht linksboven → r13 varianten.
- Jordi (18 nov) over r13: "F is juist weer helemaal fout, welke vind jij het best consistent qua schaduw" → Claude: G (schaduw alleen onder de bovenkaak en achterin, ondertanden in schaduw van de onderlip zoals het model). G gaat naar de eindkeuring.

## Af (18 nov), ronde 14
- `af/pitahaya_draak_fase3.png` (+ `_8x`) = r14 = r13 G + 7 px van de eindkeuring (schaduw achterin de bek, banding staartlus, knots rechtsonder donkerst, rafels lichtkant). Vergelijking `af/af_vs_r9_8x.png`; r9 in `af/oud_r9/`.
- Open (niet door Jordi genoemd na r12): rechte lijn onder de kaak buiten de bek (zwart (13–16,30) + grijze buikrand (17–22,30)).
- Jordi (18 nov): "de stippen op de buik waren eerst beter, kopieer de buik van eerder en dan is die klaar" → r15 = r14 + buikpitjes van r10A (17 px, `sprite_r15/maak_r15.py`). **Af.**
