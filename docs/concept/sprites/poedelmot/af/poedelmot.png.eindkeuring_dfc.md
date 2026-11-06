# Eindkeuring poedelmot kleur r21: Gen 3 + Dragonfly Cave (verse keurder, 6 nov)

Vraag van Jordi: "heeft die de laatste eindkeuring en dragonflycave keuring al gehad? om te kijken of die echt een pokemon is". Ik heb eerst zelf geoordeeld en `poedelmot.png.keuring.md` pas daarna gelezen. Getoetst zijn alleen de twee eisen uit SPRITE_KERN (accuraat t.o.v. het model; een Gen 3-sprite volgens onze eisen). Het ontwerp is niet ter discussie gesteld.

Bron: `referenties/samengesteld.png` (mapping uit `silhouet/sil.py`: x 139–854 → 62 px, offset (1,17)). Sprite `kleur_r21/poedelmot.png`, 64×64, geïndexeerd, 14 kleuren + transparant (index 0), `raster.txt` = png.
Gelezen: SPRITE_KERN, SPRITING §0–8, FAKEMON_DESIGN, FAKEMON_CHECKLIST, en in `bronnen/` de Spriting Guide (Recoloring rules, Revamps/outline shading, Outlining, Shading rounded surfaces, Shine, Textures/fur, Outline shading) en uit *Making Fake Pokémon* "Pokémon Are Simple".

## 8×
- Sprite op 8× met raster (scratch `eindkeur/poedel_8x.png`), uitsneden 12× op donker (`zoom_boven_donker.png`, `zoom_onder_donker.png`), naast het model op 8× (`model_vs_sprite.png`) en een kaart van alle binnenlijnen in 3 (`interne3.png`).
- Pixelmetingen tegen het model: van de 150 binnenlijn-pixels in 3 liggen er 125 op een modelpixel met p15 < 60 (zwart in het model), 24 op 60–120, 1 hoger ((34,53), p15 124, aansluitpixel). De naad op de voorvleugel (y35, x41–51, daarna (52–53,36)) ligt ook in het model recht en zakt aan het eind een rij, net als in de sprite.

## 1×
- Naast Dustox, Venomoth, Beautifly, Masquerain en Altaria op 1× en 3×, op licht (248) en donker (40,40,48) (`naast_1x_licht.png`, `naast_1x_donker.png`, `naast_3x_licht.png`).
- Leest op 1× als één wezen: twee donkere geveerde sprieten als V boven de kop, grote zwarte ogen met glans, witte pluizige romp, twee vleugels in perspectief (verre links kleiner, nabije rechts groot), pluimpootjes onderaan. Op donker geen lichte stipjes rond de rand (geen buiten-AA); op licht geen gat in de omlijning. Lijndikte en contrast in dezelfde familie als de vijf echte sprites; hij oogt lichter, zoals Altaria's wolk.

## Checklist (FAKEMON_CHECKLIST + SPRITE_KERN + SPRITING §0)
| # | Punt | Oordeel | Pixels / meting |
|---|---|---|---|
| §0.1 / B1 | 3/4, kop meer naar de kijker dan het lijf | voldoet | Kop bijna frontaal met verre oog smaller (x16–19 tegen x25–31); lijf/vleugels 3/4: verre vleugel x6–21, nabije x30–62. Insect mag het meest frontaal (checklist). |
| §0.2 / C1 | Alles geteld en verbonden | voldoet | 2 sprieten, 2 ogen, 2 vleugelparen zichtbaar zoals het model, 5 pootjes zoals afbeelding 2; alle klauwtjes omlijnd en aangesloten. |
| §0.3 / A6 | Geen rechte stukken waar het rond is | voldoet | Langste rechte binnenlijn (y35, 11 px) is de vleugelnaad en is in het model ook recht. Buitenomtrek: geen rechte rug/buik > 4 px; rechterrand 60/61/62-wiebel (y19–29, y38–43) volgt de geschulpte vleugelrand van het model. |
| §0.4 / B3 | Ogen geïntegreerd, verre oog geen kopie | voldoet | Rechteroog: glans (27–28,35)+(27,36), olijfreflex B tegenover de glans (28–30,37–38), tan ring. Linkeroog smaller, alleen glans (18,34). DFC-eis "witte glans + gekleurde reflectie" gehaald. |
| §0.5 / A1 | Silhouet leest op 1× | voldoet | Zie 1×. Silhouet = model direct verkleind (alpha-diff 0). |
| §0.6 / D1 | Formaat eindevolutie | voldoet | 1782 px, box 62×45. Ter vergelijking: Dustox 1343, Masquerain 1303, Altaria 1893, Venomoth 2119. |
| §0.7 / C7 | Pose niet stijf | voldoet | Pootjes op 4 hoogtes (klauwtjes y55–61), vleugels ongelijk. |
| A2 | Dominant kenmerk breekt de omtrek | voldoet | De sprieten steken boven en links uit. |
| A5 | Niet symmetrisch | voldoet | Vleugels en sprieten verschillen per kant. |
| B7 | Gezicht compleet | voldoet | Ogen, tan snuit tussen de ogen, kinlijn (19,39)→(28,40). |
| Netheid | ≤ 3 tinten per groep, geen clusters < 3 px | voldoet | controle.py: losse pixels 0, clusters < 3 px 0. Wit A/7/6(D), tan 6/5/4, mauve 8/9, spriet E/C/1. |
| Buitenlijn | 1 px, zwart aan de schaduwkant, selout aan de lichtkant, nooit om en om | voldoet | Rand 181 px: 2 ×120 (vooral rechts: 82 van 92), 3 ×36 (vooral links: 32 van 40), 4 ×15 (selout in 2 reeksen van 7 en 8), 1 ×10 (sprietranden). Enkele afwijkende randpixels zijn aansluitingen van een binnenlijn op de rand ((21,54), (30,57), (58,36)) of de geleidelijke overgang 1→2→3→4 aan de sprietvoet (19,25)–(22,27), precies wat de gids voorschrijft. Geen 1/2 of 2/3 om en om. |
| Binnenlijnen | Alleen waar vorm over vorm valt, donkere vlaktint | voldoet | 3 (96,72,56) is lichter dan het zwart van het model op die plekken; alle lijnen scheiden een pluim/plaat/vleugel van wat erachter ligt. |
| E1 | Verre kant donkerder | voldoet | Verre vleugel krijgt de tanband y30–34 en de slagschaduw van de spriet. |
| E3 | Donkerte-aandeel | wijkt af (R) | 0,33 (< 80 lum) tegen 0,04–0,26 bij de vijf; komt door de zwartbruine sprieten (E+1 = 238 px) die het model voorschrijft. Zonder sprieten ±0,20. Richtlijn, geen afkeur. |

