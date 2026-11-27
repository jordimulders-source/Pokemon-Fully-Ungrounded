# Regionale Staryu (koekje) ronde 2: keurderreparaties uit `keuring_r1/KEURING.md`

Bestanden: `staryu_r2.png`, `kaal.png` (kale reductie met de gerepareerde klassen), `vel.png` (r2 8× | r1 8× | model 8× / close-ups (sprite | model) / 1× op wit, crème, donker, zwart + model 1× + Gen 3 Staryu/Starmie), `bouw.py` (= r1-pijplijn met `klassen(r2=True)` + stap 5 keurderreparaties met asserts op de oude waarde).

## Diff r1 → r2: 13 px (silhouet-diff 0)
**Keurderreparaties (9 px):**
1. (11,29) K → 2 (selout). Linkerrand nu s,s,s,s op (11,27–29),(12,30); zwart begint op (12,31).
2. (24,32), (24,33) chiprand 6 → 3 (deeg tussen chip en juweel, model gem. 142/119).
3. (20,36) → 2 (model gem. 94 → selout, zoals de keurder mat); (29,46) chipbruin → 3 (via de klassenreparatie, model gem. 118).
4. (30,13), (31,13), (31,14) 4 → 3; (29,15), (29,16) 4 → 5.
5. (26,35) stond in r1 al op 9 (donkerst, gecontroleerd met assert). Geen wijziging. De keurder las hier waarschijnlijk een andere pixel; de ring onderaan is r. 36 x27–31, volledig 9.

**Klassenreparatie (`gereedschap/klassen.py`, `naden_uit`, punt 3):** donkere naden en randjes vielen door lage verzadiging in de chocoladeklasse. Gemeten op het natieve model: de 11 echte chips zijn componenten (chocolade + binnen-zwart) van 29–55 natieve px, al het andere is ≤ 5 px. Componenten < 15 px buiten het juweelvak zijn nu deeg. In de kale reductie veranderde dat 9 px: (32,12), (50,26), (11,27), (11,28), (11,29), (20,36), (21,36), (19,37), (29,46). De eerste vijf zijn randpixels die de buitenlijnstap toch al overschreef. In de eindsprite raakt dit 4 px buiten de keurderpunten (barststap en ontkorrelen gebruiken de nieuwe klassen):
- (20,35) 3 → 4 (model gem. 147, middentoon klopt);
- (19,37) 5 → 3 (model gem. 130: de naad loopt hier door);
- (19,38) 5 → 3 (barstpixel uit het model, min L 36 in de cel);
- (20,36) eerst 7 → 3 door de klassen, daarna → 2 volgens punt 3.

Verder geen wijzigingen: pixeldiff 0 buiten de 13 genoemde pixels (bewezen met een diff op r1).

## Controle
64×64, mode P, transparency 0, 14 kleuren, 981 px, zwart 8,0 %, geen lichte buitenrand en geen losse zwarte pixels.

## Twijfels
- (29,15)–(29,16) vormen samen een los lichtplukje van 2 px (< 3 px). Dit is de gemeten keurderreparatie (model 186/197); ik heb het zo gelaten.
- (20,36) is één selout-pixel in de naad (keurdermeting 94). Op 1× is het niet te zien.
