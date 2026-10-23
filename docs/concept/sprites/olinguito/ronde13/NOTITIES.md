# Olinguito ronde 13: lijf ruimtelijk in één 3/4-diagonaal (basis ronde 12)

Jordi op ronde 12: "Bijna klaar. Het lichaam heeft een onmogelijke, Escher-achtige pose momenteel." Alleen de lichaamsconstructie is veranderd. Kop, masker, ogen, mond, palet, armen en klauwen, staart en de sluiphouding zijn pixel voor pixel ronde 12 (in `bron/delen_abs.txt` zijn alleen de delen `lijf`, `been_achter` en `been_voor` nieuw).

## Oorzaak van het Escher-effect (ronde 12)
- De **dichtbije achterpoot** stond midden onder de buik (x30–45), ver links van de heup (x45–55): hij hing nergens aan en leek van achter het lijf naar voren door de buik te steken.
- De **verre achterpoot** stond rechts van de dichtbije, op de plek van de heup, en bijna even laag. In een 3/4-aanzicht naar links-voor staan de verre poten juist **links van en hoger dan** de dichtbije (de verre kant draait naar achteren). Daardoor klopten de dieptevolgorde en de overlap niet met elkaar.
- De buiklijn hing het diepst in het midden (y48 bij x34–41) in plaats van bij de borst, waardoor de romp geen richting de diepte in had.

## Constructie (`constructie.png`, hulplaag over ronde 12, alleen schets)
- Romp = boon uit twee ovalen: **borst** dichtbij, groot en laag (midden ±31,43, onder de kop), **heup** verder weg, kleiner en hoger (midden ±47,39). De middellijn loopt van linksonder-voor naar rechtsboven-achter; de staart zit aan het eind daarvan, bovenop de heup.
- Schouder- en heupas staan dwars daarop: de dichtbije kant ligt rechtsonder, de verre kant linksboven.
- Poten hangen aan die assen: dichtbije voorpoot (de klauwarm) aan de dichtbije schouder; verre voorpoot (opgetrokken sluippoot) links-hoger, achter de kop. Dichtbije achterpoot: dij over de onderkant van de heup, knie naar voren, voet onder de heup. Verre achterpoot: links van en hoger dan de dichtbije, tussen borst en dij, met de bovenkant achter de buik.
- Voethoogtes (diepte): klauwen vooraan y55 (dichtst bij), dichtbije achtervoet y54, verre achtervoet y52, verre voorpoot opgetrokken (±y47).

## Wat er veranderde (met de hand, tekstraster)
1. **Romp:** bovenkant (heup als hoogste punt, lichte flank diagonaal omlaag naar de borst) bleef; de onderkant is opnieuw: de buiklijn is het laagst bij de borst (y49, x27–30) en stijgt naar achteren (y47 bij x34–40). De achterkant van de heup is rond (rechterrand x52→53→54→53) in plaats van recht.
2. **Dichtbije achterpoot:** dezelfde getekende poot als ronde 12, maar 9 px naar rechts en 1 rij omhoog, zodat de dij precies over de onderkant van de heup valt (voor het lijf getekend, lichte naad bovenaan) en de voet onder de heup staat.
3. **Verre achterpoot:** nieuw, kort en in schaduwtint (2/1): zichtbaar tussen borst en dij, bovenkant achter de buik, voet 8 px breed en 2 rijen hoger dan de dichtbije. Hij overlapt niets en wordt overlapt door lijf en dij.
4. **Overlapvolgorde** (achter naar voor): staart, verre achterpoot, lijf, dichtbije achterpoot, verre voorpoot, dichtbije voorpoot, kop. Consequent: wat dichterbij is, ligt erover.
- Animatie ongewijzigd (kop, staart en armen 1 px omhoog in frame 2; lijf en achterpoten staan).

## Bestudeerde sprites (compare.png, onderste rij)
- **Mightyena:** overgenomen: verre voor- én achterpoot links van en hoger dan de dichtbije, donkerder en deels achter het lijf; de dichtbije achterpoot hangt aan een dij die de heup overlapt.
- **Poochyena:** overgenomen: borst laag en dichtbij, heup hoger; de verre achterpoot piept tussen buik en dichtbije poot.
- **Persian:** overgenomen: sluipende romp als boon die de diepte in loopt, staart vanaf de heup.
- Ook bekeken: Zigzagoon en Linoone (lange romp, poten kort onder de buik), Meowth, Sneasel, Zangoose en Absol (staande houdingen, minder bruikbaar voor de viervoetconstructie).

## §0-checklist (SPRITING.md)
1. **Lichaam én blik diagonaal:** ok. Kop 3/4 (ongewijzigd); romp als boon van borst (linksonder) naar heup (rechtsboven); verre poten links-hoger en in schaduw.
2. **Geteld en verbonden:** ok. 2 oren, 2 ogen, neus, mond, 2 voorpoten (elk 2 klauwen), 2 achterpoten met tenen, 1 staart; elke poot zit aan schouder of heup. bouw9: geen open randen in beide frames.
3. **Geen rechte lijnen:** ok, bouw9 meldt geen rechte randstukken > 4 px meer (ronde 12: buiklijn).
4. **Ogen geïntegreerd:** ok (ongewijzigd).
5. **Silhouet op 1×:** ok; maskerkop, klauwen vooraan, pluimstaart, en nu vier poten die als twee paren lezen.
6. **Formaat:** 1068 / 1084 px (ronde 12: 1063 / 1075); fase 1 Treecko 967, Mudkip 852, Torchic 782 (verschil door de staart, zoals eerder).
7. **Pose niet stijf:** ok; dichtbije achterpoot gebogen onder de heup, verre poot korter en hoger, één voorpoot opgetrokken.

## Controle (bouw9)
- Open randen: geen. Rechte randstukken > 4 px: geen. Zwart-aandeel rand 0,59 (doel 0,35–0,6).

## Voor Jordi
- Als het lijf nog te veel "kat" leest: de heup kan 1–2 px lager, dan helt hij minder.

## Bestanden
- `anim_front.png`, `normal.pal` (palet = ronde 10–12), `constructie.png` (schets), `compare.png` (boven: ronde 12 en 13, beide frames, 1× en 3×; onder: Mightyena, Poochyena, Persian).
- `bron/delen_abs.txt`: de bron. Bouwen: `sh bron/bouw.sh <ronde13-map> [preview.png]`. `bron/vergelijk13.py <repo-root>` maakt compare.png; `bron/constructie.py <olinguito-map>` maakt de schets.
