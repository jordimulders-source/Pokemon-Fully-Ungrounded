# Onweerswolk-Altaria frontsprite, ronde 7 (vanaf r6)

Opdracht (coördinator): scheidingslijnen tussen de bollen 1-op-1 uit het model in de wolk-selout (tint 2, L55, gekleurd, niet zwart),
1 px, gebogen; binnen elke bol kap licht, midden, schaduw tegen de boog; overgang Y44 naadloos (Y40–44 mocht); naad (7–11,25) mocht mee.
Bouwen vanuit `altaria/`: `python3 sprite_r7/bouw.py && python3 sprite_r7/vel.py`. Bestanden: `altaria_r7.png`, `altaria_r7_8x.png`, `vel.png` (r7 | r6 | model | game op 8×; lijf en rechtervleugel 16× naast het model; 1× op licht/donker), `bouw.py`.

## Diff
- r7 ↔ r6: **289 px** (lijf Y40–57: 196, waarvan Y40–43: 21; rechtervleugel: 84; linkervleugel-naad X5–13 Y22–29: 9). Alpha 0, zwart buiten de pupillen 0.
- Kop, ogen, snavel, hals, kuif, static, silhouet en alles buiten de drie zones: diff 0 (assert).

## Werkwijze
1. Lijn = blok waarin het natieve model een (bijna) zwarte pixel heeft (min L < 32) → selout 2. Losse stukjes < 3 px die nergens aan vastzitten vallen weg.
2. Op 1/3 laat het model de dunne lijnen maar in stukjes zien; daarom ook de onderboog van elke r6-bol (grens onder/rechts met een andere bol, uit `sprite_r6/bollen.txt`, op het model opgemeten) als selout, zodat de lijnen doorlopen. Daarna gedund tot 1 px.
3. Oude r5-selout in de zones die het model niet als lijn heeft → vultint van de buren (ook de naad (7–11,25)).
4. Binnen de bol: lijf midden (4) in plaats van donker; schaduw 3 direct boven/links van de lijn; kap 5/6 uit r6 blijft. Rok (Y ≥ 54) blijft donker zoals het model.

## Eerlijke twijfels
- De bollen zijn nu omlijnd en lezen als losse vormen, maar op 8× eerder als kasseien/stenen dan als zachte wolkbollen: de lijnen zijn hoekig (1/3-reductie) en er zijn rechte stukken (Y52 X14–18, Y55 X22–29 = de model-boog, Y52 X37–43, Y47 X46–50).
- Rechtervleugel: de lijnen maken kleine hoekige vakjes; leest drukker dan het model.
- Veel vlakjes < 3 px (vooral schaduwpixels 3 langs de lijnen en ringpixels); niet opgeschoond.
- De bevroren rijen boven Y40 houden de r5-stijl.
