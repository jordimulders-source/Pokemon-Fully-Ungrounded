# Studie: hoe Gen 3 zijn onze frontsprites? (24 nov)

Vraag van Jordi (24 nov): "doe eens een studie maken van de sprites die we tot nu toe af hebben, welke het meest lijken op gen 3 sprites en waarom en welke niet · want ik heb het gevoel dat we steeds meer af aan het wijken zijn van de eerder afgesproken werkwijze en ik vind het lastig dat te herstellen".

## Methode
- Alle 85 sprites van het overzichtsvel (`showcase/maak_vel.py`), frame 1, gemeten tegen **385 originele Gen 3-frontsprites** (`graphics/pokemon/*/anim_front_gba.png`).
- Per sprite 9 getallen (kleuren, vlakheid, kleine kleurvlakjes, clustergrootte, dambordpatroon, kleurvariatie per 3×3, helderheid van de buitenlijn, lichtrichting, contrast). Score = gemiddelde afstand tot de Gen 3-mediaan (0 = precies doorsnee Gen 3). **Gen 3 zelf: mediaan 0,92, 90 % onder 1,48.**
- Daarna zelf op 4× naast Mightyena, Gengar, Delibird en Pidgeotto gekeken (`top.png`, `bottom.png`).
- Getallen meten stijl, niet ontwerp of trouw aan het model. Gas- en gloeiwezens scoren altijd hoog (de echte Gastly scoort 3,6).
- Vellen: `alle_op_score.png` (alle 85, van meest naar minst Gen 3), `tabel.tsv` (alle getallen), scripts `meet.py` → `score.py` → `extra.py` → `periode.py` (draaien vanuit een werkmap; paden staan bovenin).

## Uitkomst in één zin
Het grootste verschil is **niet** nieuw: vanaf het begin zijn onze sprites **vlakker** en **rondom zwarter omlijnd** dan Gen 3. Sinds de Gemini-werkwijze (13 nov) is dat **licht erger** geworden: vlakken groter, minder kleine detailpixels.

## De drie meetbare verschillen

| | Gen 3 (mediaan) | Wij (mediaan) |
|---|---|---|
| Zwarte buitenlijn aan de **lichtkant** (linksboven) | 28 % | **55 %** (bij 6 sprites 100 %) |
| Pixels binnenin die in een kleurvlakje van 1–2 px zitten (detail, vachtstreepjes, veertjes) | 19 % | **12 %** |
| Gemiddelde grootte van een kleurvlak | 3,8 px | **5,0 px** |
| Contrast (licht–donker-bereik) | 213 | 197 |

1. **Zwart rondom.** Gen 3 omlijnt aan de lichtkant met een gekleurde, lichtere lijn (selout): Gengars lijn is donkerpaars, Delibirds donkeroranje/grijs. Bij ons is de lijn vaak overal zwart. Onze eigen regel zegt dit al ("zwart alleen aan de schaduwkant, gekleurde selout aan de lichtkant"), maar hij wordt in de praktijk niet toegepast. Rondom zwart (≥ 90 % aan de lichtkant): wingsuit-colugo, Pincurchin, Krickestro, blobfish winegum, Bandolingo, bloedmaan, Krassault, Moonkey, Oricorio tango, fruitvampier, Abra.
2. **Te vlak ("effen").** Gen 3 zit vol kleine detailpixels: haarpieken in Mightyena's vacht, veertjes bij Pidgeotto, losse lichte pixels op de bolling. Een kwart van de pixels in een Gen 3-sprite zit in een vlakje van 1–2 px. Bij ons zijn vlakken groter en gladder, met tinten als banden langs de rand. Dat is dezelfde klacht als "erg effen 2 kleuren" (Coathief, 19 nov) en "pixelblur" (23 nov).
3. **Het model komt mee.** Een Gemini-model is moderne indie-pixelart: cel-shading in grote vlakken, dikke zwarte lijn. "Model overnemen" neemt die stijl 1-op-1 mee. De regel "kleur mag altijd afwijken van het model" (17 nov) wordt te weinig gebruikt om die stijl naar Gen 3 om te zetten.

