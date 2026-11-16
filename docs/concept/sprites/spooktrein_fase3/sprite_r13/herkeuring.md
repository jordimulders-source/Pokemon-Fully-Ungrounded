# Herkeuring r13 (16 nov, zelfde eindkeurder)

**Oordeel: FAIL, alleen op de koeienvanger.** De rest is PASS.

## MOET-punten r12
- r13 is pixelgelijk aan `sprite_r12/eind_voorstel.png` (diff 0, palet gelijk). Alle 21 punten zijn opgelost.
- Er is niets achteruitgegaan. Groen-diff t.o.v. r12: 0. Naad kop/lijf en lijfplaten zijn nu rustig, de linkerrand van de koeienvanger loopt zonder buil.
- Hoofdvraag op 1×/2×/8× naast het model: nog steeds ja, voor kop, lijf, schoorsteen, wielen en wolk.

## Extra punt coördinator: koeienvanger = drie poten i.p.v. één puntige kaak
**Dit is een MOET en valt niet onder "wat simpeler".** Simpeler mag minder tinten en minder roestvlekjes betekenen. Het mag niet betekenen dat de vorm anders gaat lezen: het model toont één puntige kaak, r13 leest als poten of blokken (Jordi: niets herinterpreteren). Vel: `herkeuring_koeienvanger.png` (r13 16× | model natief 11×).

Meting (FAKEMON_CHECKLIST A6, zuil = evenwijdige randen > 6 px):
- Er staan vier verticale naden van 8–9 rijen: x4 (y47–55, idx 12), x10–11 (y48–55, idx 12/1), x15–16 (y48–55, idx 1) en x22 (y48–55, idx 12).
- Alle plaatbovenkanten liggen op dezelfde hoogte (y48–49, lichte kap idx 7).
- De middentand (x12–14) en de rechterplaat hebben een vlakke onderkant (y55–56).

Het model (zie `sprite_r11/koeienvanger_keuring.md` §1):
- De naden waaieren naar de punt linksonder: links leunen ze naar rechts-omlaag, rechts naar links.
- De bovenkanten hangen in V's onder de zigzag.
- De middentand eindigt in een punt omlaag.
- Het laagste punt ligt linksonder, bij (4–7, 59). Dat klopt al.

**Opdracht voor de maker** (geen script van mij: dit is vorm, geen pixelruis):
- Zone x0–24, y46–59. Het silhouet blijft zoals het is, behalve de middentand.
- Neem de naden en de plaatbovenkanten over uit `model/natief.png` (overnemen, niet hertekenen).
- Schuine naden van 1 px die naar de punt leunen. Bovenkanten schuin, volgend op de zigzag.
- Middentand met een punt van 1–2 px omlaag (y56–57; mag het bevroren groen niet raken).
- Tinten blijven 7/11/12/1 + roest 8/9. Groen-diff 0.

Toets: op 2× moet je één kaak met tanden zien, geen tafelpoten. Geen naad recht over meer dan 4 rijen.

## MAG (blijft uit de eindkeuring)
- Lichte rand linksboven op de bovenste lijfplaat.
- (33,24), (41,28), (2,30–31), (20,44).