## Dragonfly Cave-punten
- **Silhouet en leesbaarheid op 1×:** goed; leest als één Pokémon, niet als losse delen.
- **Outline/selout:** volgens de gids: zwart(bruin) rond de schaduwkant, donkerbruin 3 en bruin 4 als omlijningsbasis/hooglicht aan de lichtkant (linksboven), 1 px, geen klonten. Regel 4 van recoloring ("outlines reasonably dark" bij een lichte sprite) gehaald: ook de selout 4 (152,120,104) is duidelijk donkerder dan het wit.
- **Shading en lichtrichting:** licht linksboven. Linkerkant van romp en kop wit tot aan de lijn; schaduw (7/6) rechtsonder op de romp, onder de kraag en op de pluimen; slagschaduw van de linkerspriet op de verre vleugel. Consistent.
- **Kleurgebruik/palet:** 14 kleuren, per groep één toon (warm wit/crème/tan, mauve plaatjes in dezelfde warme familie); veel hooglicht zoals R/S-stijl, dus niet te donker. Geen neon, geen verlopen.
- **Anti-aliasing:** alleen binnen de lijn; buitenkant schoon (gecontroleerd op donker).
- **Banding:** niet gezien als fout. De crème/tan-stroken onder de linkerspriet (y30–31) zijn de slagschaduw uit het model, geen tinten parallel aan de buitenrand.
- **Pillow shading:** nee; de lichte kant loopt licht door tot de omlijning.
- **Jaggies:** geen spijkertjes of besluiteloze curven in kop, ogen en sprieten. De 1-px-wiebel aan de rechtervleugelrand volgt de geschulpte rand van het model (silhouet bevroren).
- **Detail op schaal ("Pokémon are simple"):** de sprietbaarden zijn als regelmatige C/E-strepen samengevat, de vleugelkrullen als enkele vlakken. Geen detail dat op 1× ruis wordt, behalve dat de pluimen onderaan druk zijn (zie ter info).
- **Textuur (vacht):** de grenzen wit/crème zijn kort en gekarteld met streepjes in haarrichting op de kraag; volgens de gids "niet overdrijven", dat is hier gehaald.
- **Ontwerp als Pokémon / eindevolutie:** groot, vol en met twee opvallende kenmerken (sprieten, ogen); past naast Dustox/Venomoth als eindvorm van een tweestaps-insectenlijn.

## Reparaties (alleen uitvoering)
Geen verplichte. Optioneel, niet nodig voor PASS:
- (58,36) staat in 3 tussen 2's op de schaduwkant; mag 2 worden als de naad daar niet tot de rand hoeft (model p15 1, dus 2 klopt ook met het model). Is op 1× niet te zien.

## Ter info voor Jordi (geen FAIL, ontwerp)
- Het onderlijf is een net van donkere lijnen rond elke pluim en plaat (150 binnenlijnpixels). Dat staat zo in het model (125 van de 150 op zwart in het model) en is dus goed vertaald, maar op 3× leest het onderlijf wat als losse kiezels en is het het drukste deel van de sprite. Wil je het rustiger, dan is dat een keuze in het model (minder of zachtere scheidingen), niet in de uitvoering.
- Het donkerte-aandeel ligt boven de Gen 3-band door de zwartbruine sprieten; dat geeft hem juist zijn kenmerk.

Oordeel: PASS
