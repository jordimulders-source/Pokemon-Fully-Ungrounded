# Regional Baltoy-lijn (Baltoy → Claydol, Rock/Psychic)

## Jordi, letterlijk
- 21 nov: "De regional Baltoy lijn wordt denk ik rock/psychic, waar het origineel nu dus ground/cosmic is".
- 22 nov: "tijd voor de regional baltoy lijn".
- 22 nov, inspiratie (keuze uit 4): **Tiwanaku-monoliet**.
- 22 nov, over het type: "wat zou goed passen? Want ik wil ook nog een levende tempel/gebouw maken die mogelijk dan ook in aanmerking komt daarvoor". Na het advies van Claude (Baltoy-lijn Rock/Psychic, de tempel een andere typing): "akkoord, baltoy/claydol, moet herkenbaar zijn vanwege de ogen, het silhouet mag veranderen".

## Besloten
- **Rock/Psychic**, beide fases. In de repo is Rock/Psychic vrij zodra Lunatone/Solrock Rock/Cosmic worden.
- **Twee fases: Baltoy → Claydol** (regional forms; blijven Baltoy/Claydol heten?, niet besproken).
- Inspiratie: **Tiwanaku-monoliet** (stenen beelden van Tiwanaku, Bolivia).
- **Herkenbaar aan de ogen** van Baltoy/Claydol; **het silhouet mag veranderen**.
- Levende tempel/gebouw (los idee, IDEEEN.md) krijgt een andere typing dan Rock/Psychic (Claude-advies, akkoord); typing van de tempel nog open.

## Ogen van het origineel (referentie `referenties/baltoy_claydol_gen3_6x.png`)
- Baltoy: twee smalle spleetogen (dicht/turend) in een rode band over het gezicht; daaronder op het lijf een rond oranje "oog" met rode rand.
- Claydol: een ring van ronde rode/oranje ogen rondom de kop (pupil als punt of streep), plus een ring met geel oog op de borst.

## Voorstel Claude (niet van Jordi)
- Kenmerken van een Tiwanaku-monoliet in de prompt: rechthoekig blok, vierkante kop met hoofdband, handen tegen de borst met beker (kero) en staf, ingekerfde motieven op het lijf, benen nauwelijks los.
- Frontaal aanzicht, zoals een beeld (Hoenn tekent Baltoy en Claydol ook frontaal). Andere wens: aanpassen.

## Rondes
- Prompt Baltoy r1: `gemini/PROMPT_baltoy_r1.md` (nieuw gesprek, geen bijlage).
- r1 (`gemini/baltoy_r1.png`, rechthoekig frontaal beeld), Jordi: "dit is geen pokemon sprite, niet driekwart, geen goede vorm en totaal geen baltoy".
- Daarna (meerkeuze): Tiwanaku-deel = "vorm deels" (kop en lijf hoekiger zoals een monoliet, armen en tolpunt blijven Baltoy); geen bijlage, "alleen tekst". Wat er naast de ogen van Baltoy moet blijven: "something else", toelichting gevraagd.
- Toelichting "something else" (Jordi, 22 nov, met een close-up van Baltoys gezicht): "die ronde ogen met een streep erin met het rode patroon erboven". Prompt r2: `gemini/PROMPT_baltoy_r2.md` (driekwart, Baltoy bij naam, armen en tolpunt van Baltoy, kop en lijf hoekiger als monoliet).
- r2 (`gemini/baltoy_r2.png`, rond Baltoy-lijf met gekerfde zigzag-hoofdband, roodbruine steen), Jordi: "nu is die herkenbaar baltoy, alleen klopt de vorm met tiwanaku? plus vertaalt dit naar een sprite". Natief raster ±10,2 px (±80×80). Ruwe maattest 64 en 48 px naast de Gen 3-Baltoy: `maattest/maattest_64_48_gen3baltoy.png` (vertaalt goed; zigzagband wordt bij 48 px ruis).
- Jordi over r2: "dus dan moet de vorm veranderen en dan moet de band robuuster". Prompt r3: `gemini/PROMPT_baltoy_r3.md` (nieuw gesprek; r2-prompt + hoekige Tiwanaku-vorm bovenaan + robuuste band).
- r3 (`gemini/baltoy_r3.png`, vierkante bloklkop met platte top, meanderband, gefacetteerd lijf, grijze steen), Jordi: "hij is nog herkenbaar baltoy, klopt het ontwerp met tiwanaku?"
- Claude over r3: kop en grijze steen kloppen met Tiwanaku; band = Grieks meander, lijf = kristal. Jordi: "ja schrijf r4 met trapmotief en pijlerlijf" → `gemini/PROMPT_baltoy_r4.md`.
- r4 (`gemini/baltoy_r4.png`, vierkante kop met trapband en kruis, rechte pijler met reliëf en punt, beige steen), Jordi: "en nu".
- Claude over r4: Tiwanaku klopt, maar paal/tentharing-gevoel. Jordi: "ja maak hem levendiger, schrijf r5" → `gemini/PROMPT_baltoy_r5.md` (bredere pijler, bijna geen hals, armen schuin omlaag/naar voren: voorstel Claude).
- r5 (`gemini/baltoy_r5.png`, breder blok zonder hals, armen schuin omlaag, chakana getrapt, punt los onder het lijf).

