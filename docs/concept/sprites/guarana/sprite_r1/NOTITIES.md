# Guaraná fase 1 (Grass/Ghost) frontsprite, ronde 1 (maker)

Bestanden: `guarana_r1.png` (hoofdversie, 64×64, mode P, index 0 transparant, 11 kleuren incl. transparant), `kaal.png` (kale reductie), `r1_zonder_puntjes.png` (variant, voorstel Claude), `r1_ogen_groter.png` (variant), `vel.png` (r1 8× | kaal 8× | model op dezelfde schaal / close-ups 12× tros+ogen, rank+blad, ranken links, ranken rechts, telkens sprite | model / 1× op wit, crème, donker, zwart + model 1×), `varianten.png` (de drie versies naast elkaar, 8× en 1×), `naast_maatstaf.png` (r1 naast Skinguin, Dundragoon, Zapacha, Princadee, Bellsprout, Oddish, Hoppip, Ekans; _gba), `bouw.py`.
Gereedschap `../gereedschap/` (gekopieerd van Dundragoon, aangepast): `pitch.py`, `natief.py`, `klassen.py` (zwart/rood/groen/oogwit per modelpixel), `gemeen.py` (schaal, palet), `ogen.py` (pupil-/oogwitdekking per spritepixel), `vel.py`, `raster.py`, `controle.py`, `zones.py`.
Bouwen: `cd guarana && python3 sprite_r1/bouw.py` (`kaal` = alleen kale reductie); varianten: `VARIANT=zonder_puntjes python3 sprite_r1/bouw.py sprite_r1/r1_zonder_puntjes.png`, `VARIANT=ogen_groter python3 sprite_r1/bouw.py sprite_r1/r1_ogen_groter.png` (draai de hoofdversie als laatste: elke run schrijft `kaal.png`).

## Metingen
- **Rasterpitch:** kam op **10,24 px** (1024/100), fase x 9,25 / y 9,35 (zelfde raster als Dundragoon). Natief 99×99, figuur x14–84, y19–78 (**71×60**).
- Wit dat ingesloten is in de vruchttros = oogwit (het model heeft puur wit oogwit, dat anders als achtergrond telde); ingesloten wit in de krullen = achtergrond (gaten).
- **Schaal 44/71 = 0,620.** Figuur **44×37 (x10–53, y15–51), 809 px**. Niet gespiegeld (model kijkt al naar links), verhoudingen ongewijzigd.
- **Positie:** gemeten in echte Gen 3-sprites (_gba): Bellsprout x10–54 y15–48, Ekans x10–52 y12–51, Hoppip x13–52 y11–53, Oddish x18–46 y16–48 → horizontaal gecentreerd, onderkant op y51 (zoals Ekans). Let op: onze goedgekeurde fakemons staan lager (Zapacha onderkant y62, Princadee y60); dat is alleen een verschuiving als Claude/Jordi dat liever heeft.
- Maat ±810 px zoals Hoppip (811) / Bellsprout (609) / Ekans (984).

## Kale reductie (`kaal.png`)
Oppervlakteweging per spritepixel over het natieve raster: achtergrond als < ½ pixel figuur; **zwart wint vanaf 30 %**; daarna **oogwit vanaf 30 %**; anders de groep (rood/groen) met het grootste oppervlak, tint uit de gemiddelde modelhelderheid (rood L 72/100/140, groen 80/118/145). Silhouet, alle 7 vruchten, de drie ogen, rank met spiraal en gat, blad, vier krullen en de puntjes komen uit deze reductie.

## Palet (index: kleur) = modeltonen
0 transparant · 1 zwart (16,16,16) · rood 2 donker lijn/selout (112,32,32) 3 schaduw (176,56,48) 4 midden (224,80,56) 5 licht (240,136,104) · groen 6 donker lijn/selout (48,72,48) 7 schaduw (96,124,72) 8 midden (122,154,88) 9 licht (150,182,108) · 10 oogwit (248,248,248) · 11 oogwit-schaduw (196,200,204, niet gebruikt na de reductie; vrij).
Gemeten modelgemiddelden per tintvak: rood (119,35,32) (170,54,50) (220,86,59) (241,146,125); groen (54,78,52) (93,120,73) (119,149,87) (137,171,101). Blad = groene groep (het model gebruikt dezelfde groenen). 10 kleuren in gebruik, 5 vrij.

