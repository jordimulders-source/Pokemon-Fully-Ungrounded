# Nachtaap fase 1, ronde 3: afwerking naar echte Pokémon-sprites

Jordi over ronde 2: "nachtaap is echt een enorme verbetering, moet nu alleen meer lijken op de al bestaande Pokémon-sprites qua kleuren, shading, belijning etc." Hij was het ook eens met de zwakke punten die ik zelf had genoemd: de handen lezen als een driehoekje, de halfdichte ogen lezen slaperig, hij is groot naast Abra en Espurr, en het lijf is generiek. Het ontwerp, de pose en het concept bleven gelijk; deze ronde gaat over de afwerking.

Bestanden:
- `anim_front.png`: 64×128, geïndexeerd, index 0 transparant.
- `normal.pal`
- `thumbnails.png`: tussenstappen van deze ronde (A, B en C).
- `compare.png`: ronde 1, 2 en 3 naast Abra, Espurr, Munna, Elgyem, Hatenna, Natu, Ralts, Spoink en de Hoenn-starters, op 3× en 1×, met de silhouettest.
- `bron/build.py`: maakt de sprite (`python3 bron/build.py .`).
- `bron/compose.py`: maakt het vel (`python3 bron/compose.py .`).

`thumbnails.png` is samengesteld uit voorbeeldbeelden van de tussenstappen. Alleen C (de gekozen versie) is uit de bron te maken.

## Wat ik van de echte sprites heb overgenomen (pixel voor pixel vergeleken)
Ik heb Abra (GBA), Espurr, Munna, Elgyem, Ralts (GBA) en Natu (GBA) op 6× bekeken, plus de paletten van Espeon, Whismur, Grumpig, Wynaut en Spoink.
- **Kleuren:** Game Freak-lavendel heeft meer kleur dan mijn pastel van ronde 2, met een schaduw die naar violet/blauw schuift (Espeon `#d5ace6/#b473e6/#7b52b4/#52396a`, Espurr `#b0b8d8/#9898b8/#706890`). De vacht is nu `#e6cdf6 / #b49cde / #8373bd / #4a396a`. Het zilver is Ralts-wit (`#f6f6ff/#cdcde6/#9ca4c5`, blauwgrijze schaduw), het accent Whismur-roze (`#ffa4d5/#e65aa4/#9c2962`). De ogen zijn diep nachtblauw met cyaan gloed (`#293973`, `#62c5de`, `#eeffff`) in plaats van pastel-cyaan.
- **Schaduw:** Abra heeft schaduw als **vlakken met een vaste breedte** langs de onder-/rechterkant (de rechterkant van de kop, onder de armen), plus een klein hooglicht linksboven. Ronde 2 maakte elliptische verlopen. Nu krijgt elke vorm een schaduwband ter breedte van een vaste verschuiving: 4 px op de kop, 3 px op het lijf, 1–2 px op armen, oren en staart. Daarbij komt een slagschaduw van 2 px onder voorliggende vormen (onder de kin en de armen) en per vorm een klein hooglichtvlekje.
- **Belijning:** dezelfde regels als bij Abra en Ralts. Aan de bovenkant loopt de schaduwtint als lijn, aan de linkerkant de donkerste tint, aan de onder- en rechterkant zwart. Binnenlijnen (kop over lijf, armen) zijn de donkerste tint, alleen aan de schaduwkant zwart. Zwart zit verder alleen in de ogen, rond de parel en tussen de vingers.
- **Ogen in weinig pixels:** Game Freak tekent glans als één vorm, niet als verloop. Hier is dat een maansikkel van 5 px linksboven in elk oog, met een kleine gloed rechtsonder. Ik heb de ogen met de hand gezet.

## Opgeloste punten
- **"Slaperig" → mysterieus:** er zijn geen halfdichte oogleden meer. Frame 1 heeft grote, donkere nachtogen (zoals de echte nachtaap) zonder zichtbare pupil, met een **maansikkel als weerspiegeling**. Je ziet niet waar hij kijkt en het maanmotief zit letterlijk in de blik. Frame 2 laat de ogen opengaan als twee gloeiende manen met een pupil. Lege lichte schijven (variant A) leken op een bril, dus die heb ik laten vallen.
- **Handen:** de driehoek is weg. Hij houdt nu een **kleine gloeiende maanparel** voor zijn buik, met magenta vingertoppen aan weerszijden. Op 1× lees je meteen "houdt iets magisch vast" (zoals de parel van Spoink en de lepels van Abra). Het is ook het zaadje van de genezer: zijn licht, later misschien een lantaarn of maansteen. In frame 2 houdt één hand de parel en zegent de andere.
- **Kleiner:** hij was 46×52 met 1441 px oppervlak en is nu 42×48 met 1248 px. De kop is kleiner (14×11,5 in plaats van 15,5×12,5) en de spiraal ook (straal 9,6 in plaats van 10,5).
- **Lijf minder generiek:** het zitkussen (de gevouwen benen) ligt nu áchter het lijf. Daardoor lees je dijen links en rechts, geen emmer. De parel geeft de buik een middelpunt. Een zilveren kraag of slab met schulpen heb ik geprobeerd (A, B), maar dat werd een emmerrand of een "schermpje" en maakte het geheel te druk.

