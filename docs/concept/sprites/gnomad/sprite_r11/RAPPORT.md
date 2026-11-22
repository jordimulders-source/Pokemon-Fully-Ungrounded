# Gnomad sprite r11: binnenlijnen onder neus en snor (22 nov)

Bron: `../sprite_r10/gnomad.png`. Jordi: "beter, maar nu lezen de zwarte lijn onder de dneus en de zwarte pixels onder de snor niet zo goed, horen die daar nog? de rest is prima".
Volgens de gids zijn dit binnenlijnen (geen outline shadows tegen de achtergrond), dus in de outline base van het eigen vlak.

- **A (`gnomad_A.png`), zonder zwart:** onder de neus (17..22,33) zwart → 6 (donkerroze, outline base van de neus; scheidt de roze neus van de crème snor). Onder de snor (13..17,38) zwart → e (bruin, outline base van de snor), zelfde tint als de rest van de snoronderrand; eronder ligt de huid/arm al in 6/7. Zwart 198 → 187 (13,0 % → 12,3 %).
- **B (`gnomad_B.png`):** als A, maar 2 zwarte pixels op de diepste punten: (22,33) rechterhoek onder de neus (schaduwkant) en (17,38) de kier waar snor, arm en lijf samenkomen. Zwart 189 (12,4 %). Op 8× kan (22,33) als stipje lezen.
- Controle (`r11.py`): alleen deze 11 pixels gewijzigd, alleen van zwart, silhouet en palet gelijk; rest diff 0 t.o.v. r10.
- Bestanden: `vergelijk_8x.png` (r10 | A | B), `strook_1x.png` (r10, A, B op 1× en 3×).
