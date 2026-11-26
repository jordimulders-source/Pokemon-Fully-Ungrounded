# Eindkeuring ronde 2: gaucho-Ludicolo (26 nov)

Basis: `../af/ludicolo_gaucho.png` (= `../eindkeuring/mond_V2.png`): eindkeuring 1 (`../eindkeuring/KEURING.md`) + Jordi's keuzes daarna: ogen wit (irispixels → wit, oog B, `oog_wit.py`) en snavel omlijnd (rode lijn eromheen, onderkant zwart als outline shadow, `mond_lijn.py`). Model: `../r6/gemini_r6.png`. Familie: `../../af/lotad_gaucho.png`, `../../lombre/af/lombre_gaucho.png`.
Resultaat: `ludicolo_gaucho_e2.png` (64×64, P, index 0 transparant), `ludicolo_gaucho_e2_8x.png`, `vergelijk.png` (voor | na | model op 8×, gezicht op 20×; 1× en 2× op licht en donker naast gaucho-Lotad, gaucho-Lombre, Dundragoon, Skinguin, Zapacha en Princadee).
Scripts: `e2.py` (alle wijzigingen met asserts op de oude index → `e2_uitvoer.txt`), `controle.py` (→ `controle_uitvoer.txt`), `vel.py`.

## Gids (`dragonflycave_spriting_guide.txt` r. 80–170, 340–470)
"The 'outline shadows' are always black (or ever-so-slightly off-black) on Pokémon sprites"; "the relative luminosity of the shades on the original sprite should always be maintained"; "The outline base and outline highlight colors are also colors. When you're recoloring, you must also recolor the outlines"; "we take the base outlining shade for every color and color all of the outline except the shadows in that color, and remove the clusters so that the outline is always one pixel wide"; "place pixels of the outline highlight color on the inside of the outline rather than the outside".

## Getoetst en goed gelaten
- **Ogen (diff 0):** wit (255,255,255) = het wit van gaucho-Lotad en gaucho-Lombre. Lotad-oog = wit met zwarte stip, zonder eigen zwarte ring: het wit ligt direct tegen de huidtint (Lotad `af/` (19–20,40–41)). Bij de Ludicolo ligt het wit op dezelfde manier direct tegen de olijf maskertinten, het rood en (linkeroog onder) het snavelgeel; dat is dezelfde opbouw, dus geen ring toegevoegd. Pupillen 1×2 zwart, geen wit in de pupil.
- **Bovenkant snavel tussen de ogen** ((23,26), (24,26) rood donker): niet tot rode lijn gemaakt, want rij 25 erboven is al rode lijn (dan 2 px dik).
- **Kleurtinten:** palet ongewijzigd t.o.v. eindkeuring 1 (+ wit op 15). Rood licht (7) wordt niet meer gebruikt (zat alleen in de oogglans, nu wit); slots 7 en 14 vrij.
- **Schaduw:** sinds ronde 1 niet veranderd; niets aangeraakt.

## Belijning snavelrand (15 pixels, alleen indexwissels; alpha-diff 0, ogen diff 0)
`mond_lijn.py` maakte rode pixels naast het geel tot rode lijn en die direct onder het geel tot zwart, maar sloeg pixels over die al rode lijn waren. Daardoor: onderkant half zwart, half rood; rechts zwart en rood om en om; drie verdikkingen.
| pixel | was → nu | reden |
|---|---|---|
| (18,27) | zwart → geel donker | 2×2-lijncluster (17–18, 27–28); het model is hier geel (225,158,83), het bovenste snavellobje loopt t/m rij 27 |
| (18,28) | rode lijn → zwart | onderkant van dat lobje, zwart zoals (19,28) ernaast (onderkant zwart) |
| (16,30) | rode lijn → rood diep | 2 px lijn naast de buitenlijn (15,30); terug naar de tint van vóór mond_lijn |
| (34,31) | rode lijn → rood donker | L-verdikking met (33,31) en (34,32); model (147,72,52) = rood donker |
| (34,29), (33,30) | zwart → rode lijn | rechterzijkant liep rood-rood-zwart-zwart-rood-rood-rood: zijkant nu doorlopend rode lijn (Jordi: "rode lijn eromheen") |
| (32,34), (31,35), (30,35), (24–29,36) | rode lijn → zwart (9) | onderkant snavel: x18–23 was al zwart, de rest nog rood; nu doorlopend zwart van (18,33) tot (33,34) (Jordi: onderkant zwart als outline shadow) |
Uitkomst (`controle.py`): 2×2-lijnclusters rond de snavel 0 (was 1); onderrand zwart 34 / rood 2 (de 2 rode = de hoekpixels (34,29), (33,30) van de rechterzijkant); zijkanten 14× rode lijn, 0× zwart. Zwart-aandeel 16,2 % → 16,6 %.

## Ter info voor Jordi (niet gewijzigd)
1. **Band boven de ogen** (x23–27, y23–25): zwarte hoedrandlijn + 2 rijen rode lijn = 3 px donker. In ronde 1 is dezelfde slagschaduw elders rood diep geworden (S1), hier niet omdat het in het bevroren gezichtsvak ligt. Rij 25 (x23–26, model ML 67–70) zou volgens S1 rood diep worden. Idem rechts van het rechteroog (34–35, 24–25): zwart boven rode lijn. Alleen als je dat wilt.
2. **Rechterkant snavel zwart** zou ook kunnen (de Gen 3-Ludicolo heeft zwart rechts en onder om de snavel en bruin links/boven); gekozen is rood, omdat jij "rode lijn eromheen, onderkant zwart" koos.