## Paletindeling (recept-formaat)
```
'nachtaap': {'vacht': [1, 2, 3, 4], 'zilver': [5, 6, 7], 'magenta': [8, 9, 10], 'ogen': [11, 12, 13], 'wit': [14],
             '_base': {'vacht': 2}}
```
| index | kleur | onderdeel |
|---|---|---|
| 0 | #94cd9c | transparant |
| 1–4 | #e6cdf6 #b49cde #8373bd #4a396a | vacht (2 basis; 3 schaduw en bovenlijn; 4 linkerlijn/binnenlijnen) |
| 5–7 | #f6f6ff #cdcde6 #9ca4c5 | zilver: sikkels boven de ogen, snuit |
| 8–10 | #ffa4d5 #e65aa4 #9c2962 | magenta: edelsteen, oren, neus, vingertoppen, staartpunt |
| 11–13 | #eeffff #62c5de #293973 | ogen + maanparel (maansikkel, gloed, nacht) |
| 14 | #ffffff | glans (parel; in frame 2 ook in de ogen) |
| 15 | #101010 | omlijning, pupillen |

Gebruik in frame 1 (index 1..15): 26 / 271 / 342 / 132 · 38 / 28 / 18 · 9 / 17 / 6 · 22 / 24 / 65 · 1 · 249.
De schaduwtint 3 is vaker dan de basis 2, omdat de bovenlijn en de schaduwvlakken samen groot zijn. Het recept heeft daarom `'_base': {'vacht': 2}` nodig. De parel deelt de groep "ogen". Dat is bewust: in elke variant hebben ogen en parel dezelfde gloed.

## check.py (`--stage 1`)
```
LET OP  geen back.png
LET OP  geen icon.png
OK      hoogte (px)                  42  (Hoenn fase 1 p10..p90: 30..58, mediaan 40)
OK      breedte (px)                 48  (Hoenn fase 1 p10..p90: 29..61, mediaan 42)
OK      oppervlak (px)               1248  (Hoenn fase 1 p10..p90: 527..1674, mediaan 912)
OK      kleuren gebruikt             15  (Hoenn fase 1 p10..p90: 10..15, mediaan 13)
OK      rand: aandeel zwart          0.554  (Hoenn fase 1 p10..p90: 0.235..0.578, mediaan 0.403)
OK      rand linksboven: helderheid  0.341  (Hoenn fase 1 p10..p90: 0.262..0.533, mediaan 0.38)
OK      rand rechtsonder: helderheid 0.136  (Hoenn fase 1 p10..p90: 0.059..0.296, mediaan 0.151)
OK      licht links(-)/rechts(+)     -0.053  (Hoenn fase 1 p10..p90: -0.424..0.154, mediaan -0.134)
OK      licht boven(-)/onder(+)      -0.191  (Hoenn fase 1 p10..p90: -0.531..0.1, mediaan -0.193)
OK      aandeel schaduwtinten        0.527  (Hoenn fase 1 p10..p90: 0.157..0.597, mediaan 0.404)
OK      dithering (schaakbord)       0.0304  (Hoenn fase 1 p10..p90: 0.0153..0.0936, mediaan 0.0461)
OK      losse pixels                 3  (Hoenn fase 1 p10..p90: 1..26, mediaan 8)
OK      binnenlijnen zwart           0.098  (Hoenn fase 1 p10..p90: 0.01..0.113, mediaan 0.033)
OK      verschil frame 1-2           0.342  (Hoenn fase 1 p10..p90: 0.282..0.792, mediaan 0.618)
species_info: .frontPicSize = MON_COORDS_SIZE(56, 48), .frontPicYOffset = 6
```
De eerste versie van deze ronde had de donkerste tint als lijn rondom boven/links. Dat gaf een LET OP (rand linksboven 0,21, te donker) en daarom loopt de bovenlijn nu in de schaduwtint.

## Checklist (verschillen met ronde 2)
- Type: gloeiende nachtogen met een maansikkel, voorhoofdteken, meditatiehouding, spiraal, maanparel, lavendel/magenta. Dat is nu een middel meer (de parel).
- Basisvorm en één onrealistisch kenmerk (de spiraal): ongewijzigd. De parel is een voorwerp, geen tweede lichaamskenmerk.
- Silhouet: ongewijzigd herkenbaar en compacter.
- Gespriet: vlakke schaduwvlakken, geen verlopen. Dithering 3% (alleen waar vormen samenkomen).

## Nog niet goed
- **Frame 2-ogen:** de wijd open ogen met pupil kunnen op 3× wat "verbaasd" of googly lezen in plaats van "schrikmoment". Een kleinere pupil van 1 px met een gloeirand zou intenser zijn, maar valt op 1× misschien weg.
- **Zilveren sikkels boven de ogen:** ze zijn groot en wit, en daardoor de lichtste vlek van de sprite. Ze kunnen een tint donkerder (index 6 als hoofdkleur) als ze te veel aandacht trekken.
- **Binnenlijnen:** aan het eind van de armen en onder het lijf zitten nog wat zwarte binnenlijnen (aandeel 0,098, binnen de spreiding maar hoog). Abra gebruikt daar de donkerste tint.
- Nog geen back, icoon en proefvarianten (albino/zwart).
