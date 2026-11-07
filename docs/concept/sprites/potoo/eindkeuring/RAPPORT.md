# Eindkeuring potoo: schaduw en kleuren (7 nov)

Gekeurd: `kandidaat/potoo.png` (12 kleuren gebruikt, 1242 px). Alleen uitvoering van schaduw en kleur; vorm, oog C4 en kleurstelling (wit lijf, blauwpaarse muil, zwart oog) zijn bevroren en niet gekeurd.
Vergeleken op 8× en 1× met Gen 3 Noctowl, Hoothoot, Xatu, Swellow, Swablu, Dusclops (`anim_front_gba.png`) en Drifloon (zwart oog). Bronnen: SPRITE_KERN, Dragonfly Cave-gids (shading, outline-highlights, schaduwen iets naar blauw), FAKEMON_CHECKLIST E1–E3.

Bestanden: `keurvel.png` (8× naast de referenties, 1× op wit en op licht gras), `metingen.txt` (paletten met L/H/S per tint), `markering.png` (reparatiepixels genummerd zoals hieronder). Scripts: `keurvel.py`, `markering.py`. Coördinaten (x,y) op het 64×64-vel; indexnummers volgens `kandidaat/normal.pal`.

## Metingen
| Punt | Uitkomst |
|---|---|
| Helderheidsstappen wit/grijs (8,7,6,5,4,3,2,1) | L 250/220/189/155/126/94/53/10: stappen 30–43. Gelijk aan Swablu (24–30) en Swellow (30–40). **PASS** |
| Helderheidsstappen muil (12,11,10,9) | L 132/102/77/52: stappen 25–30. **PASS** |
| Hue-shift | Licht warm (8 H60, 7 H46 S0,31, 6 H42), schaduw koel (4–1 H240–255), zoals Swablu (lila schaduw) en Dusclops. Middentoon het meest verzadigd, zoals Gen 3. **PASS** |
| Tinten per groep | Veren 8/7/6, tekening 5/4/3, lijn 2/1; muil 12/11/10 + 9. Binnen de norm als je veren en tekening als twee groepen leest (Dusclops gebruikt er 7 grijzen). **PASS** |
| Aandeel zeer donker (L<40) | 0,16 (Swellow 0,12, Drifloon 0,17, band 0,10–0,25). **PASS** |
| Buitenlijn | Zwart (1) rechts en onder; boven de kop selout 4, linkerflank 2, muilrand 9. Geen zwart/lila om en om. **PASS** |
| Contrast wit lijf op lichte achtergrond | De omlijning is overal donker; op 1× op wit en op licht gras staat het silhouet scherp. **PASS** |
| Pillow shading | Nee: de linkerflank is licht tot aan de selout, schaduw alleen rechts en onder. **PASS** |
| Tintvlakjes < 3 px | 147 (4-buren, alle kleuren; Xatu 168, Noctowl 254, Swellow 332). Het aantal is normaal, maar zie 2 en 6: losse donkere stippen in vol licht. |
| Schaduwrichting | Licht linksboven klopt voor kop, muil en flank; de vorm van de schaduw op borst en vleugel klopt niet (1, 4). |

## Reparaties (op belang)
1. **Borst: schaduw is een rechte band, geen sikkel; 8 grenst direct aan 6 (sprong 61, de 7 ontbreekt).** De bovenrand van de 6-buikschaduw loopt vlak over y41/42 van x24 tot x37 en de rechterkant van de borst blijft wit tot aan de binnenlijn.
   - (29,40) (30,40) (31,40) (32,40): 8 → 7
   - (29,41) (31,41) (32,41): 8 → 6 (rechts hoger dan links: de grens wordt een boog)
   - (34,28) (34,29) (34,30) (34,31) (34,32): 8 → 7 (smalle sikkel langs de rechterkant, sluit aan op de 6 op (35,33–35))
2. **Losse donkere stippen (2, L53) midden in vol licht wit (contrast 197).** Ze lezen op 8× als vuil, niet als spikkel in het licht. Spikkels blijven, alleen lichter waar het licht valt:
   - (25,29) (24,30) (31,33) (32,33) (31,38) (25,39): 2 → 4
   - (33,40) (30,41): 2 → 3
3. **Binnenlijn borst/vleugel (x35 y28–32, x36 y33–36) is overal 2, even dik, niet taps.** Laat hem in het licht beginnen:
   - (35,28) (35,29): 2 → 3
   - (37,28): losse 2 in 7 op de lichte vleugelrand → 3
4. **Vleugel rechts: banding (6 op x43 en 5 op x44 als twee evenwijdige kolommen langs de buitenlijn, y31–37) en een sprong 7 → 5 zonder 6 op y38–39.**
   - (44,31) (44,32): 5 → 6 (smaller bovenaan)
   - (42,36) (42,37): 7 → 6 (breder onderaan)
   - (43,38) (43,39): 7 → 6
5. **Kop rechts: wit loopt door tot de selout (8 → 4 → 1, sprong 124); de bol mist een zachte schaduwkant.**
   - (38,4) (38,5) (39,6): 8 → 7
6. **Kinschaduw: losse 3 tussen de 5'en.** (25,23): 3 → 5.
7. **Staartpunt: links donkerder (3) dan rechts (7), tegen het licht in.** (39,56) (39,58): 3 → 5 (de rechterschaduw op x43 blijft).

Totaal 36 pixels, alleen indexwissels binnen het bestaande palet; vorm, oog (x29–37 y4–16) en muil blijven ongewijzigd.

## Ter info voor Jordi
- De klauwen en het gebied eronder (x27–34 y47–52) zijn een grote zwarte vlek (1). Als schaduw onder het lijf klopt het, maar op 1× leest het als gat; lichter maken verandert het model, dus jouw keuze.
- De snorharen rechts van de kop ((40–45,8), (40–44,10), (42–43,11)) zijn rechte grijze lijntjes (4) zonder omlijning; volgens het model, maar ze mogen taps uitlopen (laatste pixel 5).
- In de muil is de violette tint (11) lichter dan de blauwe (10); dat volgt de twee kleuren van het model en is geen fout.

Oordeel: REPARATIES
