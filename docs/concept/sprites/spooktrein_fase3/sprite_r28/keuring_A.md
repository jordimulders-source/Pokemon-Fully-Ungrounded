# Strenge eindkeuring r28A (zachtere binnenlijnen), 16 nov

Vel: `vel_r27_r28A_r29.png` (r27 | r28A | r29, op 8×, 2× en 1×).

## Oordeel
- **r28A: PASS met 1 px reparatie.** Het resultaat is **r29** (`sprite_r29/sprite.png`, met `_8x`), via `sprite_r29/fix29.py`.
- Diff r28A→r29: 1 px. Kleuren: 16 indexen (0–15), dus binnen de grens.

## Leesbaarheid (1×, 2×, 8× tegenover r27)
- **Ogen:** lezen op alle schalen. De wenkbrauw- en kasranden in idx 15 staan tegen groen 2 (Δ160) en tegen roest 8 en 14 (Δ80/106). Zo blijft de vorm scherp, en het "opgeplakte" uit r27 is minder.
  - Het rechteroog verliest aan de rechterbovenrand iets aan de donkere sikkel 9 (Δ18). Dat leest als schaduw, niet als een fout.
- **Grijnsrand:** blijft scherp. Idx 15 staat daar tegen 2 en 3 (Δ160/118).
- **Naden en spleten in de koeienvanger:** lezen. Ze staan tegen 7 (Δ156), 10 (Δ130) en 11 (Δ80).
  - Op 1× is de kop zachter, maar niet vaag.

## Metingen (r27 → r28A)
| | r27 | r28A |
|---|---|---|
| Zwakke tintgrenzen (< 20 lum), alles | 1,8 % | 5,3 % |
| Zwakke tintgrenzen, zone | 1,1 % | 8,3 % (Gen 3: 0–9 %) |
| Zwart-aandeel | 0,106 | 0,035 |
| Donker-aandeel (lum < 60) | 0,173 | 0,173 |

- **Buren van idx 15 (lum 40):**
  - 9: 72× met Δ18. Dit zijn de enige zwakke grenzen. De lijn loopt over in de eigen schaduwtint, zoals een Gen 3-binnenlijn hoort te doen.
  - 1: 9× met Δ15. Dit zijn alleen T-aansluitingen op de buitenlijn.
  - 12: Δ39, 6: Δ58, 11 en 8: Δ80, overige buren ≥ 95.
- **Lijnen:**
  - De buitenlijn grenst aan transparant en blijft dus zwart. Aan de schaduw- en onderkant zijn dat de 20 zwarte zonepixels. De lichte kant houdt de selout 9.
  - Zwart en 15 wisselen nergens om en om. Op de onderrand van de koeienvanger (y55) loopt 15 boven groen en zwart boven de spleet naar transparant. Dat is logisch: het zwart staat alleen waar de vorm naar lucht gaat.
  - Er staan geen losse zwarte pixels midden in een lijn van 15.

## Reparatie r29
- **(32,43): idx 15 → 1.** De zonegrens x=33 knipte de onderlijn van de wagenplaat (x32–38). Daardoor begon een zwarte lijn met 1 px van 15.

## MAG (geen reparatie)
- **Overgang bij de schoorsteen (23,20)/(24,19):** de schoorsteenlijn (buiten de zone) blijft zwart, de koplijn eronder is 15. Dat valt op een vormgrens en hoeft niet veranderd te worden.
- **15 tegen 9 (Δ18):** maak je 15 donkerder, dan wordt hij weer hard. Laten zo.
