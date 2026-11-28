# Proefrit party-iconen (28 nov)

Doel: per moeilijkheidsbak één icoon maken en meten hoeveel werk het kost, vóór de massaproductie (±120 soorten).

## Jordi (28 nov), letterlijk
- "Ze hoeven niet perfect te zijn, zolang ze maar niet negatief opvallen. Ik heb nog nooit gedetailleerd naar dat soort icoontjes gekeken in Pokemon games, maar ze moeten wel gewoon kloppen"
- "paletregel blijft streng, Wailmer en Wailord worden ook roze volgens mij" → alleen de 6 gedeelde paletten `graphics/pokemon/icon_palettes/pal0–5`; kleur die er niet in staat = dichtstbijzijnde. Geen nieuw palet.

## Bakken
| Bak | Soort | Front | Onderlaag |
|---|---|---|---|
| A (regional form) | regionale Poliwag (Ice/Poison) | `poliwag_regional/af/poliwag_regional.png` | bestaand icoon `graphics/pokemon/poliwag/icon.png` (pal 0): vorm overnemen, kleuren/kenmerken naar onze front |
| B (evolutie bestaande soort) | Shuppetto (Banette-evolutie) | `banette_evo/af/shuppetto.png` | stijlanker: `graphics/pokemon/banette/icon.png` en `shuppet/icon.png` (oog, tinten, maat); verder onderdelen-methode |
| C (volledig nieuw) | Cuyby | `cuyby/ronde4/anim_front.png` (bovenste 64 rijen = frame 1) | onderdelen-methode zoals de viscacha |

Uitvoer per soort: `<soort>/icoon/` (werkbestanden) en `<soort>/icoon/af/icon.png` + `icon_8x.png` + `icon_anim.gif`, plus `NOTITIES.md` met: onmisbare kenmerken, paletnummer, aantal rondes, wat moeite kostte.
