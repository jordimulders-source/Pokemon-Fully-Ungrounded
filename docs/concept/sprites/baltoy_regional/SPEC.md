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
- Jordi over r5: "hij is best prima, alleen de lijnen zijn erg hard en dik, het kleurgebruik en schaduwgebruik is nog niet goed, weinig tinten. De lijnen op het lichaam zijn een blur, op het hoofd wel prima. Het hoofd mag 1 pixel langer aan de onderkant, want die lijn kapt af. Hij is wat vierkant dus het is niet erg als je wat meer rechte lijnen dan normaal hebt, maar probeer het smooth te maken waar het kan". → r6.
- r6 (afwerking op r5: hoofd 1 px langer, binnenlijnen bruin, ramp met 5 steentinten, lijfreliëf scherp; 18 vormpixels + nieuwe rij, alles uit de bronpixels).
- Jordi over r6: "het is beter maar een halfbakken oplossing, er moeten meer kleurtinten, meer schaduw, je kan niet rechte lijnen in 1 kleur trekken, dat is niet mooi. Zoek naar andere rechthoekige/vierkante pokemon en kijk hoe die dat doen". → r7 met studie (`sprite_r7/studie.md`).
- r7 (studie vierkante Pokémon `sprite_r7/studie.md`; 10 steentinten, lijnen wisselen van tint, vorm-diff 0); ogen zachter → r8 ogen scherp + keurderpunten r6.
- r8 (ogen scherp, lichte vlakken warm, keurderpunten r6 verwerkt; vorm-diff 0 t.o.v. r6).
- Jordi over r8: "het patroon op het lichaam is ook maar wat halfbakken, daar kunnen we iets meer mee denk ik" · "iets wat op echte tiwanaku monolieten zit, maar goed vertaald naar een sprite, vullend, maar niet teveel detail, het moet er netjes uit zien". → r9 varianten lijfvoorvlak: A handen met kero en staf + gordel, B getrapte gordel + reliëfbanen, C groot chakana/trappaneel (voorstel Claude).
- Keuring r8: A BIJNA / B BIJNA; kleurreparaties (nek, x35-lijn, zijvlak lijf, armen, onderrand) in het rapport van keuring_r8; worden toegepast nadat Jordi een lijfvariant van r9 kiest.
- r9 varianten A/B/C (alleen voorvlak, plat). Jordi: "het werkt allemaal niet omdat je ze niet in het juiste perspectief hebt gezet" → r10: motieven op voor- en zijvlak in driekwart, zoals de hoofdband.
- r10 varianten in driekwart. Jordi: "nu heeft B een mooi patroon. Armen en stekel aan de onderkant lijken alleen nog volledig 2d" → B gekozen; r11: armen en punt 3D.
- r11 (vanaf r10B): armen met doorsnede-schaduw en eindvlak, rechterarm donkerder; punt met voor-/zijvlak en schaduw onder het lijf; nek/ribbe/zijvlak-keurderpunten. Hoofd, band, patroon B diff 0.
- Jordi over r11: "de stekel aan de onderkant leest niet meer als een stekel. Daarnaast mogen de pixels die op een mond lijken weg, voor de rest prima genoeg om naar eindkeuring te gaan, daar fixen we de laatste issues". → r12, dan eindkeuring.
- r12 (stekel terug naar donkere r10B-band onder het lijf + smal uitlopend licht voorvlak; mondpixels weg; 8 px t.o.v. r11) → eindkeuring.
- Eindkeuring r12: BIJNA (geen blokkade); 31 uitvoeringspixels (ruis, lijn-gat, lange 1-tintlijnen, egaal zijvlak kop, omgekeerd verloop onder het lijf) toegepast → r13 (`sprite_r13/`, kandidaat; `r13_vs_r12.png`).
- Jordi over r13: "de stekel onderin klopt niet qua vorm" · "nog steeds niet" · "al 3 keer aangegeven". Stekel versmalt-verbreedt-versmalt (dopvorm) door de 2×-reductie; r14: 3 vormprobeersels (model / zuivere spits / kleine ruit).
- r14 stekelvormen A/B/C (symmetrisch). Jordi: "zucht het is allemaal niet driekwart" → r15: stekel als piramide in driekwart (breed voorvlak links, smal zijvlak rechts, ribbe schuin naar de tip, asymmetrische omtrek), 2 maten.
- Jordi: "maar het idee klopt niet" · "kijk naar het model". Model-stekel = tolpunt: korte smalle hals, donker bovenvlak van bovenaf gezien, breedste rand, kegel met licht voorvlak links en donker rechts tot een platte tip. r15 = exacte vertaling daarvan.
- r15 (maker, 2×) leek nog op r13. r16 (Claude): stekel per laag uit het model opgebouwd (hals, bovenvlak van bovenaf, breedste rand, kegel licht links/donker rechts, platte tip), figuur 2 px omhoog voor ruimte; rest = r13.
- Jordi over r16: "de arm rechts heeft opeens een stuk weggeknipt en de stekel klopt nog steeds niet, het is een 2d vlak wat niet past bij de rest van de sprite, hij moet meer naar verhouding en met netter kleurgebruik, waarom is dit zo moeilijk" · "is dit een vereiste voor de tiwanaku? anders gewoon van de originele baltoy pakken want dit duurt echt lang". r17 = r13 (armen heel) + tolpunt van de Gen 3-Baltoy 1-op-1 (3 rijen), in onze steentinten.
- Stekel 0/1/2 px naar links ter vergelijking (`sprite_r17/stekel_links_vergelijk.png`). Jordi: "ik vind de rest van de sprite wel vrij prima".
- Jordi: "de middelste mag naar de eindkeuring" → r18 = r17 met stekel 1 px links (`sprite_r18/`).
- Eindkeuring r18 (Dragonfly Cave): PASS met 1 pixel ((35,56) 9→10, gat in de onderlijn na het verschuiven) → r19 (`sprite_r19/`, kandidaat).

