# Blobfish fase 1, sprite r5 (maker)

- **A** (`blobfish_r5A.png`) = r4 + (17,32) zwart → lijnrood (KEURING r4, polijstpunt 2). Diff r4: 1 px.
- **B** (`blobfish_r5B.png`) = A + lichtronde (KEURING r4 punt 1). Alleen tinten, alpha-diff 0; elke tint met één factor geschaald, zodat de R:G:B-verhouding (hue/verzadiging van het model) blijft:
  - tint 4 (153,42,49) helderheid 76 → **(141,39,45) 70**
  - tint 6+7 samengevoegd (gewogen gemiddelde) 82/87 → **(198,53,56) 97**; index 7 → 6 (94 px)
  - tint 9 = lip (202,75,73) 113 → **(219,81,79) 122**; lippen schuiven mee, lip/lijf-verschil 25
  - losse tint-6-pixels in het tint-4-vlak → 4 (10 px, lijst KEURING); ribbel (26,36) (25,37) (24,38) blijft
  - geen extra schaduwtint; 10, 11, 12, 13, 8, lijnen ongewijzigd. B: 10 kleuren + transparant.
- Indexkaart B t.o.v. A: alleen 7→6 (94 px) en de 10 losse pixels 6→4 (assert in `maak_r5.py`).
- Let op: de mauve schaduwtint 8 (169,68,74), helderheid 99, ligt nu even licht als de nieuwe lijftint 6 (97); hij verschilt alleen nog in hue (15 px, bovenkant/vinnen). Niet aangepast (niet gevraagd).
- `vel.png`: A | B | model op 4×; 1× licht/donker: A, B, model, Magikarp, Feebas.
