# Regionale Starmie r11

Jordi over r10 (A, de zwarte diagonaal blijft), letterlijk: "hij moet nog smoother, de overgang bovenin is nog niet helemaal goed en rechts is de punt puntiger dan de rest".

- Basis is `sprite_r10/starmie_r10.png`. Bouw: `python3 sprite_r11/bouw.py` (vanuit `starmie/`).
- Zones gelijk aan r10: zone 1 = x36–46, y10–20; zone 2 = x44–57, y20–26.
- Asserts in het script: oude index per pixel, silhouet gelijk (alpha-diff 0), diff 0 buiten de zones.
- Palet ongewijzigd. **Silhouetwijzigingen: 0.**

| | gewijzigd t.o.v. r10 | buiten de zones |
|---|---|---|
| `starmie_r11.png` (A) | 9 px | 0 |
| `starmie_r11_B.png` | 10 px | 0 |

## Zone 1: achterpunt rechtsboven ("smoother", "de overgang bovenin")
**In beide varianten**
- **Lichtband (5) langs de bovenrand:** de rechtergrens loopt nu gelijkmatig diagonaal. Het eind per rij is x43, 42, 41, 40 (rij 11–14); in r10 was dat 43, 42, 41, 39, met een knik.
- **Uitloper:** de band loopt met één pixel (38,15) uit.
- **Gewijzigd:** (40,14) 4→5 en (38,15) 4→5. Niets vervaagd en geen chips weg.

**Aansluiting bovenin**, waar de selout van de achterpunt de voorste-sterlijn raakt. In r10 zat daar een dikke knoop van 2 px: (37,13), (38,13) en (38,12) waren allemaal 2.
- **A:** (38,13) 2→5. De trap wordt 3-2-2-1 (rij 10–13) en eindigt op (37,13), tegen de zwarte lijn (36,13).
- **B:** (37,13) 2→5. De trap eindigt op (38,13) en raakt de zwarte diagonaal schuin op (37,14).

**Grens licht→donker** (start van tint 3 per rij 11–18: 45, 45, 44, 44, 44, 43, 43, 43): ongewijzigd. Dat zijn al gelijkmatige stappen van 2–3 rijen.

**Is de achterpunt puntiger dan de andere achterpunten?** Nee, er is geen behandeling nodig.

| | breedte op 1 / 2 / 3 px van de tip |
|---|---|
| achterpunt rechtsboven (rij 10 / 11 / 12) | 4 / 7 / 9 |
| achterpunt linksboven (rij 9 / 10 / 11) | 3 / 5 / 8 |

## Zone 2: tip rechter voorarm ("rechts is de punt puntiger dan de rest")
**Het silhouet is gelijk aan dat van de linker voorarm:** de breedte op 1/2/3 px van de tip is links (x4/5/6) en rechts (x56/55/54) 3/5/7. Op x54 telt rechts 8, door de onderrand op rij 28 buiten de zone, net als in r9.

**Het verschil zat in de tinten.** De lichte rand was rechts maar 1 rij dik tot in de tip en het tipeinde was donker (4/3/3, met een zwarte hoek). Daardoor las de tip als een spits.

| lichte pixels (4–6) per kolom | 1 / 2 / 3 px van de tip |
|---|---|
| links (x4 / 5 / 6) | 0 / 3 / 4 |
| rechts, voor (r10) | 0 / **1** / 4 |
| rechts, na (r11) | 0 / **3** / 4 |

**Gewijzigd in beide varianten**
- (53,23) en (54,23) 4→5: de lichte rand is nu 2 rijen hoog tot in de tip, zoals links op rij 22–23. (51,23) bleef 5.
- Tipeinde x55, rij 22–24: 4/3/3 → 5/4/4. Dat is de spiegel van links (5/5/4), één tint donkerder voor de schaduwkant.
- Hoek (55,21) 1→2: selout zoals links op (5,21).

**Alleen in B:** (56,22) 1→2. De tipkolom wordt dan 2/1/1, precies zoals de linker arm op (4,22–24). In A blijft hij 1/1/1 (de schaduwkant helemaal zwart).

## Vel
`vel.png`:
- r11 | r10 op 8×, met de wijzigingen blauw omkaderd;
- zone 1 op 16×: r10 | r11 | r11_B | achterpunt linksboven;
- zone 2 op 16×: r10 | r11 | r11_B | linker voorarm gespiegeld;
- 2× en 1× op wit en donker: r11 | r11_B | r10.
