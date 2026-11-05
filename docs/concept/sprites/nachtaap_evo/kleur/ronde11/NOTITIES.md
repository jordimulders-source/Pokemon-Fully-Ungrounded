# Nachtaap fase 2: kleursprite ronde 11 (drie lichte tapse wiggen)

Basis is ronde 10. De ogen (Jordi: "ogen zijn zeer sterk") en alles buiten de rug zijn bevroren.

Jordi over het lijf: "ik vind de strepen er toch niet lekker uitkomen" en daarna "tapse wiggen licht zie ik wel zitten".

## Bewijs (`bron/diff_uitvoer.txt`)
- **Alpha-diff:** 0 (1459 px, zowel tegen de `.txt` als tegen de `.npy`).
- **Open randen:** 0.
- **Palet:** gelijk aan ronde 10.
- **Diff buiten de rug (x 15–49, y 24–50):** 0. In de rug zijn 106 px gewijzigd.
- **Restjes van de oude kené:** 0 (de kené-laag is uit het raster geschrapt).
- **Wigpixels:** 112. Daarvan vallen er 29 buiten de projectie, alleen door verdikking langs dezelfde middenlijn.

## Loop = `silhouet/wiggen_64.npy`
De wiggen staan per rij met de hand in `bron/wiggen.py` (`W1`, `W2`, `W3`). Ze beginnen bij de ruggengraat en lopen schuin-recht over de flank omlaag naar een punt.

| Wig | Rijen | Breedte per rij | Bovenaan | Tot 2/3 | Punt |
|---|---|---|---|---|---|
| voor | y 26–38 | 6 8 8 7 6 6 3 3 3 3 3 2 1 | 6 px | ≥ 3 px | 1 px |
| midden (de langste) | y 27–40 | 4 4 4 4 3 3 3 3 3 3 2 2 1 1 | 4 px | ≥ 3 px | 1 px |
| achter (de kortste, op het achterlijf) | y 34–38 | 4 3 3 2 1 | 4 px | ≥ 3 px | 1 px |

- De eindpunten liggen dus op y 38, 40 en 38.
- **Een trede halverwege:** niet gedaan. Op 1× las een verspringing van 1 px als hapje.
- **Bovenkant:** waar de projectie op de bovenste omlijning ligt, blijft de omlijning staan. Tussen de voorste en de middelste wig zit bovenaan 2 px vacht; in de projectie begonnen ze ook los van elkaar.

## Kleur (patroonregels)
- Vlak maanzilver (idx 15) aan de lichtkant, vlak lila (idx 6) waar de wig in de lijfschaduw komt.
- Geen bevel.
- 1 px basis (idx 4) tussen wig en vachthooglicht.

## Lessen
- **Een tapse wig leest pas als hij bovenaan ≥ 4 px is en lang ≥ 3 px blijft.** De punt is alleen het laatste stuk (2 → 1 px). Begint de taper meteen, dan wordt het weer een streepje.
- **Waar twee wiggen in de projectie bovenaan bijna raken:** schuif de bovenste rij 1–2 px in, zodat er vacht tussen blijft. Anders lezen ze als één vlek.
