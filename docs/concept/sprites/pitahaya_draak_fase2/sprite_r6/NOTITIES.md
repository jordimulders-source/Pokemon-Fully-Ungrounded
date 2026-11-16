# Pitahaya-draak fase 2, sprite r6 (maker): roze binnen de bek wordt grijs

Jordi (letterlijk): "kan dat roze in de bek ook een andere kleur? een donkerdere tint van wit/grijs wat we nu aan het doen zijn? dan ziet dat er natuurlijker uit"

Op `pitahaya2_r5.png`.
- Script `maak_r6.py`; met `--B` krijg je de variant.
- Vel: `vel6.py` → `vel.png`, met de bek op 12×: model | r6 | r6B | r5. Verder 8× r6 | r5, en 1× en 2× op licht en donker.
- Afwijkingen per pixel: `pitahaya2_r6_afwijkingen.txt` en `pitahaya2_r6B_afwijkingen.txt`.

**Bewijs (asserts in het script):**
- alle wijzigingen liggen binnen x 9–13, y 43–47, dus buiten de bek is de **diff met r5 0**;
- het silhouet is gelijk;
- er is geen dambord van grijstinten in de bekzone.

Palet ongewijzigd (14 incl. transparant). De grijsgroep blijft 3 tinten: W (237), w (191) en v (155).

## Wat
- **Binnen (verre lip) wordt v, de donkerste grijstint (5 px):** (10,45) p, (10,46) r, (11,46) r, (12,45) r en (13,45) r.
- **Wig wordt w (6 px; de pit (11,44) blijft):** (10,43), (11,43), (10,44), (12,44), (13,44) en (11,45). Dit is de grijstint die het model in de wig meet (mediaan 187).
  - Reden: zou de wig v blijven, dan versmelt hij met de verre lip tot één donker vlak, en dan zijn er nog maar 2 delen in plaats van 4.
  - Gen 3 (Exploud in `../sprite_r5/studie_open_bek.png`): waar een plooi over de tong valt, ligt een donkere lijn met lichtere vlakken eromheen. De volgorde is nu: wig grijs, verre lip donkergrijs, tong wit vooraan en grijs achterin.
- **Blijven roze (schil):** bovenlip en tandvlees, de lipband van de onderkaak met de linker buitenrand (9,46)–(9,47) d, en de mondhoek naar de wang (17,44)–(17,47).

## Twijfel (variant `pitahaya2_r6B.png`)
(9,45) r en (10,47) r zijn de plekken waar de verre lip overgaat in de buitenste lipband. In het model zijn ze 8/9 en 6/9 roze. In r6 blijven ze roze; in r6B worden ze ook v. In r6B loopt de grijze plooi door tot de buitenrand links.

## Zelf getoetst
- **12× en 2×:** de binnenkant leest nu als één vrucht: wit/grijs vlees met een donkergrijze plooi. Het roze zit alleen nog aan de buitenkant als schil.
- **De vier delen:** de bovenlip met tanden, de grijze wig, de donkergrijze plooi en de witte tong blijven te onderscheiden.
- **1×:** een witte bek met grijze bovenhoek.
- **Zwak:** de wig (w) raakt de grijze achterkant van de tong (14,45) alleen diagonaal, bij (13,44)/(14,45), naast de kaaklijn. Die raakplek valt op 2× niet op.