## Welke lijken het meest op Gen 3 (score ≤ 0,9)
Regionale Rufflet 0,5 · Uyuni-Silicobra 0,6 · Cuychu 0,6 · Princadee 0,6 · Palpaca 0,7 · Hitmongroove 0,8 · pitahaya-draak fase 3 0,8 · Clionice 0,8 · Hauntflare 0,8 · Pupoodle 0,8 · Oricorio samba 0,8 · Axolaunch 0,9 · Flytron 0,9 · Nocticue 0,9 · Kadabra 0,9 · steenjaguar-welp 0,9.

**Waarom:** veel textuur in de vorm zelf (veren, stro, wol, schubben), getekend met kleine streepjes van 1–2 px in plaats van grote vlakken; tinten die de vorm volgen (sikkel); bij Cuychu (20 % zwart aan de lichtkant) en Palpaca/Princadee (±50 %) een lijn die aan de lichtkant lichter wordt. Princadee naast Pidgeotto en Cuychu naast Mightyena lezen als hetzelfde spel.

## Welke wijken het meest af (score ≥ 1,9)
| Sprite | Score | Wat er anders is |
|---|---|---|
| Dustly | 3,6 | geen buitenlijn, zachte vlekken (gas; de echte Gastly scoort ook hoog, dus deels het ontwerp) |
| DJ Rotom | 2,8 | lichtgevende rand, grote effen vlakken, rechte techniek-vormen |
| bloedmaan (Lunatone) | 2,7 | grote egale vlakken, overal zwarte lijn, weinig contrast |
| Cryomet | 2,5 | lichte gloeirand i.p.v. lijn (ijs/gloei; deels ontwerp) |
| Bandolingo | 2,5 | effen bruin in 2–3 banden, zwart rondom |
| Gengas | 2,4 | zachte overloop (pillow) op een grote bol, weinig detail; Gengar heeft harde vlekken |
| Globsnail, Skinguin | 2,2 | grote effen vlakken (Skinguin: zie de kanttekening hieronder) |
| blobfish winegum, Oricorio tango, Wagogogon | 2,1 | effen, weinig contrast; tango en winegum zwart rondom |
| blobfish pudding, Picapau, mate-kalebas, Capybarrel | 2,0 | gladde banden langs de rand, weinig binnendetail |
| Picaraio | 1,9 | grootste effen vlakken van alle vogels |

Voor 30 van de 85 sprites geldt: verder van Gen 3 af dan 90 % van de echte Gen 3-sprites.

**Kanttekening Skinguin (Jordi, 24 nov: "Ik vind Skinguin juist heel erg op een gen 3 sprite lijken").** De score meet textuur, en een gladde pinguïn heeft van nature weinig textuur; ook echte gladde Gen 3-sprites hebben grote vlakken (Pelipper: clustergrootte 5,1, Latias 3,9). Skinguin heeft wel veel Gen 3: helder silhouet, hoog contrast (228, boven de Gen 3-mediaan), Delibird-palet, leest goed op 1× (`skinguin_naast_gen3.png`). Wat de meting wel echt laat zien: het rode lijf is grotendeels twee effen tinten (Delibird heeft meer tintstappen die de bolling tekenen) en de lijn is aan de lichtkant voor 75 % zwart. **Les: de score zegt iets over textuur en lijn, niet over "lijkt het op Gen 3"; bij gladde ontwerpen weegt hij te zwaar.** De lijst hierboven is daarom een lijst om naar te kijken, geen oordeel.

**Kanttekening Dundragoon (Jordi, 24 nov: "dundragoon scoor je ook laag terwijl ik dat echt een gen 3 sprite vind").** Score 1,44: binnen het bereik van echte Gen 3-sprites (90 % zit onder 1,48), alleen plek 53 van 85 omdat onze lijst als geheel scheef is. Lijn aan de lichtkant 51 % (net boven de Gen 3-mediaan), contrast 223 (hoog). Enige afwijking: grotere effen vlakken (6,1 px tegen Dunsparce 4,0), hetzelfde gladde-ontwerp-effect als bij Skinguin; Milotic heeft dat ook (5,2). Vel: `dundragoon_naast_gen3.png`.

