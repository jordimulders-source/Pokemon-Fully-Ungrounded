# Onweerswolk-Altaria (Electric/Dragon) frontsprite, ronde 1 (kandidaat)

Bestanden: `altaria_r1.png` (64×64, geïndexeerd, index 0 transparant, 10 kleuren incl. transparant gebruikt), `altaria_r1_8x.png` (8× op wit), `kaal.png` (kale reductie), `vel.png` (r1 8× | model op dezelfde schaal 8× / close-ups 12× kop+kuif en linkervleugel, steeds sprite | model / 1× op wit, crème, donker, zwart + model 1×), `bouw.py`.
Gereedschap: `../gereedschap/` (kopie van `swablu_regional/gereedschap/`, aangepast; het Swablu-gereedschap is niet aangeraakt): `pitch.py`, `natief.py` (→ `natief.png`), `klassen.py` (modelpixels indelen + `statisch()`), `gemeen.py` (schaal, palet, blokken), `frac.py`, `raster.py`, `vel.py`, `controle.py`, `zones.py`.
Bouwen: `cd swablu_regional/altaria && python3 gereedschap/natief.py && python3 sprite_r1/bouw.py && python3 gereedschap/vel.py sprite_r1/altaria_r1.png sprite_r1/vel.png`.

## Metingen
- **Rasterpitch:** kammen op 15,36 en 10,24 (3:2) → gemeenschappelijke cel **5,12 px** (1024/200), fase 4,10 in x en y. Natief raster 199×199; figuur x15–188, y14–174 (**174×161**, incl. de static-stukjes buiten de wolk).
- **Formaat:** game-Altaria (bovenste frame) x4–61, y0–62, **1778 px**. Schaal **precies 1/3** (gehele 3×3-blokken, geen halve pixels): figuur **x3–61, y9–62, 1820 px** (58×54). Onderkant op y62 zoals de game-Altaria, breedte vrijwel gelijk (59 tegen 58). Blokfase (u≡1, v≡2 mod 3) gekozen op de kleinste kleurspreiding binnen de blokken. Verhoudingen van het model ongewijzigd, niet gespiegeld.

## Klassen in het model (alleen indelen, niets tekenen)
Achtergrond = bijna-wit verbonden met de rand, plus het ingesloten pure wit tussen kop en kuifstrengen (min ≥ 240). Zwart = L < 30. Violet = B−G ≥ 45 (kop, hals, kuif); de blauwgrijze randpixels van de kuifstrengen (binnen 2 px van violet, boven de vleugels) tellen als violet. Lichte pixels (L ≥ 203): cyaanwit (G−R ≥ 18) = static, anders lavendelwit (kuiflicht, oogglans). **Static** (`klassen.statisch`): cyaanwit + dunne lichte lijntjes (1–2 natieve px breed, beide kanten ≥ 35 donkerder, cyaan); niet in kop/snavel/wang; stukjes < 3 natieve px weg. De overlay hiervan valt samen met alle static-lijnen van het model, ook de stukjes buiten de wolk links (natief x15–24, y55–72) en rechts (x185–188, y56–67).

## Kale reductie (tegen het "blurry" van Swablu r1)
Eerst elke natieve pixel naar de dichtstbijzijnde paletkleur van zijn eigen klasse (geen mengkleuren), dan per 3×3-blok: static wint vanaf 2/9 (dun lijntje); achtergrond onder 5/9 figuur; zwart vanaf 3/9; anders wolk of violet naar het grootste aandeel, tint = de paletkleur die het dichtst bij het blokgemiddelde van die groep ligt (alleen modeltinten, 4 harde wolktonen, geen tussentinten). Kuif apart: kuif vanaf 5/9 figuur, zwart vanaf 4/9, anders de meest voorkomende violettint (de klassenregels maakten er klonten en zwarte stukken van).

