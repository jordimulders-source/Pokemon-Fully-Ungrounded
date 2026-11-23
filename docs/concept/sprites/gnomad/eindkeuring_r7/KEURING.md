# Eindkeuring Gnomad sprite r7 (`../sprite_r7/gnomad_A.png`), 22 nov

Verse keurder, alleen uitvoering (model `../r1/gemini_r1.png` + bevroren besluiten in `../SPEC.md`). Sprite niet gewijzigd; simulatie in `voorstel.png`.

## Oordeel: PASS na reparaties 1–5 (6–7 aanbevolen)
Zonder reparaties FAIL op één punt: zwart 21,4 % (327/1525 px), eigenaar wil < ±19 %.
Na 1–7: **18,2 %** (278 px). Na alleen 1–5: 18,6 %.
Ter vergelijking (bovenste 64×64 van anim_front, donkerste kleur): Machoke 17,3 · Vigoroth 15,2 · Sudowoodo 14,3 · Jigglypuff 12,5 · Loudred 24,3 %.

## Wat goed is (niet aanraken)
- Buitenlijn gesloten, zwart aan de schaduwkant; lichte kant van armen/snor/broek met eigen selout (p, g, b).
- Licht linksboven: muts L/l linksboven → M/m rechtsonder, neus met highlight linksboven, broek c → b.
- 16 kleuren, per materiaal 3–4 tinten; geen dithering, geen losse pixels, geen gaten in lijnen.
- Riem leest op 1× als Machoke-riem: zwarte lijn boven/onder, bruine band, crème gesp met eigen rand, afgeronde hoeken en staand gat. Trapjes rechts (4-5-4-3) zijn regelmatig.
- Leesbaarheid op 1× naast Machoke/Jigglypuff/Loudred/Vigoroth/Sudowoodo (`vergelijk_1x.png`, `vergelijk_2x.png`): silhouet, muts, neus, snor en riem duidelijk; past naast Gnomini.

## Reparaties (x,y → kleur uit het palet)
m = (112,95,138) donkerste mutstint · p = (172,72,102) donkerste roze. Alle pixels zijn nu zwart (24,20,32).

1. **[hoog] Mutsrand boven de neus → m** (12 px): (13,27) (14,27) (15,27) (16,26) (17,25) (18,25) (19,25) (20,25) (21,26) (22,26) (22,27) (23,27). Schaduw onder de muts; neus blijft afgetekend (roze tegen donker paars).
2. **[hoog] Mutsrand rechts van de neus → m** (13 px): (24,28) (25,28) (26,28) en (26..35,29). Haalt ook de "lijkt net een oog"-zwartlijn naast de neus weg (Jordi r1).
3. **[hoog] Mutsrand boven rechter snorpluk → m** (5 px): (36,28) (37,28) (38,27) (39,27) (40,28). Zo is de hele mutsrand één lijn in m; buitenrand (11,26) en (41,27–28) blijft zwart.
4. **[middel] Mutsvouw → m** (4 px): (39,22) (39,23) (40,23) (39,24). De rand van het gat (40–42,24) blijft zwart.
5. **[hoog] Onderlijn rechter snorhelft → p** (9 px): (22..30,39). Wordt slagschaduw van de snor op het lijf (licht van boven); snorpunten (21–22,38) en (30–31,38) blijven zwart.
6. **[middel] Dubbele lijn onder linker snorhelft → p** (2 px): (14,39) (15,39). (13,39) blijft zwart als aansluiting op de arm-/lijflijn.
7. **[middel] Grens gezicht/rechter snorhelft → p** (4 px): (33,30) (33,31) (34,32) (34,33). De snor heeft daar al een eigen selout (s).

Bewust níet voorgesteld: riemlijnen, gesprand en gesp-gat. SPEC bevriest "zwarte lijnen boven/onder zoals Machoke" en de gesp "met eigen omlijning"; die zijn ook niet nodig om onder 19 % te komen. Neusonderkant (17..22,33) ook zwart laten: in p loopt hij weg in de P-schaduw van de neus.

## Kleine opmerking (geen reparatie nodig)
- Kruislijn (22..32,52) is 11 px kaarsrecht; mag, maar oogt stijf. Alleen als de eigenaar het noemt.

## Bestanden
- `keur.py`: meting, simulatie (assert: alleen zwarte pixels veranderen), vergelijkingen.
- `voorstel.png` (64×64, zelfde palet), `voorstel_8x.png`, `r7_voorstel_markering_6x.png` (r7 | voorstel | gewijzigde pixels groen omrand), `vergelijk_1x.png`, `vergelijk_2x.png` (r7, voorstel, Gnomini, Machoke, Jigglypuff, Loudred, Vigoroth, Sudowoodo).