**Conclusie na Skinguin en Dundragoon:** de totaalscore en de plek in de rangorde zeggen niet of een sprite op Gen 3 lijkt. Bruikbaar blijven alleen de twee losse metingen (zwart aan de lichtkant, effen vlakken), en die alleen naast een Gen 3-sprite van hetzelfde soort ontwerp (glad naast glad, vacht naast vacht).

## Wijken we steeds meer af?
Ja, licht. Mediaanscore per periode (datums uit Stand van zaken; de git-geschiedenis vóór 22 nov is er niet meer):

| Periode | Aantal | Score | Clustergrootte |
|---|---|---|---|
| t/m 12 nov (handwerk, eerste Gemini) | 17 | 1,12 | 4,9 |
| 13–18 nov (Gemini overnemen) | 24 | 1,26 | 4,9 |
| 19–20 nov (opknapronde + nieuw) | 14 | 1,34 | 5,1 |
| 21–24 nov | 30 | 1,39 | 5,5 |

De opknapronde (19 nov) maakte niet alles Gen 3-iger: Palpaca, Llamauler en Soulibri kregen meer detail, maar Coathief, Picapau en Picaraio werden vlakker en zwarter omlijnd dan hun oude versie (`af/oud_voor_gemini/`, `oud_v1`, `oud_v2`).

## Waar het misgaat in de werkwijze (oorzaken)
1. **Elke ronde toetst trouw aan het model; niemand toetst meer "lijkt het naast een echte Gen 3-sprite uit hetzelfde spel?"** Stap 5 van SPRITE_KERN ("Claude kijkt zelf op 8× naast Taillow") is verdrongen door modeltrouw-keuringen.
2. **De regel "geen tintvlakjes < 3 px" klopt niet met Gen 3**: 19 % van de pixels binnenin een Gen 3-sprite zit juist in zulke vlakjes. Deze regel duwt naar vlak en effen. (Voorstel, zie hieronder; niet zelf aangepast.)
3. **"Rustiger maken" en "ruis weghalen"** halen precies het detail weg dat Gen 3 Gen 3 maakt (Jordi 23 nov al: pixelblur).
4. **Selout staat in de regels maar niet in de checklist met een getal**, dus elke ronde blijft de zwarte lijn van het model staan.

## Voorstellen (Jordi beslist; nog niets aangepast)
- **A. Twee meetgetallen in de eindkeuring**, met de Gen 3-grens erbij: zwart aan de lichtkant ≤ ±50 % (Gen 3: 90 % van de sprites zit eronder) en detailpixels binnenin ≥ ±13 % (Gen 3 p10). Script staat er (`extra.py`); de keurder krijgt het getal, niet alleen zijn oog.
- **B. Regel "geen tintvlakjes < 3 px" vervangen** door: "kleine vlakjes alleen als ze vorm of textuur tekenen (vachtpiek, veer, glans, rand van een sikkel); geen willekeurige ruis". Dat is een designregel, dus alleen na jouw ja.
- **C. Na de modelreductie een vaste "Gen 3-stap"** (alleen kleur, binnen het bevroren silhouet, dus geen hertekenen): lijn aan de lichtkant in de donkerste eigen tint, en de bandjes langs de rand omzetten naar sikkel + textuur zoals de best scorende sprites (Princadee, Rufflet, Cuychu).
- **D. Vaste naastlegger**: elke eindkeuring op 4× naast twee echte Gen 3-sprites van hetzelfde bouwtype (`gen3_ref.png`-stijl), zoals bovenaan dit document.
- **E. Herstel van wat al af is**: niet alles. Kandidaten met de grootste winst voor de minste moeite zijn de sprites waar alleen de lijn zwart rondom is (selout-stap is pure kleur): wingsuit-colugo, Pincurchin, Krickestro, Bandolingo, bloedmaan, Krassault, Moonkey, Oricorio tango, fruitvampier, Abra. Dustly, Cryomet en DJ Rotom wijken grotendeels af door hun ontwerp (gas, gloed, machine) en kunnen blijven.
