# Ruimtestation sprite r9 (25 nov): vormherstel op s18p15

Jordi over r8: "ze zijn allemaal nog niet super afgewerkt, dus het grootste kan gewoon, probeer de vormen goed te herstellen, rond rond, rechthoekig rechthoek, de panelen in het midden groeien niet mee, het oog netjes erin zetten, maar ik denk dat we er wel komen".

De basis is r8 s18p15. De zijbollen zijn ×1,8, de voorste bol ×1,3 en de panelen ×1,5.

## Bestanden
- `sprite.png` (+ `sprite_8x.png`): de eindsprite. Hij heeft 16 kleuren (incl. transparant) en transparency=0.
- `vel.png`: bovenaan r8 s18p15, r9 en het model. Daaronder close-ups van de ogen en de panelen (boven r8, onder r9). Onderaan 1× en 2× naast fase 2, op licht en op donker.
- `model9.py` maakt `model_r9.png`. `maak9.py` en `pijp/` zijn de r8-pijplijn en maken de tussenstap `sprite_r9.png`. `herstel9.py` doet de vormreparaties en maakt `sprite.png`.
- `diff_herstel.png` laat in rood zien wat herstel9 veranderde ten opzichte van de pijplijn.
- `w_r9/log_herstel9.txt` bevat elke pixel met zijn reden.
- Om opnieuw te maken: `python3 model9.py`, dan `cd w_r9; VAR=r9 python3 ../pijp/bouw7.py`, dan `python3 maak9.py r9`, dan `VAR=r9 python3 herstel9.py`.

## 1. Mastpanelen (model)
**Wat er in r8 misging:** PB en PF stonden in r8 al op ×1,5, maar in de sprite groeiden ze nauwelijks mee.
- PB werd 3 → 4 px breed.
- PF bleef 4 px breed. Hij groeide rond zijn middellijn, en de linkerhelft viel achter de voorste buis. Daarnaast gaven staafjepixels in het bronpaneel gaten in het model (wit, telde als achtergrond).

**Wat r9 anders doet:**
- **Gaten:** in PB/PF wordt een staafjepixel binnen het paneel opgevuld met de dichtstbijzijnde paneelpixel van hetzelfde paneel.
- **Anker:** PF groeit nu, net als PB, vanaf zijn linkerrand (anker v=0), zodat de verbreding naast de buis zichtbaar wordt.
- **Factor:** PB krijgt ×2,0 en PF ×2,5 (t.o.v. r13b). Dat komt neer op ×1,5 van de zichtbare r7-breedte: PB 3 → 5 px, PF 4 → 7 px.
- **Afwijking van de letterlijke opdracht:** ×1,5 als modelfactor gaf geen zichtbare groei (r8 had die factor al). In de map staat geen ×1,5-variant meer. Die kan terug met `KPK` in `pijp/common.py`.

## 2. Vormherstel (herstel9.py)
Er zijn 359 pixels anders dan de pijplijnuitvoer (344 t.o.v. r8 s18p15). Het silhouet telt 1281 px (r8: 1282).

### Panelen (177 px + 57 px weg)
**Vorm:**
- Een pixel hoort bij een paneel als zijn middelpunt binnen het modelparallellogram valt. Dat parallellogram is GEO uit `lijnen.py`: de gemeten hoekpunten van het model, met de r9-verbreding.
- De volgorde van achter naar voor is PC, PA, PB, PD, PF, PE.
- De romp blijft vóór het paneel waar hij buiten het parallellogram ligt, of waar het model ≥ 50 % romp heeft.
- Losse hoekpunten (≤ 1 buur) zijn weggehaald.
- Gaten van 1 px zijn dichtgemaakt.
- Rompgaten zijn gevuld met de kleur uit de kale modelreductie (9 px).

