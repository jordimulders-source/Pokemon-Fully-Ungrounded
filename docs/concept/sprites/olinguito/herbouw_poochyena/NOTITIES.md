# Olinguito fase 1 – herbouw op Poochyena (24 okt)

Basis: `graphics/pokemon/poochyena/anim_front.png` als geheel als onderlaag (kop-constructie, lijf, vier poten, sprongpose, 3/4-hoek). Daarover met de hand de olinguito getekend, rij voor rij (`bron/teken_v1.py` t/m `v6.py`, elke volgende versie overschrijft alleen benoemde pixels). Palet = `ronde23/normal.pal` (ongewijzigd). Geen vormfuncties; `stap0_herkleurd.txt` is de basis alleen als naslag.

Bestanden: `anim_front.png` (64×128, 2 frames, index 0 transparant), `normal.pal`, `onderlaag.png` (basis | basis vaag + rood = mijn omlijning, blauw = nieuw buiten de basis | resultaat), `compare.png` (resultaat, basis, ronde 23, Galar-Linoone; 1× en 3×), `bron/` (rasters, scripts, uitsnedes `zelfcheck_*.png` op 8×). Frame 2 = romp en kop 2 px omlaag (zoals Poochyena's frame 2, kleiner), poten en staartpunt blijven staan.

## Wat er van de basis bleef / veranderde
- **Kop:** Poochyena-kop (snuit naar links, neus links voorop, één oog, kop iets omlaag). Spitse oren → kleine ronde oren met crème binnenkant (ver oor links kleiner, nabij oor rechts groter). Masker: donkere band rond het oog, over de neusbrug tot net boven de neus, golvende rand (boven: brug lager → boven het oog hoger → achter het oog weer lager; onder: lob onder het oog). Licht boogje (6-7-8-8-7-6 + eindjes) direct op de bovenrand boven het oog. Oog in ronde16-stijl (bovenlid 1, oranje/goud iris, glans). Crème snuit/kaak/wang; scheve grijns (mondlijn met één omhoog gekrulde hoek + één tandje), geen tong.
- **Lijf:** Poochyena-pluk en gekartelde vacht weg; de rug volgt nu een ronde boog op de plek van de pluk (anders werd het een wezel). Rompomtrek verder als de basis; achterhoofd en romp achteraan rond gemaakt.
- **Poten:** positie, hoek en volgorde van de basis. Alleen rechte stukken weggewerkt (borst/voorpoot schuin, hak aan de achterpoot, rechterrand verre voorpoot, zolen ≤ 3 px op één na).
- **Klauwen:** 2 per voorpoot, Sandslash-stijl (wit/lichtgrijs blad, grijze binnenlijn, donkere omlijning, gebogen punt); de verre voorpoot kleiner en grijzer.
- **Staart:** hangende J vanaf de bovenkant van de heup (waar Poochyena's staart aansluit): naar rechts, in een boog omlaag (segmenten 1-2-3-4-3-2-1, geen rechte stam), onderaan terug omhoog met een ronde crème punt, deels achter de nabije achterpoot.

## Zelfcheck per onderdeel (8×, `bron/zelfcheck_*.png`; `bron/check.py`)
| Onderdeel | Vast aan lijf | Rechte lijn ≥ 4 | Dikte vs tegenhanger | Opmerking |
|---|---|---|---|---|
| Kop | ja, overlapt de borst (B6) | nee (achterhoofd gebogen 1-2-2-1) | n.v.t. | 3/4 zoals de basis: snuit één vorm naar links-voor, één oog; kop draait meer naar de kijker dan het lijf (B1) |
| Voorpoot dichtbij | ja | nee | ±6 px, gelijk aan verre voorpoot | vooruitgestoken, hoogst-links (in de sprong) |
| Voorpoot ver | ja, onder de borst | nee | ±6–7 px | laagste voet (draagt), schaduwtint, kleinere grijze klauwen |
| Achterpoot dichtbij | ja | nee (hak naar achteren) | ±6 px | |
| Achterpoot ver | ja | n.v.t. | — | alleen als donker stukje dij tussen voorpoot ver en achterpoot dichtbij, zoals in de basis |
| Staart | ja, aan de bovenheup | stam en binnenrand 4 (top van de boog) | — | J leest; het gaatje van de J is klein (2 px) |
- **Diagonaal:** voorpoot dichtbij vóór + achterpoot ver vóór (onder de buik); voorpoot ver + achterpoot dichtbij achter: diagonale paren, geen telgang. Dit is de Poochyena-constructie zelf.
- **Open randen:** 0 in beide frames (`check.py`). Omtrek-runs ≥ 4: alleen de staartboog (4) en twee zolen (4).
- **Meting:** 1182 px, box 54×38, kop ±53% van de hoogte, donker aandeel 0,27 (Dark, mag).

## Checklist (FAKEMON_CHECKLIST / SPRITING §0)
A1 ok (marterachtig dier met maskergezicht; leest niet meer als Poochyena) · A2 ok (J-staart + masker) · A3 ok (kop linksboven, staart rechts als tegenwicht) · A4 ok (lucht tussen alle poten, J-gat) · A5 ok · A6 ok op de rug na (boog, geen doos) · B1 ok · B2 ok (lange snuit → één oog, neus meest links) · B4 ok · B5 ok · B6 ok · B7 ok · C1 deels: verre achterpoot alleen als dij zichtbaar (zoals de basis) · C2 sprongpose, voethoogtes 3 · C3 ok · C4 ok · C5 ok · C6 ok (verre voorpoot in schaduw, grijzere klauwen) · C7 ok (verre voorpoot draagt) · C8 ok · D1 **te groot** (1182 > 1050) · D2 ok · D3 matig (zie onder) · D4 54 breed (> 48; staart) · E1–E3 ok. §0: 1 ok, 2 ok, 3 ok, 4 ok, 5 ok, 6 zie D1, 7 ok.

## Eerlijk oordeel
- Leest op 1× en 3× als een echt dier/Pokémon in een natuurlijke sprongpose; geen Escher-poten, kop natuurlijk 3/4. Duidelijk beter gebouwd dan ronde 23.
- **Maar:** het oogt eerder als een fase 2 dan een fase 1: het lijf is lang (wezel/fret-achtig) en de kop is relatief klein naast ronde 23. 1182 px, 54 breed. Als Jordi het compacter wil: de staart strakker oprollen en de romp achteraan 3–4 px inkorten (wel een afwijking van de basis).
- Het masker is een brede donkere band; de mondlijn eronder geeft samen twee donkere strepen in het gezicht. De snuitpunt is vrij plat/hoekig.
- Klauwen zijn herkenbaar als twee witte haakklauwen; op 1× zijn ze klein maar zichtbaar.

## Lessen
- Een echte sprite als geheel als onderlaag geeft meteen een kloppende pose; de enige valkuil is wat je weghaalt: Poochyena's pluk bepaalde het rugvolume, zonder die pluk werd het lijf een lange plank. Volume terugzetten met een ronde rug.
- Bij het wissen van een gebied (claws opnieuw) altijd de rijen beperken: een te ruime wisrechthoek sneed een stuk van de voorpoot weg (v3), pas zichtbaar in de open-randen-check.
- `check.py` (open randen + rechte omtrek-runs) na elke stap draaien scheelt veel kijken.
