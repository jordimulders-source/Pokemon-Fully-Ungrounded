# Poedellarve: kleur r1

Eerste kleurronde op het bevroren silhouet (`../silhouet/silhouet.png`) en het model (`../referenties/model_gekozen.png`).

## Werkwijze
- **Meetgereedschap eerst** (`stappen/`). Gekopieerd van de poedelmot en omgezet naar de schaal van de larve (x0 236, y0 346, 13,55 modelpx per spritepixel, links 12, boven 33): `px.py`, `box1x.py`, `lijnkaart.py`, `ov.py`, `tl.py`, `grid.py`, `meet.py`, `apply.py`. Nieuw zijn:
  - `rgb.py`: gemiddelde modelhelderheid per spritepixel, zonder de groene achtergrond;
  - `klas.py`: meetkaart van de klassen zwart, lijn en helderheid;
  - `kwart.py`: het model op kwart-spritepixels, om dunne lijnen, glans en krullen te plaatsen;
  - `fijn.py`: het model met een raster per spritepixel, naast de sprite.
- **Met de hand getekend** als tekstraster per rij (`stappen/r1.txt` is de eerste versie, `r1b`–`r1f` zijn de eigen reparaties, `r1f.txt` is de eindstand). `bouw.py` zet de tekst om naar `raster.txt` en meldt elke silhouetfout. `zet.py` doet losse pixelwijzigingen. Daarna komen `palet.py`, `controle.py` en `vel.py`.
- **Oog:** het nabije oog is het rechteroog van Eevee (`graphics/pokemon/eevee/anim_front_gba.png`, x 31–33, y 33–37), pixel voor pixel overgenomen. Ik heb de middelste volle rij weggelaten (4 rijen hoog, zoals het model: y 45,5–48,9) en de boven- en onderrij naar rechts verbreed (het model helt). Het oog staat op x 41–43, y 45–48:
  - glans wit op (42,46), op de plek van Eevee; het model zet hem op x 42,75–43,25;
  - grijze reflectie in 3 op (42,47).
- **Verre oog:** (49,45)–(49,47) in zwart tegen de buitenlijn, zoals het model (x 49–50,3, y 45,3–47,2). De glans is één pixel in 7 op (49,46). Het model heeft daar een kleine witte glans; wit leek op 1× op een gat in de buitenlijn.
- **Gemeten plekken** (rgb.py: gemiddelde helderheid):
  - neus (47,48)/(48,48): 45/51;
  - mond: tik (45,49) 170, lijn (46–48,50) 131–168, steeltje (48,49) 157;
  - kinlijn (39,51)/(40,51) 150 en (41,52)/(42,52) 156/144;
  - bovenrand van de voorpoot (43–45,53): 107–125;
  - linkerrand van de bovenste lob van de voorpoot (45,54–57): 120–145;
  - borstrand boven de verre poot (35–38,56): 159–173, p10 ±95; in 3/4 gezet omdat de lijn in het model zwart en dun is;
  - segmentnaden: x19 rij 50–55, x24 rij 50–53, x28 rij 47–51, x32 rij 45–53 (kopcontour), allemaal 150–208. Ze staan in 5/6 en worden taps naar 4/3 in de schaduw.
- **Textuur:** de dambordtextuur onder op de segmenten is niet nagetekend (les poedelmot: raster). In plaats daarvan staan er vlakke schaduwbanden: 7 op rij 55, 6 op rij 56–57 en 4 op rij 58 (model 100–154). De vachtstreepjes op kop en borst zijn weggelaten; het model is daar op spritegrootte vlak wit (225–236).
- **Pootjes:** achterpootjes x 15–17, 22–25 en 28–31 (rij 59–61). De verste (28–31) is donkerder, zoals het model (113–126 tegen 145–169). De ruimte tussen de pootjes staat in 3/4, met de buitenlijn eronder.
  - Verre voorpoot: de bolle onderkant x 33–41, rij 57–62, licht rechtsboven, sikkel linksonder.
  - Nabije voorpoot: twee lobben (rij 53–56 en 58–60) met 3-lijnen ertussen, zoals het model.
- **Belijning:** buitenlijn 2 (donkerbruin; het model is zwart). Aan de lichtkant staat een selout in 3, in 5 aaneengesloten reeksen van 3–8 px: kopbovenrand, bolletjes 1–4 en de bovenrand van de staart. Er wordt nergens om en om gewisseld.

## Controle (`controle_uitvoer.txt`)
- alpha-diff 0 (silhouet niet aangeraakt, ook de sprietkrullen niet);
- open randen 0, losse pixels 0, tintclusters < 3 px 0;
- 10 kleuren + transparant.
- Uitgezonderd als lijnwerk:
  - de sprieten (`spriet_zone.txt`, 1–2 px detail zoals bij de poedelmot);
  - de 1-px-segmentnaden in 5/6 (`naden.txt`);
  - de twee oogglansen.

## Zelfgenoemde zwakke punten
Gerepareerd in r1b–r1f:
- r1 had 97 losse pixels en 123 kleine clusters, omdat ik de metingen te letterlijk per pixel had overgenomen. Ik heb opnieuw getekend met schone banden.
- Pootlijnen en borstrand waren te flauw (4), nu 3.
- Het krulpunt links las als een vlakke top; (37,34) staat nu in 4, zodat de haak met de donkere holte (36,34) leest.
- Er was geen selout; die is toegevoegd.
- Het verre oog had geen glans.

Nog open: ik kan ze binnen de opdracht niet verder oplossen, of ze vragen een keuze.
1. **Kijkrichting:** model en silhouet kijken naar **rechts**; Gen 3-frontsprites kijken naar links-voor (SPRITE_KERN). Ik heb het bevroren silhouet gevolgd. Spiegelen kan zonder hertekenen, maar dan ligt het licht rechtsboven. Dat is een keuze voor de coördinator of Jordi.
2. **Sprietkrullen:** binnen het silhouet lezen de krullen zwakker dan in het model. De haak en de spiraal zijn maar 1–2 px; op 1× lijken de sprieten wat op konijnenoortjes. Het BOX-verkleinde model doet dat ook. Ik heb het silhouet niet aangepast.
3. **Bolletjes 1 en 3:** door het silhouet zijn dat nubjes van 1–2 px breed. Ze lezen als kleine tandjes, niet als ronde pluisbolletjes. De selout verzacht dat.
4. **Buitenlijn:** de selout in 3 aan de lichtkant wijkt licht af van de egale zwarte lijn van het model. Ik heb hem gezet voor de Gen 3-eis; als de keurder de modellijn zwaarder weegt, kan hij terug naar 2 (diff: 23 px).