**Kleur:** volgens het bestaande r8/fase 2-recept.
- **Rand:** een pixel is rand als zijn buur buiten het eigen parallellogram ligt. Wat ervoor ligt, telt als binnen, zodat de rand recht doorloopt. De rand is zwart aan de onderkant en navy aan de lichtkant.
- **Vlakken:** de lichte rand c langs de lichtkant, en de vaktint per vak (licht → donker).
- **Rasterlijnen:** 1 px per kolom of rij, op u = ¼, ½, ¾ (voor/achter, 4 vakken) en ⅓, ⅔ (mast, 3 vakken). Op een donker vak is de lijn e, anders c.

**Paneelcontrole:** de treden zijn per kolom de boven- en onderrand (bij de mast per rij links/rechts). Lange randen hebben een gelijk ritme, met verschillen van hooguit 1.

| paneel | eigen pixel buiten het parallellogram | leeg binnen | lange rand boven | lange rand onder |
|---|---|---|---|---|
| PA | 0 | 1 | 2,3,3,3,4 | 3,3,4,3 |
| PC | 1 | 1 | 4,4,4,3 | 4,4,3 |
| PD | 0 | 5 (hoekpunten) | 3,3,2,3 | 3,3,2,3 |
| PE | 2 | 2 | 3,3,3 | 3,3,3,2 |
| PB | 0 | 1 | links recht 14 | rechts recht 14 |
| PF | 2 | 3 | links recht 10 | rechts recht 10 |

### Bollen (13 px)
- Op de vrije rand is de bol nu een cirkel: een pixel hoort erbij als zijn middelpunt ≤ R ligt.
- R is gefit op de bestaande rand en het middelpunt komt uit het model.
- Een oude randpixel die nu binnen ligt, krijgt de tint van zijn buur naar binnen.

| bol | R (px) | vrije sector | afwijking vóór herstel | afwijking r9 |
|---|---|---|---|---|
| voor | 7,84 | 204° | −0,37 … +1,56 | −0,37 … +0,42 |
| links | 5,51 | 258° | −1,38 … +2,00 | −0,11 … +0,47 |
| rechts | 6,51 | 183° | −0,46 … +0,38 | −0,29 … +0,50 |
| achter | 4,51 | 258° | −0,43 … +0,50 | ongewijzigd (al binnen ±0,5) |
| knoop (hub) | – | geen vrije rand | – | – |

De afwijking is d − (R − 0,5) van de randpixels.

### Ogen (96 px)
**Vorm:** het voorste oog heeft ring 8 (rijen 4,6,8,8,8,8,6,4), iris 6 (4,6,6,6,6,4) en een pupil van 2×2 precies in het midden. De zij-ogen hebben dezelfde vorm, verkleind: ring 6 (4,6,6,6,6,4), iris 4 (2,4,4,2) en pupil 2×2. Binnen de ring zit geen wit.

**Kleur:**
- Iristint: 9 of a uit de modeldekking.
- Ringtint: 8 linksboven, 6 rechtsonder, 7 voor de rest. De modeldekking gaf na de verschuiving ruis.
- Oude oogpixels buiten de nieuwe vorm krijgen de boltint van hun buur.

**Plek:** zo dicht mogelijk bij het model, met de voorwaarde dat geen oogpixel op de bolrand of op de kraag ligt. Daardoor zijn de ogen verschoven:
- voor: +0,74 / +0,13 px
- links: +1,04 / −0,85 px. In het model ligt hij op de silhouetrand; in r8 lag de ring óp de omlijning.
- rechts: +0,39 / −0,47 px

### Omlijning (7 px)
Een randpixel tegen transparant is zwart aan de onderkant en rechts, en navy elders (r4-regel). Dit raakte alleen pixels die door het herstel aan de rand kwamen te liggen.

### Buizen
Aan de buizen zijn geen pixels veranderd. Op 12× gecontroleerd: de contouren lopen met een regelmatige trap van 1–2 px.

## Ter info
- **Lengtelijnen:** het model heeft in elk paneel ook een middenlijn in de lengte (2 rijen vakken). Die staat niet in de sprite, zoals in r7/r8.
- **PF in het model:** de verbrede PF is in `model_r9.png` nog rommelig van textuur. In de sprite komt PF volledig uit de geometrie en het recept, dus dat heeft geen invloed.
- **Keuring:** er is nog geen keurder geweest.
