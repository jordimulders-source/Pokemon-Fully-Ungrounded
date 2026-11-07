# Hatun runa – kleur ronde 2

Basis: `../kleur_r1/raster.txt`. Gereedschap: `stappen/` (kopie van r1, paden naar kleur_r2). Handwerk: `stappen/e_r2.txt`, `stappen/e_poot.txt` + losse pixels (zet.py).
`vel.png`: r2 | r1 | model op 8×, close-ups kop/vleugel 12×, 1× en 2× op licht/donker + model 1× (BOX).

## Wat er veranderde (alleen de zwakke punten uit r1)
- **Staart lichter** volgens de modelmediaan (`rgb.py 42 30 57 46`: veel 5 in het midden/rechts): meer 5 in rij 33–39, tweede scheiding nu (52,38)→(50,40) op de donkere modelpixels; eerste scheiding (52,34)→(46,40) ongewijzigd.
- **Verre dekveren:** lichtere 3-rand net binnen de omlijning linksonder (rij 38–41, x15–19), zoals de modelmediaan (rij 37–41: 3 langs de onderrand, 2 binnenin).
- **Pootjes:** tenen met de grijsbruine highlight van het model (gemeten 128,102,82 → paletkleur E); verre poot 1 highlightpixel (schaduwkant), nabije poot 3–4 (tenen (37–38,59), (37,60)).
- **Palet:** E was donkerrood van de bek (2 px); de bek-donkerrood is nu 3 (model-mediaan (14,52) = 118,57,42, vrijwel gelijk aan 3 = 126,68,42); E = teen-grijsbruin (128,104,84). Zalm D op (15,51) erbij zodat de open bek op 1× rood leest.
- Losse pixels opgeruimd: (36,49) → 7, (25,50) → 8.

## Controles
- Silhouet-diff **0** (971 px, `controle.py`).
- Buitenrand (`rand.py`): alleen (12,48) en (11,49) in donkergrijs B = bewuste selout van de grijze snavel aan de lichtkant (onderkant snavel zwart).
- Kleine clusters (< 3 px) alleen: lijnpixels, veerpunten (5/3), oog (glans (18,48), sikkel, iris), goudvlekje kruin, bekpixels.
- Toon (`toon.py`, sprite vs model 1×): staart 80/91, verre vleugel 66/76, nabije vleugel 92/99, buik 134/142; het verschil komt grotendeels doordat het verkleinde model lijn en achtergrond middelt.

## Afwijkingen van het model (met reden)
1. Verre vleugel: 3 scheidingen i.p.v. ±5 dunne lijnen (opdracht: geen zebra, minder en grotere vormen op de modelplekken).
2. Nabije vleugel: scheidingslijnen donkerbruin en taps (2 bij de inkeping, 3 naar binnen) i.p.v. bijna zwart; zelfde plekken (L1–L8 gemeten).
3. Bovensnavel: lichtkant-selout in donkergrijs B, zwart aan de onderkant (model: overal zwart).
4. Bek-donkerrood = bruin 3 (paletruimte; model-mediaan ligt er vlak bij).

## Open punten
Geen zelfgeziene zwakke punten meer die ik zonder keurder zou veranderen. Ter info: de staart is gevolgd zoals het model (opgezet, rechts); leest op 1× als staart, niet als derde vleugel.
