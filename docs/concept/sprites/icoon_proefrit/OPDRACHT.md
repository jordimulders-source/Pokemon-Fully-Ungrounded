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

## Bijsturing Jordi (28 nov)
- Poliwag: "poliwag oke, maar de spiraal klopt niet, tov de normale poliwag" → spiraal pixel voor pixel uit het originele icoon, omgekleurd (`poliwag_regional/icoon/spiraal_E.png`).
- Bak A alleen bij gelijke vorm: "voor poliwag kan je prima het icoon overnemen, maar poliwhirl en wrath zijn echt andere designs dus daar gaat dat niet lukken" → regional forms met een ander ontwerp gaan naar bak B/C.
- Shuppetto r1 afgekeurd: "ziet er vreselijk uit" · "hij is niet driekwart en lijkt op een soort verlepte versie van zichzelf" · "maar dat komt omdat je weer zelf aan het tekenen bent" · "dat moet echt verboden worden". Regel in `docs/lessen/ICOON_WERKWIJZE.md`.
