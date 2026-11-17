# r11 (16 nov): 14 px uit `eindkeuring/KEURING_r10.md` op r10 (hoofdversie en plaatlicht-variant)

Script: `maak_r11.py`. Per pixel is met een assert gecontroleerd dat de oude waarde klopt. Diff buiten de 14 px = 0, silhouet gelijk (bewezen in het script). De lijst per pixel staat in `pitahaya2_r11_afwijkingen.txt`.
- Verre lip p → r (8 px): (19,48) (18,49) (19,49) (17,50) (18,50) (19,50) (16,51) (17,51).
- Mondhoek p → r (1 px): (19,43).
- Sikkelplak d → r (5 px): (24,48) (25,48) (26,48) (27,48) (26,49).

Controle:
- Nieuwe dambordjes: 0.
- **Nieuwe losse pixel: (27,49) d.** Zijn buren (26,49) en (27,48) werden r. Rij 49 leest nu `dddddd r d` (x 20–27). Niet aangepast, want hij valt buiten de opdracht. Voorstel: (27,49) d → r, of (26,49) laten staan als d. De keurder beslist.

Bestanden:
- `pitahaya2_r11.png` en `pitahaya2_r11_plaatlicht.png`
- `*_8x.png`: 8×, nearest neighbour
- `vel.png` (`vel.py`): r10, r11, r11 plaatlicht en model op 8×, de bek op 12× (model, r10, r11), en 1×/2× op licht en donker naast Salamence en Lairon
