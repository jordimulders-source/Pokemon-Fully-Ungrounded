# Gnometrotter Grass r11 (maker, 23 nov)

Basis `../sprite_r10/gnometrotter_grass.png`. Script `maak_r11.py` (gebruikt de zones van `../sprite_r10/maak_r10.py`; → `gnometrotter_grass.png`, `_8x.png`, `log_r11.txt`, `vel.png` = model | r10 | r11 op 8×).

| Zone | px t.o.v. r10 |
|---|---|
| muts (herverdeling naar de donkere tinten) | 222 |
| losse pixels | 3 |
| bladeren (baard, haar) | 0 px (andere kleur via het palet) |
| rest | 0 (assert) |

- **Indexkeuze:** geen index valt zonder zichtbaar verschil samen (bruin 2–4 en groen 5 liggen ≥ 37 RGB uit elkaar). Daarom neemt de muts de donkere tinten en de bladeren de lichte: muts = hooglicht 13, lijf 12, schaduw/sikkel 5 (linkerblad 14→13, 13→12, 12→5; rechterblad rand 13→12, lijf 12→5); bladeren houden 14/13/12 (licht linksboven / midden / schaduwhelft rechtsonder), nu met een lichte geelgroene ramp zoals het model.
- **Palet:** 14 (150,196,104) → (184,214,120); 13 (110,156,82) → (136,182,92); 12 (72,116,62) → (80,124,64); 5 (38,70,42) → (42,74,44) (iets lichter, zodat het schaduwblad van de muts niet zwart wordt). 0, 1, 2–4, 6–11, 15 ongewijzigd. Het blaadje aan de rugtak (5/13) verschuift mee.
- **Losse pixels:** (18,32), (32,16), (35,14) waren vlakjes van 1 px tussen nerven; de enige passende 4-buurtint is de nerf 5, daarin opgenomen. (32,15) werd al 5 door de mutsverdeling.
- Twijfel: het rechterblad van de muts is nu grotendeels 5 (model: lum ±70–89, donkerst van de figuur); leest donker, maar de nerf tussen linker- en rechterblad valt daar samen met het vlak.