## Pixels die afwijken van de kale reductie: 277 px, **0 px getekend**
Per zone (`zones.py`): **kuif 32, kop+oog+snavel 11, hals 15, vleugel links 52, vleugel rechts 59, wolk midden 65, shelf cloud onder 43.** Per stap (overlap mogelijk):
- static kort (19): static-stukjes van 1–2 px (8-buren) → buurtint; die gaven streepjesruis. Over: 10 lijnen van 4–35 px, alle op modelplekken.
- ontkorrelen (143): tintvlekjes < 4 px (4-buren) → meest voorkomende buurtint van dezelfde groep (lijnen, static niet). Dit maakt de bollen tot grote tintvlakken.
- uitsteeksels (40): tintpixel met hoogstens 1 gelijke buur en 3–4 buren in één andere tint van de groep → die tint (rondere bolranden, geen trapjeskorrel).
- losse zwarte pixels (1): zwart zonder zwarte buur midden in een vlak → buurtint. Ogen uitgezonderd.
- buitenlijn (124): geen open of lichte rand: achtergrond rechts/onder → zwart; lichtkant → selout (wolk donker (28,50,81), violet donker). Kuif: geen zwart (strengen zijn 1–2 px; anders wordt de hele streng zwart), licht violet aan de rand → midden, behalve aan de lichtkant (boven/links) van een streng die eronder/rechts donkerder doorloopt; midden → donker aan de schaduwkant van een 2 px dikke streng.
- Ogen: (23,21) en (27,21) zwart, precies op de gemeten modelovalen (natief x72–75 en x85–87, y50–53; `frac.py`: K4 en K6). Geen glans: de modelglans is < 1 spritepixel (l1/l2).
- Snavel en wang komen ongewijzigd uit de reductie: snavel x22–26 (zwarte linker- en onderrand, teal), wang (28–29,23) teal met hooglicht.

## Palet (index: kleur) = k-means-centra van de modelpixels per klasse
0 transparant · 1 zwart (6,12,28) · wolk 2 donker/selout (28,50,81) L46, 3 midden (50,83,116) L76, 4 licht (89,139,170) L127, 5 hooglicht (144,202,221) L186 · violet 6 donker (56,61,139) L68, 7 midden (94,98,207) L109, 8 licht (141,145,237) L154 · 9 lavendelwit (236,240,251) (in het palet, niet gebruikt) · 10 static (188,224,237) L214.
Helderheidsstappen wolk 30/51/59, violet 41/45: duidelijk contrast. Snavel en wang gebruiken de wolktinten (zoals in het model).

## Controle (`controle.py`)
- 10 kleuren incl. transparant; index 0 transparant; geïndexeerd. Wolk 4 tinten (donker werkt als selout/schaduwrand, zoals de onderwolk-plus-bollen bij Swablu), violet 3, static 1.
- Geen losse pixels; enige "losse zwarte pixel" is het rechteroog (bedoeld). Zwart 12,3 %, static 6,0 % van de figuur.
- Tintvlekjes < 3 px die over zijn: selout-pixels langs de buitenrand (lijn), kuifstrengen en takjes (1 px dun, zoals in het model), oog-omgeving.

## Eerlijke twijfels
- **Kuif:** op 1/3 zijn de strengen 1–2 px; de zwarte omlijning van het model valt weg (anders wordt alles zwart). De kuif leest als violet gewei met licht boven, midden, donker onder; de takjes zijn 1 px. Drie lichtviolette pixels (L154, geen wit) staan aan de bovenrand van een streng: (37,12), (25,16), (28,16).
- **Static buiten de wolk** (links x3–8, y22–28; rechts x59–61, y23–26) is lichte modelkleur op de achtergrond, zonder rand: het is een los effect, geen lijfrand. Op een lichte gevechtsachtergrond valt het weinig op (zoals in het model).
- **Static in de wolk:** 10 lijnen op de modelplekken, 6 % van de figuur; dichtst op de linkervleugel. Als het als barstjes leest: de kortste (4–6 px) weghalen is de eerste stap.
- **Bollen:** door de 3×3-reductie zijn de bolvormen hoekiger dan de ronde modelbollen; de lichte toppen en donkere scheidingen staan op de modelplekken, maar sommige bollen (rechts in het lijf, x40–52, y30–48) lezen vlakker dan in het model.
