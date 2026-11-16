# Keuring r6 – pitahaya-draak fase 2, `sprite_r6/pitahaya2_r6.png` en `pitahaya2_r6B.png`

Hulpmiddelen in deze map:
- `zij.py`/`zijB.py` → `bek_r6.png` en `bek_r6B.png` (bek op 20× naast het model);
- `r5_r6_r6B_1x2x.png` (r5 | r6 | r6B op 1× en 2×, lichte en donkere achtergrond);
- `meet_*.py` (clusters, dambord).

Diff met r5: r6 13 px, r6B 15 px, allemaal in x9–13, y42–47. Het palet is gelijk (v/w/W + pit).
Letters: v = donkergrijs (155), w = grijs (191), W = wit (237), s = pit, K = zwart, r/p = roze.

## Oordeel: FAIL (1 pixel)

### Bovenlip
De bovenlip is goed hersteld. De kaaklijn loopt nu als trap 7–4–3:
- rij 42, x3–9;
- rij 43, x10–13;
- rij 44, x14–16.

Op 2× zakt de lijn zichtbaar naar de mondhoek, zoals bij Croconaw en Gyarados, en leest hij niet meer als liniaal. De tanden (4,43) en (8,43) staan nog onder de lijn.

### Leest de binnenkant natuurlijk, en zijn de delen apart?
- **Natuurlijk:** ja. De verre lip in v is een donkere grijze plooi tussen wig en tong. Hij hoort nu bij het vruchtvlees in plaats van een roze streep te zijn. Op 2× is de bek een wit vlees met een donkere vouw en een grijzere bovenhoek; op 1× een witte bek met pitjes en een donkere bovenrand.
- **Delen:**
  - bovenlip met tanden: apart;
  - wig (w met pit (11,44)): apart;
  - verre lip (v): apart;
  - witte tong: apart.
- **Behalve rechts:** daar lopen wig en de grijze achterkant van de tong in elkaar over (zie hieronder).
- De wig is nu w en niet meer de donkerste tint. Het donkerste binnenin is de lipvouw v. Dat is een gevolg van Jordi's keuze en geen fout.

### Raakt de wig de grijze achterkant van de tong lelijk bij (13,44)/(14,45)?
**Ja.**
- (13,44) w en (14,45) w zijn dezelfde tint en raken elkaar diagonaal.
- De donkere lip stopt op (13,45) en de kaaklijn op (14,44); die twee kruisen elkaar op hetzelfde punt.
- Daardoor loopt het grijs van de wig via die diagonaal door naar de tongachterkant (x14–16, y45–48). Op 20× en op 2× leest dat als één grijze band om het einde van de lip heen.
- Dit is precies Jordi's eerdere opmerking: "onderkant en bovenkant mond loopt nu een beetje in elkaar over".

### Netheid in de bekzone
- Het grijs heeft 3 tinten plus de pit.
- Het enige dambord is (16,43): lijn tegen vulling bij de mondhoek, dus normaal.
- (11,45) w is een lichte pixel die tussen v (10,45) en v (12,45) in de lip steekt. Hij komt uit het model (wigblok 8–9/9 vlees) en hangt diagonaal aan de wig. Klein, en mag blijven.
- W (15,49) en pit (10,48) staan zo in het model (zie eerdere keuringen).
- Verder geen nieuwe losse pixels.

## Reparatie (voor r6 en r6B allebei)
1. **(14,45): w → v.** De verre lip loopt dan door tot hij de kaaklijn raakt, op (14,44)/(15,44) K.
   - Herleid tot het model: de maker mat in r5 dat de verre lip bij nx 44, ny 95,5 aansluit op de kaaklijn, en dat is spritekolom 14.
   - Daarmee is de wig helemaal afgesloten van de tongachterkant. Die begint dan op (15,45).
   - Diff verder 0.

## r6 tegenover r6B (beschrijving, geen keuze)
- **r6:** links houdt de lip roze resten:
  - (9,44) r en (9,45) r, naast de voorste tand;
  - (10,47) r, onder (10,46) v.

  De grijze vouw gaat links over in de roze lipband.
- **r6B:** (9,45) en (10,47) zijn ook v. Alleen (9,44) r blijft, als roze stukje in de hoek bij de tand. De grijze vouw loopt door tot tegen de linker lipband, en het roze zit alleen nog op de buitenlippen.
- **Op 1× en 2×:** nauwelijks verschil. Op 8–20× is r6B de doorlopende grijze vouw en houdt r6 een roze begin links.
