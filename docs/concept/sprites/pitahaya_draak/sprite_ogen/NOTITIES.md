# Pitahaya-draak: oogvarianten op r3

Jordi: "begint al netjes te worden, kunnen de ogen nog iets scherpere lijnen krijgen als alternatieve versie waar ik uit kan kiezen?"

## Opzet
- **Basis:** `pitahaya_r3.png` (kopie uit `sprite_r3/`).
- **Ooggebied:** verre oog x 18–23, nabije oog x 28–36, y 22–27, zonder randpixels.
- **Bewezen met assert in de scripts:** diff 0 buiten het ooggebied en silhouet-diff 0.
- **Niets getekend.** Elke oogpixel komt uit het natieve model (A, B) of uit een echte Gen 3-sprite (C).
- **Bestanden:** `afwijkingen_r3.txt` (elke gewijzigde pixel), `ogen_vel.png` (r3 | A | B | C op 8×, kop op 12× met het model, 1× en 2× op licht en donker).

## A: model, strengere lijnregel (`ogen.py A.png A`), 7 px
Het ooggebied opnieuw gereduceerd uit het natieve raster met deze regels:
- zwart alleen bij ≥ 5/9 zwarte modelpixels (was ≥ 2);
- iris amber bij ≥ 3 amber modelpixels, toon via het blokgemiddelde;
- een omtreklijn alleen waar het model ≥ 2 zwarte pixels heeft én de pixel aan de iris grenst;
- de glans per oog in de cel met de meeste witte modelpixels.

Resultaat:
- Het nabije ooglid wordt een dunnere schuine lijn: (32,23), (36,23) en (35,22) zijn niet meer zwart.
- Het verre oog krijgt de glanspixel van het model op (20,24); die ontbrak.
- (22,24) wordt roze en (22,26) amber, (18,26) wordt selout.

## B: dezelfde regel op een andere fase (`ogen.py B.png B 1 0`), 16 px
- Het ooggebied is één natieve pixel lager bemonsterd.
- Nabije oog: een strakke 1-px schuine lidlijn, met daaronder glans, pupil en een bredere amber iris (donker amber boven, licht onder).
- Verre oog: met glans.
- Dit is het duidelijkst "scherpere lijnen" en nog steeds alleen modelpixels.

## C: Gen 3-oog uit Shiftry (`ogen_c.py C.png 3,4,5 20 23`), 30 px
- **Bron:** `graphics/pokemon/shiftry/anim_front.png`, frame 1, x 21–27, y 24–28, pixel voor pixel. Lid (96,64,40) en zwart worden ons zwart, het geel (240,224,128) ons licht amber.
- **Nabije oog:** het hele oog (7×5) op de plek van het modeloog.
- **Verre oog:** hetzelfde oog met alleen de kolommen 3–5 (schrappen, perspectief smaller), op x 20–22.
- **Oude oogpixels** die erbuiten vallen worden roze huid uit het model.
- **Let op:** dit wijkt af van het model. Veel minder amber en geen glans; het oog leest als een boze spleet in plaats van de grote amber ogen van het model.
