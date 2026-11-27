# Kudu (fase 3 van 3, impala-lijn, Normal/Steel)
Alle citaten en lijnbesluiten: `docs/concept/IDEEEN.md` → "Impala-lijn"; samenvatting `POKEMON.md` → Impala-lijn. Prompts/rondes: `gemini/PROMPTS.md`. Fase 1: `../dikdik/`, fase 2: `../impala/`.

## Vast (Jordi)
- Normal/Steel; "beide steel, hoorns echt van metaal, alleen de dikdik niet".
- "het belangrijkste is dat de vorm van de hoorns blijft kloppen" (kudu = open kurkentrekkerspiraal).
- Overdrijven "zodat ze een beetje afwijken van de dieren ook, maar de inspiratie wel nog kenbaar is".
- Lichaamskleur goud ("lichaamskleur he").
- Hoorns: spiegelglans met witte slijprand ("akkoord", 25 nov).
- Tekening: witte verticale strepen + witte V tussen de ogen (wit = slijprand-wit) ("akkoord", 25 nov).

## Keuzes (Jordi, 26 nov, meerkeuze)
- Uitstraling: **koninklijk, kalm** (majestueus en rustig, kop hoog, hoorns als kroon).
- Manen: **manen + keelfranje** (kuif groeit door tot echte manen over de hals, plus de keelfranje van een echte kudubok).
- Hoorns: **heel groot** (overdreven, 2–2,5 draai, ongeveer even hoog als het lijf; bepalen het silhouet).
- Pre-evolutie: **niet noemen** in de prompt.
- Grootte (Jordi, 26 nov): "mag echt een grote sprite zijn ook".
- Strepen (Jordi, 26 nov): "de kudu strepen moeten we wel erop doen ook indien mogelijk".
- Manen (Jordi, 26 nov, meerkeuze): over de hals/schouders (vanaf achter de oren over de bovenkant van de hals naar beide kanten over de schouders, voller dan paardenmanen, eindigen op de schouder).
- Hoorns (Jordi, 26 nov, meerkeuze): naar achteren, even groot, schuin over de rug naar de hoek rechtsboven (zodat kop en lijf groter in het vak staan). Beste manen tot nu toe: r3b.

## Model (Jordi, 26 nov)
- Gemini r1–r5 (+ r3b/r3c bijgestuurd), zie `gemini/PROMPTS.md`. Jordi: "ik denk dat we met gemini niet verder gaan komen"; "kan jij niet gaan bouwen en de manen in de sprite aanpassen desnoods?"; "het moet namelijk geen baard of sik worden, maar echt nekhaar dat over de schouders valt"; **"r3b zit het dichtste bij mijn visie"**.
- **Model = `referenties/model_r3b.png`** (Gemini r3b). Afwijking die Jordi toestaat: de manen in de sprite aanpassen tot nekhaar dat over de schouders valt (geen baard of sik).
- Keelfranje: op de vraag of die als baard/sik leest, Jordi: "nee hoor ik zie daar echt ruimte tussen" → blijft zoals in r3b.
- Open: grootte (Jordi r4: "lijkt wat klein").
- **Manen (Jordi, 26 nov): variant A** (`sprite/r1/model_A.png`: manen van r3b naar achteren/omlaag over de schouder): "A is goed, alleen houd er rekening mee dat gemini die boog had gedaan omdat er een schouder zat, dus die boog hoeft geen boog meer te zijn".
- **Model manen = `sprite/r3/model_A3.png`** (keelfranjelokken van r3b gespiegeld over de schouder, kamlokken erboven). Jordi (26 nov): "klopt wel nu dat je de nek niet helemaal goed ziet in de sprite, dat moet duidelijker".
- Oog (Jordi, 26 nov, op r6 met oog B): "hij heeft een veel te lief oog"; over de varianten A–D: "alle 4". Nieuwe strengere varianten in `sprite/r6/oog_streng_varianten.png`.
- **Manen opnieuw (Jordi, 26 nov, op r6):** "nekharen zijn een grote pixel blur, daar is echt niks uit te halen"; "kijk bijv naar growlithe, arcanine of soortgelijke pokemon met manen of vacht"; "maar het moet dus los zijn, ponyta en rapidash hebben vlammen dus werken niet, de rest hebben geen manen of extra vacht"; "het moet los van het lichaam zitten"; "kijk alle gens door daarvoor"; "dus furfrou ook niet". Ronde 7 (`sprite/r7/`).
- Op r7 (Jordi, 27 nov): "wel goed, je kijkt naar de andere pokemon en doet vervolgens compleet iets anders"; "met allemaal rechte pixellijnen, want ja dat hebben alle pokemon". r8: vacht van Arcanine/Growlithe 1-op-1 overnemen.
- Jordi (27 nov): "wat andere pokemon doen is geen banen, meer gewoon de vorm een beetje gerafeld".
- Jordi (27 nov): "pyroar heeft bijv ook manen maar dat is gewoon een lang hangend kapsel"; "de vrouwelijke variant".
- Jordi (27 nov): "nee hij moet de pyroar niet nadoen" (Pyroar alleen als voorbeeld van een lang hangend kapsel).
- **Oog (Jordi, 27 nov): "k4 voor oog"** = Bidoof-oog 1-op-1 (`sprite/r6/kudu_r6_oogK4.png`, bron in `sprite/oog_klein.py`).
- Jordi op r8 (27 nov): "de vorm klopt niet, gezien het links veel meer eroverheen loopt dan rechts, daarom houd je ook bijna geen ruimte over. Links is het zelfs helemaal 1 geworden met de poot, wat een prutswerk weer".
- Jordi op r9 (27 nov): "het is qua vorm nu iets te wollerig".
- Manen (Jordi, 27 nov): "doe maar b6b, maar netter, minder rechte lijnen" → r11 (B6b opgeschoond). Jordi op r11: "HUH", "wat is dit"; daarna: **"o dat is mijn fout, b6a bedoelde ik"** → keuze = `sprite/r10/kudu_r10_B6a.png`, netter, minder rechte lijnen (r12). r11 vervalt.
- Manen (Jordi, 27 nov): "linkerstuk van r10 b6a en rechterstuk van r12 van de maan" → `sprite/r13/kudu_r13.png` (B6a + r12 vanaf x30 = schouderrand; 15 px). "en dan naar eindkeuring".
