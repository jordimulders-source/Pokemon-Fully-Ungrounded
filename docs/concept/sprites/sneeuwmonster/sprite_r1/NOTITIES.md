# Sneeuwmonster fase 1 (Ice) frontsprite, ronde 1 (kandidaat)

Bestanden: `sneeuwmonster_r1.png` (64×64, mode P, index 0 transparant, 9 kleuren incl. transparant), `kaal.png` (kale reductie), `mond_shroomish.png` en `mond_chinchou.png` (mondvarianten, alleen de mondpixels anders), `vel.png` (r1 8× | kaal 8× | model op dezelfde schaal / close-ups kop en lijf 12× naast het model / 1× op wit, crème, donker, zwart + model 1× + beide mondvarianten 1× / mondvarianten 8× naast elkaar), `bouw.py` (sprite + kaal + monden), `maakvel.py`.
Gereedschap (`../gereedschap/`, gekopieerd van Dundragoon en aangepast): `pitch.py`, `natief.py` (→ `natief.png`), `klassen.py` (zwart / steen / blauwe sneeuwlijn / sneeuw per modelpixel; achtergrond = wit verbonden met de rand, zodat wit hooglicht binnen de figuur sneeuw blijft), `gemeen.py` (schaal, palet, overlap), `vel.py`, `raster.py`, `controle.py`, `zones.py`.
Bouwen: `cd sneeuwmonster && python3 sprite_r1/bouw.py && python3 sprite_r1/maakvel.py` (`bouw.py kaal` toont alleen de kale reductie).

## Metingen
- **Rasterpitch:** één duidelijke kam op **10,24 px** (x fase 9,05, y fase 9,25). Natief raster 99×99; figuur x27–70, y16–81 = **44×66**, 2054 px.
- **Gen 3 fase 1-soorten (`anim_front_gba.png`, b×h / px):** Snorunt 35×41 / 856, Wynaut 35×40 / 819, Azurill 39×37 / 850, Spheal 39×33 / 890, Marill 42×35 / 866, Shuppet 31×39 / 704, Teddiursa 28×36 / 652, Smoochum 24×36 / 597, Swinub 26×22 / 482 (Glalie ter vergelijking 49×45 / 1470).
- **Schaal: 42/66 = 0,636** (1,57 natieve px per spritepixel), verhoudingen ongewijzigd, niet gespiegeld. Figuur **x18–45, y11–52 (28×42), 829 px**: hoogte en oppervlak tussen Snorunt (41 / 856) en Wynaut (40 / 819), de rechtopstaande fase 1-soorten van hetzelfde bouwtype; smaller omdat het model een smalle peervorm is (b:h = 2:3). Voeten op y52 zoals Snorunt/Wynaut (onderkant y51–52).

## Wat uit het model komt (kale reductie, `kaal.png`)
Oppervlakteweging per spritepixel over het natieve raster: achtergrond als < ½ pixel figuur; **zwart wint** vanaf 30 %, **steen** (grijs) vanaf 40 %, **blauwe sneeuwlijn** vanaf 30 %; anders sneeuw met de tint uit de gemiddelde modelhelderheid (< 212 schaduw, < 236 midden, anders licht; steen < 72 donker, < 108 midden, anders licht).
Silhouet, sneeuwpluk met drie bolletjes en de lijntjes ertussen, beide ogen, de twee knopen, beide armstompjes (links tegen de rand, rechts als boog in het lijf), de schaduwsikkels (rechts en onder op kop en lijf, de schaduw onder de kop), beide voetjes en de lijn tussen de voetjes komen allemaal uit deze reductie. De buitenlijn van het model is zelf al Gen 3 (blauwe lijn links/boven, zwart rechts/onder) en is zo overgenomen.

## Pixels die afwijken van de kale reductie: 76 px (silhouet-diff 0)
Per zone (`zones.py`): **sneeuwpluk 12, kop 13, ogen 14, lijf+armpjes 22, knopen 3, voetjes 12.** Per stap:
- **buitenlijn (23 px):** geen open of lichte rand; achtergrond rechts/onder → zwart, lichtkant → sneeuwlijn (selout). Zwart uit het model blijft zwart.
- **ontkorrelen (47 px):** sneeuwtintvlekjes < 3 px (licht < 2) nemen de buurtint van de sneeuw aan (o.a. de 1-px middenkolom langs de schaduwgrens rechts op de kop, (37–38, 20–26) → schaduw); lijnen en steen niet aangeraakt.
- **ogen (4 px), naar het model:** het witte modelhooglicht viel in het gemiddelde weg (twee grijze blokjes zonder glans). Opnieuw uit het model: oogpixel = donkere modeldekking ≥ 40 %, tint uit de modelhelderheid (< 35 zwart, < 72 steen donker, anders steen midden); glans = zwaartepunt van het witte modelhooglicht in het oog, gemapt naar de dichtstbijzijnde pixel met ≥ 2 oogburen: links (23,23), rechts (31,24). Linkeroog 2×3 + glans linksboven, rechteroog 3×4 met glans linksboven-midden, zoals het model.
- **buitenlijn om en om (4 px):** losse sneeuwlijnpixels op de rand tussen zwart → zwart ((22,29) links bij de hals, (21,45) links onder, (35,13)/(36,13) bovenop het rechterbolletje van de pluk).
- **Geen pixel die niet uit het model of uit een technische regel komt;** niets met de hand getekend.

