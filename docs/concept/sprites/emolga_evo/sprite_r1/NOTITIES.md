# Emolga-evolutie (wingsuit-colugo) frontsprite, ronde 1 (maker)

Bestanden: `A0.png` (model 1-op-1), `A.png` (A0 + kop 1,4x, optie A), `kaal_A0.png` / `kaal_A.png` (kale reductie, zelfde palet),
`vel.png` (per sprite: rN 8x | model op dezelfde schaal 8x | gezicht 12x sprite/model met raster | 1x licht en donker).
Bouwen: `python3 sprite_r1/maak.py` (vanuit `emolga_evo/`). Scripts: `bouw_a0.py`, `bouw_a.py`, `gezicht_a0.py`, `gezicht_a.py`;
gereedschap in `../gereedschap/` (pitch, natief, gemeen = modelklassen, reduceer = oppervlak-middeling, opschoon, kop = kopmasker/1,4x,
raster = model per spritecel, controle, vel, vergelijk).

## Metingen
- Natief raster model: pitch 10,238, fase 9,35 (zelfde raster als Alphyena), 99x99; figuur x16-84, y7-84 = **69x78**.
- 78 -> 63 rijen = -19 %: te veel voor schrappen (Hauntflare-les, >13 %), dus **oppervlak-middeling met meerderheidsklasse**
  (geen mengtinten, Swablu-les), silhouet = bedekking >= 0,45. Schaal 63/78 = 0,808. Figuur in de sprite x4-59, y1-63
  (rechtervleugelpunt 1 px van de bovenrand, kin op de onderrand). 1397 px. Kijkt naar links, niet gespiegeld.
- Silhouet t.o.v. het model (vlakgemiddelde alfa >= 0,45 op dezelfde schaal): 2 px alleen sprite, 19 px alleen model (dunne randen);
  zwaartepunt verschilt 0,1 px. A: 3 / 20 px.
- **A:** kop = natieve kopomtrek langs de modellijnen (`kop.py` NATPOLY: verre oor + kop + nabije oor tot en met hun zwarte
  omlijning; NIET de armband van de linkervleugel tussen de oren), alleen modelpixels, 1,4x om het onderkant-midden (kin) = 1,131x natief,
  met dezelfde oppervlak-middeling. Referentie op modelniveau: `model/kop_opties/A_kopmodel_1024.png`.
  Buiten de kopzone (nieuwe + oude kop, 627 px) **pixeldiff 0 t.o.v. A0** (assert in `bouw_a.py`).

## Palet (index = modelklasse)
0 transparant · 1 K (16,16,24) · vacht 2 D (36,36,44) 3 E (60,60,70) 4 G (90,88,100) · geel 5 y (184,140,24) 6 Y (224,184,40)
7 L (248,220,80) · wit 8 B (180,194,208) 9 W (240,246,250). 10 kleuren incl. transparant. Vacht naar Emolga (32/56/88), geel en wit
iets verzadigder dan het model; vlakverdeling (welke tint waar) = model.

## Afwijkingen t.o.v. de kale reductie
**A0: 178 px** — gezicht 43, oren 45, linkervleugel 40, rechtervleugel 28, buik/hand 22. Per stap:
- ontkorrel 54: tintvlakjes < 3 px nemen de buurtint van dezelfde kleurgroep (niet in het gezicht).
- buitenlijn 89: alleen kleur van randpixels: schaduwkant (buitenwaartse normaal niet naar linksboven, of transparant rechts) -> K;
  lichtkant -> selout (vacht D, ook modelzwart; geel y; wit B), zoals Emolga's oor (32/32/40 linksboven). Daarna geen D/K om en om.
- lichtstreep 12: de lichte modelstreep (G) die op de rand lag en selout werd, 1 px naar binnen (opbouw rand | G | D zoals in het model):
  (55,5) (48,13) (7,19) (7,20) (38,24) (7,41-47).
- lijf-reparaties 6 (wat de reductie kapotmaakte, naar het model): oorlijn nabije oor doorlopend (17,40)y>K (15,42)D>K;
  losse K (16,46)>G en 2x2 zwart blok (15,43)>G; losse gele Gemini-pixel (31,45)>E; los streepje (9,21)K>D.
- gezicht 26, per spritecel gelezen op het model (`raster.py`): verre visorstrepen wit (10,55-57) (14,54), pupiltop (17,54)K,
  pupil (16,55)E (13,56)E, oogglans linksonder (15,58)W, krul (19,59)W (18,60)W (17,61)W (16,62)W, wang/band onder de ogen (11,58) (12,58)
  (14,58) (13-15,60)E, rand (20,60)K, gele kinpixel (13,62)>B (Gemini-ruis). Overige: (11,55) (11,56) (21,56)>G, (9,57)>G, (10,58)>G.
**A (kopzone): 75 px t.o.v. de kale kopreductie** — gezicht 22, oren 53. Per stap: dubbele lijn 14 (1,13x maakt 1-px modellijnen soms
2 px: binnenste K -> buurtint), naad 10 (rand van de grotere kop over lijf/vleugel -> K: (23,27) (21,28) (22,28) (19,30) (16,33) (16,34)
(14,38) (25,37) (25,38)), ontkorrel 15, buitenlijn 33, oude-kop-pixel (6,49) -> transparant, reparaties 9: (17,39)>G, gele Gemini-pixels
(20,48)>W (12,62)>B, 2 px dikke oorlijnen -> 1 px (15,35) (14,36) (14,37)>D en (24,40) (23,42) (23,43)>G.
**Pixels die niet uit het model komen:** alleen kleurwissels hierboven (selout/zwart, buurtint) en de naad-K van A (de kopomlijning
op een plek waar in het model lijf lag). Geen getekende vormen; oog, krul, oren en hand zijn modelpixels.

## Controle
64x64, mode P, transparency 0, 10 kleuren. Geen losse zwarte pixels. Losse tintpixels alleen in het gezicht (oogglans, krul,
visorstrepen, model) en 2-px clusters in het gezicht. 2x2-"dambord"-treffers zijn allemaal 1-px diagonale lijnen (lichte streep in de
vleugelband), geen vlak patroon. Zwart A0 15,5 %, A 16,7 %.

## Twijfels
- Het gezicht is het model per cel: verre visorstrepen W-G-W-G (1 px breed) en de witte krul in de pupil zijn modelvormen, maar op 1x
  druk; alternatief zou een Gen 3-oog uit een bestaande sprite zijn (niet gedaan, opdracht = model).
- Linkervleugelrand is nu selout D i.p.v. modelzwart (Gen 3-regel licht linksboven); op 1x nauwelijks verschil.
- Vacht licht G (90,88,100) maakt de kop iets grijzer dan het model (66); donkerder = minder stap tussen E en G.