## Pixels die afwijken van de kale reductie (hoofdversie): 205 px, silhouet-diff 0
Per zone (`zones.py`): **vruchttros+ogen 89, rank 50, ranken/krullen 53, blad 13.** Per stap (een pixel kan in twee stappen meetellen):
- **ogen (15 px), uit het model:** per spritepixel de dekking van de modelpupil (zwarte modelpixels binnen het oogwit, natief gemeten in `ogen.py`) en het modeloogwit; pupil ≥ 40 % → zwart, anders oogwit ≥ 40 % → wit. Resultaat: boven oog wit 5×4 met pupil 2×2 (18–19,20–21); rechts wit 5×3 met pupil 3 px (28,22)(27,23)(28,23); onder wit 5×5 met pupil 3 px (17,30)(16,31)(17,31). Geen glanspixel.
- **binnenlijnen (44 px):** zwart dat niet aan de achtergrond grenst (het raster tussen de vruchten, de lijn tros/nek, de lijnen waar krullen over de rank vallen) → donkerste eigen tint (rood 2 / groen 6), op de modelplek. Zwart dat 4-buur is van oogwit blijft zwart (oogcontour zoals het model).
- **buitenlijn (92 px):** geen open/lichte rand; achtergrond rechts/onder → zwart, lichtkant → selout (2/6).
- **lichtkant zwart → selout (20 px):** zwart van het model op de buitenrand met achtergrond alleen boven/links → selout (Gen 3: zwart alleen aan de schaduwkant). Niet aangeraakt: pupillen, oogcontour en de zwarte puntjes aan de vruchtpunten.
- **ontkorrelen (34 px):** tintvlekjes < 3 px (licht < 2) → buurtint van dezelfde groep.
- Geen andere pixels die niet uit het model komen; niets getekend.

## Varianten
- **`r1_zonder_puntjes.png` (voorstel Claude, Jordi kiest):** de negen zwarte puntjes aan de vruchtpunten (natief gemeten: (30,19)(31,19)(22,26)(22,27)(14,38)(24,53)(25,53)(47,30)(48,30)) worden in het natieve model achtergrond, daarna dezelfde pijplijn. Figuur 43×36, 806 px.
- **`r1_ogen_groter.png`:** elk oog = het **nabije oog van Weepinbell** (`graphics/pokemon/weepinbell/anim_front_gba.png`, x26–32 y34–40, 7×7: ooglid in eigen donkere tint linksboven, wit, 2×2 zwarte pupil, zwart rechts/onder), pixel voor pixel; Weepinbells bruine ooglid → ons donkerrood 2. Geplaatst met de pupil op de modelpupil; het rechteroog 1 px naar links zodat het binnen het silhouet blijft. Oude modeloogpixels erbuiten → rood midden. Gekozen omdat het de enige Gen 3-sprite met een rond wit oog met volledig omringde 2×2-pupil op deze maat is (zoekscript over alle `_gba`-sprites; Weepinbell kwam bovenaan; Magnemite heeft een 1-px pupil, Weepinbells verre oog is half dichtgeknepen). 258 px anders dan kaal (vruchttros+ogen 142).

## Controle (`controle.py`)
64×64, mode P, transparency 0, 11 kleuren incl. transparant; per groep ≤ 3 tinten + lijn/selout; geen lichte kleur op de buitenrand. Zwart 20,8 % van de figuur (Bellsprout 19,2, Tangela 16,1, Ekans 14,4, Hoppip 12,9). Eén "losse" zwarte pixel (25,25): oogcontour links-onder van het rechteroog, staat zo in het model. Resterende tintvlekjes < 3 px: groen 7/8/9 in de krullen en het blad (schuine 1-px stroken) en rood 4/5 (18,17)(26,20)(15,32): glanspunten op de vruchten, modelplekken.

## Zwakke punten (eerlijk)
- **Ogen hoofdversie zijn klein** (wit 5×3 tot 5×5, pupil 2–4 px). Op 1× lezen boven- en onderoog als ogen; het **rechteroog leest het zwakst** (smal, pupil tegen de zwarte rand, op 8× bijna een "C"). Daarom de variant met Weepinbell-ogen, die op 1× duidelijk drie starende ogen geeft.
- **Krullen (ranken):** in het model 2–3 natieve px groen met zwarte rand; op 0,62× zijn ze 1–2 px breed en worden vooral lijn (zwart/donkergroen) met weinig groen. De twee kleine krullen onder het lijf lezen als lusjes/"="-vormen, de spiraal van het model is daar weg. Reparatie zou tekenen zijn; niet gedaan. Zwart in de krullen ±40 %, in tros/rank 17–21 %.
- **Tros:** de zwarte rasterlijnen van het model (1 natieve px) vallen deels onder de 30 %-drempel; waar ze wel doorkomen zijn ze nu donkerrood. De vruchten zijn daardoor minder strak gescheiden dan in het model; donkerrood (modelschaduw onder elke vrucht) en binnenlijn hebben dezelfde tint.
- Oogwit-schaduw (index 11) wordt niet gebruikt; het model heeft grijs in het oogwit, maar op deze maat valt dat onder de oogdrempel.
