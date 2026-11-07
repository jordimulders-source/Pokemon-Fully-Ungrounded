# Eindkeuring 2 potoo: uitvoering na de 35 reparaties (7 nov)

Gekeurd: `eind_r1/potoo.png` (12 kleuren, 1242 px). Alleen uitvoering; ontwerp, vorm, oog, muil, klauwen en snorharen zijn door Jordi goedgekeurd en niet gekeurd.
Vergeleken op 8× en 1× (licht, gras, donker) met Gen 3 Noctowl, Xatu, Swellow, Swablu, Dusclops (`anim_front_gba.png`) en Drifloon. Bronnen: SPRITE_KERN, Dragonfly Cave-gids (schaduw iets naar blauw, outline-highlights, geen lichte stippen buiten de lijn), FAKEMON_CHECKLIST E1–E3. Ook het model (`model/model_lijf_20.png`) bekeken: de grijze haartjes boven op de kop (y1) en rechts (snorharen, (39,3)) staan in het model en zijn geen fout.

Bestanden: `keurvel.png` (8× naast de referenties, 1× op wit, gras en twee donkere tinten), `metingen.txt` (paletten met L/H/S, tintvlakjes), `proef.png` (links nu, rechts met de reparaties hieronder, rood omkaderd; de sprite zelf is niet gewijzigd). Scripts: `keurvel.py`, `proef.py`. Coördinaten (x,y) op het 64×64-vel, indexen volgens het palet van de sprite.

## Metingen
| Punt | Uitkomst |
|---|---|
| Helderheidsstappen wit/grijs (8..1) | L 250/220/189/155/126/94/53/10: stappen 30–41 (Swellow 30–40, Swablu 24–30). **PASS** |
| Helderheidsstappen muil (12,11,10,9) | L 132/102/77/52: 25–30. **PASS** |
| Kleurtemperatuur | Licht warm (H46–60), schaduw koel (H240–255), zoals de gids en Swablu/Dusclops. **PASS** |
| Tinten per groep | Veren 8/7/6, tekening 5/4/3, lijn 2/1, muil 12/11/10 + 9. **PASS** |
| Aandeel L<40 | 0,16 (Swellow 0,12, Drifloon 0,17). **PASS** |
| Tintvlakjes < 3 px | 148 (Xatu 168, Noctowl 254, Swellow 332); vrijwel alle zijn spikkels van de tekening. **PASS** |
| Lichte kleur op de buitenrand | Geen 5–8/12 op de rand. **PASS** |
| Pillow shading | Nee; linkerflank licht tot de selout. **PASS** |
| Vorige reparaties | Borstboog, stippen, taps binnenlijn, kop rechts, kin en staartpunt zijn goed uitgevoerd; niets nieuws kapot. Alleen de borstovergang mist links nog de 7 (punt 5). |
| Leesbaarheid 1× | Scherp op wit en op donker; oog, muil en houding lezen direct, op niveau van Noctowl/Swablu. **PASS** |

## Reparaties (op belang)
1. **Buitenlijn kop rechtsboven: 1-2-1 om en om.** Langs de rand (35,2)1 (36,2)1 (37,3)**2** (38,3)1 (40,4)1.
   - (37,3): 2 → 1
2. **Open buitenlijn aan de schaduwkant tussen de snorharen.** Van (41,7) tot (42,11) is de lijn niet zwart; (42,9) is een grijze 4 op de rand die niet bij een snorhaar hoort. De snorharen zelf blijven.
   - (42,9): 4 → 1
3. **Linkerbuitenlijn onderaan de flank: dubbel dik (x21 én x22 op y38–39) en één zwarte (1) tussen de selout-2'en** (lichtkant, 2-2-1-2-2).
   - (22,40): 1 → 2
   - (22,38): 2 → 8, (22,39): 2 → 4 (flank licht tot de lijn zoals erboven; zachte stap naar de buikschaduw)
4. **Vleugel rechts: nog banding.** Over y33–40 lopen 6 (x43) en 5 (x44) als twee evenwijdige kolommen langs de rechte buitenlijn. Laat de 5 later beginnen en onderaan breder worden (sikkel):
   - (44,33) (44,34) (44,35): 5 → 6
   - (43,46) (43,47): 6 → 5
5. **Borst/buik links: 8 grenst nog direct aan 4/6 (de 7 van reparatie 1 loopt alleen van x29 tot x32), waardoor de schaduwgrens als donkere naad leest.**
   - (24,40) (25,40) (27,40): 8 → 7
   - (24,41) (25,41): 4 → 6
6. **Lijn onder de kop (y19–21) eindigt aan de lichte kant met de donkerste tint**: 2 op (38–39,19), 5 in het midden, 2 op (34,21). Taps laten uitlopen:
   - (34,21): 2 → 4

Totaal 16 pixels, alleen indexwissels binnen het palet; silhouet, oog, muil, klauwen en snorharen blijven gelijk. `proef.py` controleert elke oude waarde.

## Ter info voor Jordi
- De vleugelrand rechts (x45, y31–48) is een kaarsrechte verticale lijn van 18 px; Gen 3 zou daar een lichte boog tekenen. Dat is een vormwijziging, dus jouw keuze.

Oordeel: REPARATIES
