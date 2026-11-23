# Gnometrotter Rock: sprite r7b (23 nov)

Basis = r7; alleen linkerarm/vuist en rugrots aangepast, de rest is bevroren (pixeldiff 0 erbuiten). Script: `r7b.py`, meting `meet6.npz` en dekking `dek.npy` (gedeelde geometrie).
Leveringen: `gnometrotter_rock.png` (palet byte-gelijk aan r7), `gnometrotter_rock_8x.png`, `naast_model.png` (r7b | r7 | model, 8×), `uitsnede_12x.png` (arm boven, rots onder; sprite | model met spritepixelraster). Losse pixels: 0.

## 1. Linkerarm + vuist (14 px anders dan r7, waarvan 6 silhouet)
- **Elleboog:** in r7 scheidde een lijn op (16,30) en (16,31) de onderarm van de bovenarm. In het model zijn die pixels roze arm, met de binnenhoek van de elleboog erdoorheen. Nu zijn ze vlak (8), dus onder- en bovenarm vormen één gebogen arm: van de vuist naar rechts en dan omhoog naar de schouder onder de baard.
- **Tinten van de arm:**
  - bovenkant onderarm f
  - midden 8 (ook (13,32) en (13,33), voorheen f)
  - onderkant en bovenarm 7: de schaduwzijde onder de baard
- **Vuist ronder en groter dan de arm** (model: bal tot rij 29,6 boven en 36,5 onder). Silhouet erbij, met dezelfde drempel 0,2 als de armboog van r7:
  - (7,29) en (8,29): modeldekking 0,25 en 0,22, lijn 6
  - (2,34) en (2,35): 0,38 en 0,32, zwart
  - (3,36): 0,45, zwart
  - (12,36): 0,23, zwart
- **Pixels die daardoor binnen de vuist kwamen:** (7,30) en (8,30) zijn nu f, (3,34) en (3,35) zijn nu 7.

## 2. Rugrots (4 px anders dan r7)
- **Tinten per pixel uit de gemeten modelhelderheid** (5 ≥ 140, 4 ≥ 115, anders 3). De knik is alleen nog lijn waar het model daar donker is.
- Daardoor is de lichte voorkant een wig die naar linksonder smaller wordt, zoals in het model:
  - rij 9–11: x 45–47
  - rij 12–13: x 45–46
  - rij 14–15: x 45
- Ook de knik loopt schuin: (47,12) → (47,13) → (46,14) → (46,15).
- Aanpassingen per pixel:
  - (47,10): van lijn naar 5 (gemeten 145)
  - (47,11): van lijn naar 5 (gemeten 130; sluit aan op de wig)
  - (45,11): van 4 naar 5 (gemeten 142)
  - (47,13): van 3 naar knik 2 (grens tussen licht 135 en donker 101 in het model)
- Het silhouet van de rots is niet veranderd: de buitenranden lopen in het model ook vrijwel verticaal (rechts x 49,7 van rij 9 tot 18). Het schuine zit in de voorkant en de knik.

## Wat niet uit het model komt
- De armtinten (f/8/7): een keuze richting Gen 3, licht linksboven.
- De 6 silhouetpixels liggen onder de 50 %-drempel; ze zijn gekozen op modeldekking ≥ 0,2.
- (47,11) is 5 in plaats van de gemeten 4, en (47,13) is knik in plaats van vlak, om losse pixels te voorkomen.

## Eigen kanttekening
- De rots staat op 8× maar iets schuiner dan in r7, omdat het model zelf maar ±2 px helling heeft over 7 rijen. Meer schuinte zou silhouet of knik moeten verzinnen.
