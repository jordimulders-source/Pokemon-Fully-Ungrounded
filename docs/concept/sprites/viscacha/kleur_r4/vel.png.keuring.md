# Keuring viscacha kleur ronde 4 (onafhankelijke keurder, 7 nov)
- Bron: docs/concept/sprites/viscacha/referenties/gemini_gekozen_ronde6.png (verkleind: kleur_r4/gemini64.png), referenties/jordi_foto1_oog_zijaanzicht.png en jordi_foto2_oog_rechtop.png; vergeleken met graphics/pokemon/{drowzee,pachirisu,dedenne}/anim_front.png (bovenste 64×64), kleur_r3/viscacha.png, kleur_r3/vel.png.keuring.md, kleur_r4/NOTITIES.md, controle_uitvoer.txt.
- Bekeken: kleur_r4/viscacha.png op 8× (nearest), 1× op licht (240) en donker (40), kop 16× naast gemini64 en de foto's, raster rij voor rij (oog, staartaanzet, poten), pixeldiff r3→r4 zelf berekend.

## Blind (vóór SPEC/notities)
- 1×: zandkleurig springknaagdier naar links, voorpoten op, staart met gele pluim; leest als officiële sprite in de Pachirisu/Dedenne-hoek. Electric door het geel.
- Oog: smal amandeloog met zware lidlijn, halfgesloten; leest loom/zelfvoldaan, niet boos (lid ligt horizontaal, zakt niet naar de snuit), niet dicht (glanspixel), geen monster.
- Gele stip op de neuspunt: op 1× een klein geel puntje vóór de snuit; eerder "gele neus/pluk" dan vonk, maar het is de minst duidelijke plek van de sprite.
- Oren ronder dan ik bij een viscacha verwachtte uit r3; nabij oor met bruine schelp.

## Per onderdeel (lijkt op / wijkt af in)
- **Pose/massa**: lijkt op Gemini (ongewijzigd t.o.v. r3) / wijkt af in: niets.
- **Oog**: lijkt op de foto's (donker, hoog opzij, zwaar bovenlid, smalle spleet; slaperig-zelfvoldaan) en is technisch een echt Pokémon-oog (Drowzee-bouw: lidlijn 1 op (11–14,25), spleet 2 rijen (9–15,26–27), onderlid 3 op (11–14,28), pupil 1 op (11,27), glans D op (12,26)) / wijkt af in Gemini: luier, de enige door Jordi toegestane afwijking. Glans houden: zonder leest de spleet als dicht.
- **Snuitpluk**: lijkt op Gemini (gele pluk op de snuitpunt, (2–4,26–28)) / wijkt af in: kleiner. Geen schicht- of zigzagvorm, vast aan de snuit, selout 8 aan de rand; leest op 1× als gele vacht/neuspunt, niet als vonk. Grensgeval, zie voor Jordi.
- **Oren**: lijken op Gemini (rondere top: 3 px bij (19–21,12) en (6–8,12), nabij oor 1 px breder (23,15–17), grotere binnenschelp B/C) / wijken af in: het nabije oor blijft iets smaller dan de grote schelp van Gemini. Top van het verre oor 3 px plat met afgeronde hoeken via (5,13): leest rond genoeg.
- **Wangpluk**: ongewijzigd t.o.v. r3 (PASS).
- **Lijf/schouder**: zachte 4-overgang (21,34–36), (22,36), (24,37–39) geeft de romp op 8× wat vorm zonder nieuwe lijn of banding. OK.
- **Staartaanzet**: r3-recht stuk gebroken tot trap (47–49,48), (50–53,47), (54–57,46) / wijkt af in Gemini: loopt nog als schuine rechte (3–4–4) en gaat daarna abrupt naar 1 px per rij op (58,45); een boog zou aflopende stukken hebben. Klein, geen FAIL.
- **Verre voet**: hiel en teen rond ((22,58), (29,58) weg, (29,57) → 1). OK.
- **Scheen nabije achterpoot**: 3-strook taps (47,56–58 → 4). OK als reparatie; buitenrand x49 rij 53–58 blijft een rechte verticaal, voor een scheen aanvaardbaar.
- **Belijning/netheid**: 1 px, 2 lichtkant / 1 schaduwkant, geen om-en-om; 0 open randen, 0 losse pixels, kleine clusters alleen oog + pluimkern (57,12); 16 kleuren, palet gelijk aan r3.

## Pixeldiff r3→r4 (zelf gemeten)
76 px, allemaal in de benoemde zones: oren (rij 12–17), oog (9–15, 25–29), snuitpluk (2–4, 26–28), schouder (21–24, 34–39), staartaanzet (50–56, 46–48), verre voet (22/29, 57–58), scheen (47, 56–58). Niets erbuiten.

## Reparaties (optioneel, klein; geen FAIL-reden)
1. Staartaanzet: aflopende stukken in plaats van 3–4–4, bv. (54,46) → 1 en (55–57,46) ruimer laten aansluiten op rij 45, zodat het verloop 4–3–2–1 wordt.

## Voor Jordi
- Snuitpluk: Gemini heeft hem; op 1× een geel puntje op de neus. Erbij laten of weg (6 px terug naar r3)?
- Oor: rondere top nu, maar nog iets smaller dan de grote schelp van Gemini (silhouetzaak).
- Oog bewust luier dan Gemini (Drowzee-lid), zoals op zijn foto's.

Oordeel: PASS