## Model gekozen (22 nov)
- Claude over r5: beter (kop op het lijf, breder, armen schuin omlaag, chakana getrapt); minder: punt los onder het blok, wat robotachtig, rode band dunner. Jordi: "de wat minder dingen zijn niet erg, helemaal omdat de punt in een sprite gefixed kan worden, lijkt die genoeg tiwanaku?" Claude: ja. Jordi: "ga maar bouwen dan".
- **Bevroren model: `referenties/gemini_gekozen_r5.png`** (natief raster ±10,1 px, figuur ±69×71).
- **Toegestane afwijking (benoemde reparatie):** de punt sluit aan op het lijf: het lijf loopt onderaan taps toe naar de punt (zoals in r4), in plaats van een los ruitje onder een plat blok.
- Formaat (voorstel Claude, fase 1): ±48 px hoog, door rijen/kolommen te schrappen zoals Gengas/Alphyena (gezicht en band beschermd).

## Frontsprite
- r1 (maker, schrappen 68×70 → 47×48, punt taps aan het lijf), keurder BIJNA (rechterarm te dun, chakana/vlekjes in de band, schaduw onderaan, rechteroog 1 px te breed, losse rode pixels).
- r2 (maker, 83 px binnen de zones), keuring A BIJNA / eindkeuring Dragonfly Cave B PASS; ter info: 47×48 (±1300 px) is groter dan een gewone fase 1 (700–950 px).
- r3 = r2 + 6 pixels door Claude (zwarte lijn rechtsboven (42–43,16); kinlijn (34–37,38) zwart, (34–37,39) schaduw). Naar Jordi: `sprite_r3/naast_model.png`.
- Jordi over r3: "hij is nog niet mooi" · "onderkant klopt de vorm niet, de band is ook nu al niet mooi, armen zijn niet mooi, hij kan dus prima kleiner. ogen zijn niet rond, hele slordige sprite" · "model is mooier dan r4, dus ondanks dat die dan wat minder tiwanaku wordt is het wel een beter design" (= onderkant zoals het model; de taps-afwijking vervalt).
- r4: verse maker, opnieuw vanaf het model, exacte 2×-reductie (±34×35), ronde ogen (anders Gen 3-Baltoy-oog 1-op-1), band vereenvoudigd op de modelplekken, armen schoon.
- r4A (verse maker, 2×-reductie 34×34): 299 van 642 pixels afwijkend van de kale reductie (band/reliëf "vereenvoudigd" op Claudes opdracht). Jordi: "ik zie dat heel veel opnieuw getekend is" · "niet de bedoeling". r5: basis = kale 2×-reductie (`gereedschap/kaal34`), alleen technische reparaties met bronpixels uit het model.
- r5 (`sprite_r5/`): kaal34 + 48 pixels (47 uit de bronpixels, 1 oogring); punt nog los zoals het model.
