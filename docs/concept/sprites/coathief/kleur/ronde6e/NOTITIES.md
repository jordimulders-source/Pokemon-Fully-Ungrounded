# Coathief: kleursprite ronde 6e (de curve van de nabije voorpoot volgens de onderlaag)

Basis: ronde 6d.
- Jordi over 6d: "het is dichterbij, maar de vorm mag iets geleidelijker aan lopen" (krabbel `referenties/krabbel_jordi_belijning2.png`).
- Aanvulling: "mijn lijn is een indicatie he, onderlaag heeft de correcte lijn".
- **De maatstaf is dus de zwarte omlijning van de onderlaag**, verkleind naar 64. De krabbel geeft alleen de richting aan.

## Bestanden
- `coathief.png`
- `vel.png`
- `uitsnede.png`
- `onderlaag_6d_6e_voorpoten.png`: de voorpoten op 8×, met de onderlaag, 6d en 6e naast elkaar, op licht en op donker, plus 1×.
- `onderlaaglijn_over_6e.png`: de controle. De zwarte omlijning van de onderlaag (blauwe stippen, luma < 30, verkleind 4:1) ligt op 20× over 6e.
- **Silhouet:** `../../silhouet/ronde6.txt` (1328 px, 2 px meer dan ronde5), gemaakt door `bron/silhouet_ronde6.py`.
- `bron/`:
  - het blok "ronde 6e" staat onderaan `reparaties.txt`;
  - `onderlaag_lijn.py` maakt de controle-overlay;
  - `diff_r6d.py` is de diff tegen 6d;
  - `controle.py`.

## Bewijs
```
controle.py: pixels 1328 | silhouet 1328 (ronde6.txt) | alpha-diff 0 | open randen 0 | losse pixels 0
diff_r6d.py: zone x 17-34, y 46-59  28 px | buiten de zone: 0
```

## De curve (afgelezen van de onderlaag)
Positie van de onderlaaglijn per rij, en het pixel in 6e:

| y | onderlaaglijn x | 6e | |
|---|---|---|---|
| 45–47 | ≈ 33 | d-contour x 33 in het lijf | (32,46) is nu b, zodat de arm breder wordt |
| 48–49 | ≈ 31,5–32 | k op x 31 | silhouetrand |
| 50–52 | ≈ 31,5 | k op x 32 | silhouetrand, ≤ 0,5 px |
| 53 | ≈ 30,8 | (31,53) | |
| 54 | ≈ 30 | (29–30,54) | |
| 55 | ≈ 28 | (27–28,55) | |
| 56 | ≈ 24,5–26,5 | (24–26,56) | onderkant van de manchet |

- Segmenten: eerst verticaal (x 32, 3 rijen), dan 1, 2, 2 en 3 naar links. Dat is één geleidelijke boog, zonder hoek of trap.
- In 6d was het een horizontale knik van 3 px op y 54 met een korte trap eronder.
- De overlay laat zien dat de blauwe lijn over de k-pixels van 6e loopt.

**Silhouet:** (26,55) en (26,56) zijn erbij gekomen. Daar ligt de onderkant van de manchet op de onderlaag. De krabbel suggereerde ook (32,48–49) en (25,57), maar daar ligt de onderlaaglijn niet: die pixels zijn niet toegevoegd. Tussen de poten blijft lucht op y 57 (x 24–26).

## Kleur
- **Nabije bovenarm (vacht):** rustiger dan in 6d. Er is één l-pixel (27,50) als lichtkant langs de naad, verder b, en d langs de curve. De oranje hooglichtvlek is weg.
- **Bruin en manchet:** het bruin loopt tot y 53, zoals op de onderlaag (x 27–30 → 28–30). De naad naar de donkere manchet ligt op 26|27 (y 50) en 27|28 (y 51–53), de grens die de onderlaag laat zien.
- **Manchet:** groter en rond, in de nabije tinten, met Y/y linksboven. De onderkant (24–26,56) is k.
- **Verre poot:** komt pas onder de curve tevoorschijn. Slagschaduw m op (31,54), (29,55) en (27,56), daarna de schaduwtinten met de lichtkant y.

## Toets (1× en 8×, licht en donker)
- De nabije poot ligt vóór de verre, met een vloeiende, geleidelijke curve die samenvalt met de onderlaaglijn.
- De verre poot draagt eronder.
- Ik zie geen zwak punt.

## Les
- Een krabbel van Jordi is een richting. Leg de echte omlijning van de onderlaag verkleind over de sprite: drempel op zwart, 4:1, als stippen op 20×. Kies per rij het pixel waar die lijn doorheen loopt.
