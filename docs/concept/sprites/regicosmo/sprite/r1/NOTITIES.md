# Regicosmo frontsprite, ronde 1 (maker)

Bestanden: `regicosmo_r1.png` (64×64, geïndexeerd, index 0 transparant, 16 kleuren incl. transparant), `kaal.png` (kale reductie), `vel.png` (r1 8× | kaal 8× | model op dezelfde schaal / 1× en 2× op wit, crème, grijs, donker, zwart + model 1× / r1 8× naast Regiaqua af, Regirock en Registeel gba).
Bouwen (vanuit `docs/concept/sprites/regicosmo/`): `python3 sprite/r1/natief.py && python3 sprite/r1/kaal.py && python3 sprite/r1/bouw.py && python3 sprite/r1/vel.py && python3 sprite/r1/controle.py`.
Hulpmiddelen: `zoom.py` (sprite-uitsnede naast het natieve model), `raster.py` (natief model met spriteraster en coördinaten), `pitch.py`.

## Metingen
- Rasterpitch: kam op 11,72 px, maar de kleinste cel is **5,86 px** (trapjes van de Mars-rand, ringen van Saturnus); natief raster 239×130, fase x 4,90 / y 5,20. Figuur natief 130×98 (x60–189, y23–120), 7 losse delen.
- Achtergrond = puur wit (≥ 246) dat met de rand samenhangt (lichte ijspixels bleven anders achtergrond).
- Schaal 62/130 = 0,477. Sprite x1–62, y15–61 (**62×47**), 1392 px, onderkant rij 61, horizontaal gecentreerd. Niet gespiegeld.
- **7 losse delen** (8-samenhang), kleinste tussenruimte: Mars–ijs 2 px, Mars–Saturnus 2 px, Mars–voet blauw 2 px, rest ≥ 4 px.

## Kale reductie (`kaal.py`)
Per natieve pixel het deel (7 hemellichamen) en de dichtstbijzijnde kleur uit het deelpalet (`gemeen.SUB`). Per spritepixel 8×8 subpunten: achtergrond als figuur < 50 %; anders het deel met het grootste aandeel en de kleur met het grootste gewogen aandeel (donkerrood, bruin donker, perzik, zand licht, grijsleisteen ×1,35; stip ×2). Detailtinten winnen vanaf een drempel (zoals "zwart wint vanaf 30 %" bij Dundragoon): Mars kratertjes/donkerrood en donkere band 35 %, asteroïde streep 35 %, maankraters 30 %, ijs cyaan 40 %, blauwe voet licht 35 %, zandvoet licht 40 %. Alle losse pixels die overblijven (Mars-vlekken, kratertjes, maankraters) zijn gemeten modelmeerderheid of -detail (controle per pixel: aandeel van die kleur in de modelcel 0,38–0,94); niets weggepoetst.

## Afwijkend van de kale reductie: 195 px van 1392
- **Mars 90:** stippen 18, buitenlijn 72.
- **ijs 17:** buitenlijn 17.
- **Saturnus 30:** de reductie brak de ring (gaten, ring en planeet door elkaar). Per spritepixel gezet uit de dominante modelkleur per cel (meting in `bouw.py` stap 1, tabel `SAT`), met: buitenlijn (lichtkant donkerrood r / ringdonker b, schaduwkant zwart), zwart binnen → b, hooglicht-beige van de bovenrand → perzik. Gat van de rechterlus (59,27) uit het model; links meet het model geen gat (< ½ px), lus dicht. **Niet uit het model:** (51,34) en (52,34) zwart (model daar 50 % ring/50 % achtergrond) om de onderlijn van de ring dicht te houden.
- **asteroïde 18:** buitenlijn 10, zwart binnen (krater) → bruin donker 8.
- **maan 15, voet blauw 11, voet zand 14:** alleen buitenlijn.
Stappen (`bouw.py`): 1 Saturnus; 2 stippen: kale cyaanpixels in Mars → meest voorkomende Mars-toon in 5×5, dan 7 blokjes 2×2 op de gemeten modelcentra (stippen op één modelrij krijgen één spriterij): linksboven (21,25) (28,25) / (24,30) / (19,36) (29,36) / (23,41) (27,41); 3 px cyaan + 1 lichter linksboven, alle 7 gelijk; 3 buitenlijn 1 px per hemellichaam (gladde normaal per deel; schaduwkant rechts/onder zwart, lichtkant selout); 4 zwart binnen een deel → selout.

## Palet (15 + transparant) en gedeelde tinten
1 zwart (16,16,16) · Mars 2 donkerrood (168,64,48) 3 rood (220,96,68) 4 oranje (240,148,96) 5 perzik (248,192,152) · 6 bruin donker (84,60,50) · 7 bruin midden (120,90,74) · 8 cyaan (120,216,212) · 9 bijna-wit (214,238,246) · 10 asteroïde licht (152,122,106) · 11 lichtgrijs (200,200,204) · 12 leisteen donker (52,64,84) · 13 grijsleisteen (118,126,142) · 14 zand midden (150,126,86) · 15 zand licht (206,182,136).
Gedeeld:
- **Stipkleuren = ijsplaneet** (Jordi: "de braille stippen met de planeet linksboven"): cyaan 8 en bijna-wit 9 zijn de stippen én het ijs (licht 9, schaduwkant cyaan). Daardoor kwam een plek vrij voor een eigen lichte tint van de asteroïde.
- **Mars-tinten in Saturnus:** donkerrood, rood, oranje, perzik (banden en planeetlijn).
- **Bruin donker 6:** donkere band van Mars, asteroïde, ring van Saturnus (donkere rand/selout). **Bruin midden 7:** band van Mars, asteroïde, zandvoet (selout/schaduw).
- **Grijsleisteen 13:** ring van Saturnus, maankraters/-schaduw/-selout, lichte vlakjes blauwe voet, selout ijs. **Leisteen donker 12:** blauwe voet.
- Voeten blijven verschillend (Jordi: "de voeten wel 2 verschillende kleuren"): blauw = 12/13, zand = 14/15 (+ 7).

## Controle (`controle.py`)
64×64, mode P, transparency 0, 16 kleuren; bbox 62×47; 7 losse delen; geen zwart met transparante buur links/boven dat niet ook rechts/onder aan de achtergrond grenst (alleen dunne punten), dus geen zwart/selout om en om op een lichtrand.

## Twijfels
- Saturnus is 15×10 px: de ring loopt door (grijs + donker), maar waar hij vóór de planeet langs gaat wisselt hij grijs/donker zoals het model (zwart-grijs-zwart op ½ px); leest op 1× als geringde planeet, op 8× wat druk.
- Kraters van Mars (ringkraters in het model) worden op 0,477× een donkerrood puntje met lichtere buur; de krater van de asteroïde valt weg (bruin op bruin; zwart binnen mag niet).
- IJs is nu cyaan aan de schaduwkant (gedeelde stipkleur), iets verzadigder dan het lichtblauw van het model.