## Claydol
- r1 (`gemini/claydol_r1.png`, 23 nov; Zonnepoort/Viracocha-figuur: vierkant gezicht, stralenkrans met ronde uiteinden, twee losse staven), Jordi: "Dit is best tof, maar het is totaal nog niet herkenbaar als claydol".
- Jordi: "de ogen wel, maar dat is niet voldoende, het moet denk ik in de hoofdvorm met ogen zitten, als dat kan" → vervolgprompt r2 in hetzelfde gesprek: `gemini/PROMPT_claydol_r2.md` (alleen de kop: Claydol-hoofdvorm met oogring; gezicht in het midden en staven nog open).
- r2 (`gemini/claydol_r2.png`; Claydol-schotelkop met punt en oogring van 5 bleke ogen, stralen, rode verf en kopreliëf weg; lijf en staven van r1), Jordi: "nu wijkt die wel erg af he" · "ondanks dat ik het wel vet gemaakt vind".
- Jordi: "of denk je dat een hybride mogelijk is" → Claude: ja; `gemini/PROMPT_claydol_r3.md` (kop van r2 + stralen die in de ogen eindigen, rode verf en reliëf van r1).
- r3 (`gemini/claydol_r3.png`; ronde kop met 3 grote ogen voor, krans van ±14 kleine oogbolletjes met punt, rode zigzag erboven; schotelrand weg), Jordi: "wat vind je?"
- Claude over r3: rode zigzag goed; schotelrand weg, stralen lezen als bolletjes/bloem, te druk (±17 ogen), voorstel r2 + zigzag + reliëf, stralen weg (of 6–8 echte stralen). Jordi: "zeg het maar" → eerste richting, `gemini/PROMPT_claydol_r4.md`.
- r4 (`gemini/claydol_r4.png`; schotel van r2 terug met rode zigzag; reliëf onder de ogen = doolhof van lijntjes; oog rechts aan de rand weg), Jordi: "en?"
- Jordi over r4: "ik vond de vorige vetter" · "minder kaal hoofd" → **r3 is de basis**. Maattest r3/r4 op 64 px naast de Gen 3-Claydol: `maattest/claydol_r3_r4_64_vs_gen3.png` (krans van r3 blijft leesbaar als bolletjes; zorg van Claude over ruis was overdreven).
- Claude over r3 en Tiwanaku: Zonnepoort/Stafgod klopt (twee staven, stralen met ronde uiteinden), monolietstijl zwakker (golvende zigzag, ronde zachte kop). Jordi: "probeer maar met claydol maar ik vraag me af of die vertalen naar sprite" → `gemini/PROMPT_claydol_r5.md` (getrapte rode lijn, gefacetteerde rand; daarna maattest 64 px).
- r5 (`gemini/claydol_r5.png`; getrapte rode lijn, gefacetteerde kop, reliëf op het gezicht grotendeels weg; derde grote oog half in het facet). Jordi: "nu kloppen alleen de ogen niet meer buiten de 2 naast de neus". Maattest r3/r5 op 64 px: `maattest/claydol_r3_r5_64.png` (getrapte lijn leest goed, facetvlak rechts ook). → `gemini/PROMPT_claydol_r6.md`.
- r6 (`gemini/claydol_r6.png`; krans-ogen nu met een stip i.p.v. een streep, derde grote oog nog half), Jordi: "wordt niet meer beter".
- Overzicht r1–r6 + Gen 3-Claydol: `gemini/claydol_r1_r6_naast_elkaar.png`.
- Jordi (23 nov): "hij is echt herkenbaar claydol, maar ik zit me af te vragen wat we met de ogen doen, bij de echte claydol draaien die om het hele oog heen. Dat staat ons design niet echt toe, tenzij we het gaan aanpassen. Of een hybride variant creëren. Daarnaast valt me op dat alleen het slaperige oog van Claydol is gekopieerd, terwijl hij minstens zoveel wakkere ogen heeft, dus hij heeft streepjes en stipjes ogen, dat kan een sprite maker prima fixen. [...] Op zich is het ook een leuk design om de ogen die als boog om zijn hoofd heen lopen als variatie erop te doen, als we daar de streepjes en puntjes afwisselen. Dan stel ik voor om naar 2 ogen op het hoofd te gaan".
- Claude: eens; 2 ogen op de kop = dezelfde 2 ogen als de regionale Baltoy (rode lijn erboven). r5 ligt daar het dichtst bij (2 ogen + half derde oog in het facet); streepjesogen in de krans uit r5, stipjesogen uit r6 (bronpixels voor beide). Voorstel model: r5, reparaties: derde oog weg (facet egaal), krans streepje/stipje om en om. Wacht op Jordi.
- Jordi: "ik vind 3 het meest net in de afwerking, maar die vertaalt mogelijk minder goed dan 5. 5 mist in het model wel een beetje het ronde perspectief, omdat die niet die afwerking rondom het oog heeft, neus wat rechterhoekiger zoals het tiwanaku model is wel netjes. ik heb veel Claydol modellen bekeken en de ogen wisselen vrijwel altijd om beurten af van . naar - naar ."
- Voorstel Claude: model = r5 (getrapte lijn, hoekige neus, 2 ogen, facet) + de afwerking rond de ogen uit r3 (bronpixels, voor het ronde perspectief); derde oog weg; krans . - . - om en om (stipjes uit r6, streepjes uit r5). Wacht op Jordi.
