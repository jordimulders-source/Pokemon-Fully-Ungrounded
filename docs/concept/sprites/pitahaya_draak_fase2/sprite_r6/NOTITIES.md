# Pitahaya-draak fase 2, sprite r6 (maker): roze binnen de bek wordt grijs

Jordi (letterlijk): "kan dat roze in de bek ook een andere kleur? een donkerdere tint van wit/grijs wat we nu aan het doen zijn? dan ziet dat er natuurlijker uit"

Op `pitahaya2_r5.png`.
- Script `maak_r6.py`; met `--B` krijg je de variant.
- Vel: `vel6.py` → `vel.png`, met de bek op 12×: model | r6 | r6B | r5. Verder 8× r6 | r5, en 1× en 2× op licht en donker.
- Afwijkingen per pixel: `pitahaya2_r6_afwijkingen.txt` en `pitahaya2_r6B_afwijkingen.txt`.

**Bewijs (asserts in het script):**
- alle wijzigingen liggen binnen x 9–13, y 43–47, dus buiten de bek is de **diff met r5 0**;
- het silhouet is gelijk;
- er is geen dambord van grijstinten in de bekzone;
- de wig is gesloten: elke wigpixel grenst alleen aan wig, pit, zwart of v. De enige uitzondering is (9,44) r, de lipband links.
- r6 heeft 13 px gewijzigd t.o.v. r5, r6B 15 px.

Palet ongewijzigd (14 incl. transparant). De grijsgroep blijft 3 tinten: W (237), w (191) en v (155).

## Wat
- **Binnen (verre lip) wordt v, de donkerste grijstint (5 px):** (10,45) p, (10,46) r, (11,46) r, (12,45) r en (13,45) r.
- **Wig wordt w (6 px; de pit (11,44) blijft):** (10,43), (11,43), (10,44), (12,44), (13,44) en (11,45). Dit is de grijstint die het model in de wig meet (mediaan 187).
  - Reden: zou de wig v blijven, dan versmelt hij met de verre lip tot één donker vlak, en dan zijn er nog maar 2 delen in plaats van 4.
  - Gen 3 (Exploud in `../sprite_r5/studie_open_bek.png`): waar een plooi over de tong valt, ligt een donkere lijn met lichtere vlakken eromheen. De volgorde is nu: wig grijs, verre lip donkergrijs, tong wit vooraan en grijs achterin.
- **Blijven roze (schil):** bovenlip en tandvlees, de lipband van de onderkaak met de linker buitenrand (9,46)–(9,47) d, en de mondhoek naar de wang (17,44)–(17,47).

## Bovenlip-reparatie (`keuring_r5/KEURING.md`, punt 2; 4 px)
De kaaklijn loopt nu als trap van 7, 4 en 3 px naar de mondhoek, zoals bij Croconaw en Gyarados (studievel r5):
- rij 42: x 3–9, met het tandvlees op x 4 en x 8;
- rij 43: x 10–13;
- rij 44: x 14–16.

Gewijzigde pixels:
- (10,43) en (11,43): v → K. In de afwijkingenlijst staat dit als twee stappen: eerst v → w (wig), daarna w → K.
- (10,42) en (11,42): K → r. Dit is het roze van de bovenkaak, dezelfde tint als op (14–16,43).

**Afwijking van het model:** in het model is dit stuk recht. Blok (10,42) heeft 3 zwarte pixels onderin, en (10,43)/(11,43) hebben 0–1 zwarte pixel (dat is wig). Deze afwijking komt van de keurder, die hiervoor Jordi's vrijgave gebruikte om naar Gen 3 te kijken.

Wat gelijk blijft: de tanden (4,43) en (8,43) en de pit (11,44). De wig is nu 5 px: (10,44), (11,44) met de pit, (12,44), (13,44) en (11,45). Hij sluit tussen de kaaklijn boven, de grijze plooi onder, (14,44) K rechts en (9,44) r links.

## Twijfel (variant `pitahaya2_r6B.png`)
(9,45) r en (10,47) r zijn de plekken waar de verre lip overgaat in de buitenste lipband. In het model zijn ze 8/9 en 6/9 roze. In r6 blijven ze roze; in r6B worden ze ook v. In r6B loopt de grijze plooi door tot de buitenrand links.

## Zelf getoetst
- **12× en 2×:** de binnenkant leest nu als één vrucht: wit/grijs vlees met een donkergrijze plooi. Het roze zit alleen nog aan de buitenkant als schil.
- **De vier delen:** de bovenlip met tanden, de grijze wig, de donkergrijze plooi en de witte tong blijven te onderscheiden.
- **1×:** een witte bek met grijze bovenhoek.
- **Zwak:** de wig (w) raakt de grijze achterkant van de tong (14,45) alleen diagonaal, bij (13,44)/(14,45), naast de kaaklijn. Die raakplek valt op 2× niet op.
