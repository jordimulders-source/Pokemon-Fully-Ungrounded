# Coathief: kleursprite ronde 8 (voorpoten overgetrokken van de onderlaag, oren zwart)

Basis: ronde 7b (ronde 7 plus de eindkeuringsreparaties).

Jordi letterlijk:
- "de ene voorpoot is nu wel een stuk groter dan de ander he, plus de vorm van de gebogen poot klopt niet meer [...] blijf vooral naar de meest linkse kijken, daar zijn de lijnen van de poten echt perfect";
- "De oren mogen trouwens ook weer zwart worden, bivakmuts idee";
- "hij moet donkerder tonen dan linoone en furret, want het is een dark type".

## Bestanden
- `coathief.png`
- `vel.png`
- `uitsnede.png`
- `overtrekvel_r8.png`: de onderlaag naast ronde 8 op hetzelfde 64-raster. Elke cel die afwijkt van de onderlaag is rood omkaderd, met de reden eronder.
- `onderlaaglijn_over_r8.png`: de zwarte omlijning van de onderlaag (blauw, verkleind 4:1) over ronde 8 op 20×.
- `onderlaag_7b_8_voorpoten.png`: de voorpoten op 8×, met de onderlaag, 7b en 8 naast elkaar, op licht en op donker, plus 1×.
- **Silhouet:** `../../silhouet/ronde9.txt` (1315 px: 10 erbij en 18 eraf ten opzichte van ronde8, alleen in x 10–34, y 50–63).
- `bron/`:
  - `raster.txt` is 7b als volle rijen;
  - `reparaties.txt` bevat ronde 8: de rijen 50–63 over x 10–34 met de hand overgetrokken, plus de oren;
  - `silhouet_ronde9.py`, `overtrekvel_r8.py`, `onderlaag_lijn.py`, `diff_r7b.py`, `controle.py`, `vel.py`.

## Bewijs
```
controle.py: pixels 1315 | silhouet 1315 (ronde9.txt) | alpha-diff 0 | open randen 0 | losse pixels 0
diff_r7b.py:
zone voorpoten (x 10-34, y 46-63)   82 px
zone oren (x 14-26, y 30-34)        16 px
totaal 98 | buiten de zones: 0
```
- Geen d (index 6) naast transparant aan de schaduwkant; de rechterrand is overal k.
- Het palet en de helderheid zijn ongewijzigd: niet lichter gemaakt (Dark-type).

## 1. Voorpoten: pixel-over, cel voor cel
Per cel bepaalt de onderlaag wat er komt: buiten, omlijning, manchet, staande poot, bruine bovenarm of klauw.
- **Manchet (opgetilde poot):**
  - linkeromlijning per rij 22, 22, 21, 21 (y 50–53);
  - rechts loopt hij via de bovenarm tot x 27–28, met de onderkant op y 56 (k).
  - Hij is ongeveer even dik als de staande poot (6–7 tegen 6 px), zoals op de onderlaag.
- **Bruine bovenarm:**
  - bruin vanaf x 26 (y 50), 28 (y 51–52) en 29 (y 53), met de punt op (28,54);
  - de naad met de manchet is gebogen;
  - de curve (29,54), (28,55), (23–26,56) is de omlijning van de onderlaag.
- **Staande poot:**
  - rechteromlijning x 31 van y 50 tot 60, linkerrand x 26 op y 57–58, zoals op de onderlaag;
  - eerst slagschaduw onder de curve, dan de lichtkant y;
  - de voet ligt op y 59–61 (k-onderrand).
- **Klauwen:**
  - **Opgetilde poot:** een crème blok op y 55–56 (x 19–23) dat op y 57 splitst in twee hangende haken met punten op (18,59) en (21,59). Glans op (20,55).
  - **Staande voet:** twee klauwen naast elkaar die naar voren op de grond liggen: (23–24,60–61) en (26–28,60–61), met glans op (27,60).
  - **Omlijning:** x bovenaan op (24–26,59) en onderaan op (22–24,62) en (26–27,62).

**Afwijkingen van de onderlaag** (gemarkeerd op `overtrekvel_r8.png`), alleen waar 1× anders niet leest:
- (20,58): lucht tussen de hangende klauwen. Op de onderlaag staat daar een zwarte rand; met die rand vloeien de klauwen op 1× samen.
- (21,59): de punt van de rechterklauw 1 px naar rechts, zodat hij vast blijft aan de klauw.
- (18,60), (20,60) en (24,63): puntjes van 1 px weggelaten, want ze lezen als kruimels.
- (25,60–61): een donkere scheiding tussen de twee klauwen van de staande voet, waar de onderlaag een teenkeep heeft.
- (25,62): lucht onder die scheiding.

## 2. Oren zwart (bivakmuts)
- **Nabij oor:** m-rand bovenop, Y/y-licht linksboven, z, en een donkere binnenkant m met een k-rand rechts.
- **Ver oor:** m/y/z met k rechts.
- Geen crème meer. Op licht en op donker lezen ze als ronde oortjes door het grijze licht linksboven, net als de rest van de muts.

## Toets (1×, 8×, 10× en 20×, licht en donker)
- Op het overtrekvel en de overlay valt de omlijning van ronde 8 samen met die van de onderlaag (±0,5 px), behalve op de gemarkeerde cellen.
- Op 1× zijn het twee even dikke voorpoten. De opgetilde zit compact onder de kin met lichte hangende klauwen, de staande is gebogen en draagt, met de klauwen ervoor.
- De oren zijn zwart en rond.
- Hij is donkerder dan Linoone en Furret.
- Ik zie geen zwak punt.

## Les
- Pixel-over werkt het best op een overtrekvel met identieke coördinaten: kies per cel het onderdeel op het celmidden, en markeer elke afwijking met een reden.
- Na een lange reeks reparaties is overtrekken sneller en zuiverder dan bijschaven.