## Palet (index: kleur)
0 transparant (152,208,160) · 1 omlijning (24,32,56) · sneeuw 2 lijn/selout (88,124,164) 3 schaduw (172,200,228) 4 midden (214,232,246) 5 licht (244,250,255) · steen 6 donker (48,50,60) 7 midden (86,88,102) 8 licht (130,132,146).
Modeltonen (gemeten): zwart 5,10,27 · sneeuwlijn 97,132,158 · schaduw 181,205,227 · midden 205,224,236 · licht 236,245,248 · steen 78,82,92 (vulling ±127). Stappen licht→midden→schaduw→lijn ±30/±42/±75 (helderheid), vergelijkbaar met Glalie (255/230/205/164). 8 kleuren, dus 7 vrij. Knopen blijven koud donkergrijs.

## Mondvarianten (het model heeft geen mond; apart)
Mondpixels 1-op-1 uit een Gen 3-sprite (`_gba`), alleen herkleurd; plek in beide: midden tussen de oogmiddens (x27), direct onder het laagste oog (y27). Pixeldiff t.o.v. r1:
- **`mond_shroomish.png`** (bron Shroomish: (28,30) tint 3 · (29,30) tint 2 · (30,30) tint 3 op huid 4, direct onder de ogen): (26,27) licht→midden, (27,27) licht→schaduw, (28,27) licht→midden. Klein zacht mondje met donkerder midden; tinten = dezelfde stappen onder de gezichtstint.
- **`mond_chinchou.png`** (bron Chinchou: (31,36) en (31,37) donkerrood op huid 4): (27,27) en (27,28) licht→sneeuwlijn. Klein verticaal mondje (2 px). Let op: bij Chinchou ligt de mond op de hoogte van de onderkant van de (grote) ogen; hier direct onder de ogen, zelfde regel als Shroomish.
- Bekeken en afgevallen: Castform (2 px horizontaal = rechte streep), Igglybuff en Jigglypuff (zwarte bovenrand met rood = open mondje), Clefairy/Cleffa/Hoppip/Togepi/Pichu (glimlach), Sunkern (lijn).

## Controle (`controle.py`)
- 64×64, mode P, transparency 0, 9 kleuren incl. transparant; sneeuw 3 tinten + lijn, steen 3 tinten.
- Geen lichte kleur op de buitenrand; geen losse zwarte pixels; zwart 11,2 % van de figuur.
- Vlekjes < 3 px die over zijn: sneeuwlijn 8× (lijnstukjes uit het model: pluklijnen, oogrand boven het linkeroog (23,22), armlijn, voetlijn), steen 15× (ogen en knopen zijn kleine vormen), wit (31,24) = glans, wit (20,36) en midden (19,38) in het linkerarmpje tussen de modellijnen, schaduw (43,35) tussen armlijn en buitenlijn rechts: allemaal modelplekken.

## Resterende twijfels (eerlijk)
- **Volume:** het model is in feite tweetonig (sneeuw 243 / schaduw 200 met smalle overgangen); de sprite neemt dat over. Kop en buik zijn grote, vrijwel effen lichte vlakken met alleen een sikkel rechts/onder. Meer Gen 3-volume (bv. een tweede schaduwtint als kern van de sikkel of een hooglicht op de bolling) staat niet in de modelhelderheid en is dus niet toegevoegd; is dat gewenst, dan is het een keuze voor Claude/Jordi.
- **Linkeroog:** de glans zit, zoals in het model, linksboven en raakt het witte gezicht; op 8× leest het linkeroog daardoor als een donker 2×3-vormpje met een hoekje eruit, niet als oog met glans. Op 1× leest het als oog. SPRITE_KERN zegt (vuurduivel) "witte pixel in een onderhoek, niet linksboven"; hier volgt de glans het model. Rechteroog: glans linksboven-midden, binnen het oog.
- **Knopen** zijn op deze maat 4×5 rondjes met kale hoeken (bovenste knoop iets ruitvormig door 1 pixel bovenop, (26,34)); in het model ronde schijfjes.
- **Sneeuwpluk:** drie bolletjes lezen, maar de lijntjes ertussen zijn op 1,57× verkleining losse 1-2 px stukjes; het rechterbolletje heeft na de om-en-om-regel een zwarte bovenrand (in het model blauw).
- Mondplek is een eigen keuze (regel: midden tussen de ogen, direct onder het laagste oog); de mondpixels zelf komen uit de bron.
