# Viscacha frontsprite, kleur ronde 6 (maker-agent): nieuwe basis op kleinere schaal
Coördinator: Gemini volgen, het geheel kleiner zodat Gemini **inclusief snorharen** in 64×64 past; niets afkappen. Keuring r5: `kleur_r5/vel.png.keuring.md` (9 reparaties).

## Basis
- `onderlaag.py`: Gemini-masker (gevuld, vlekjes < 40 px weg) op schaal **1:10,78** (was 1:9,97, ±7,5 % kleiner). Breedte 63 px incl. snorharen, offset (0,14), voeten op rij 62.
- Lichaam = masker zonder dunne delen (opening 7×7, BOX ≥ 0,5): `silhouet_auto.txt` (`#`); dunne delen (snorharen, pluimpunten) als `+` (dekking ≥ 0,12).
- `gemini64.png`: Gemini verkleind (gemiddelde kleur per spritepixel); `onderlaag.txt`: gekwantiseerd naar het palet, alleen als gids.
- Kleur met de hand: `raster_r6.py` (per rij segmenten, kop/oren/pluim/lijf/poten/snorharen apart; nazorg onderaan) → `raster.txt`, `render.py` → `viscacha.png` + `normal.pal`. De r5-oplossingen zijn op deze schaal opnieuw met de hand gezet; er is niets uit r5 geschaald. Daarom geen pixeldiff r5→r6 (ander raster); de vergelijking staat tegen het Gemini-masker hieronder.

## Keuringspunten r5 → r6 (nieuwe coördinaten)
1. **Framing:** Gemini past met snorharen (zie Basis).
2. **Snuit:** de snuitbult is het voorste punt (x6, rij 32–35). Neus 2 px donker óp de voorrand (6–7,34), los van de mond. Y-mondje: steel (7,35), dan (8–10,36) naar achteren. Ronde kin met terracotta onderlip (9–11,37), kinlijn (11–12,38); de bef begint op rij 38–39.
3. **Snorharen nabij:** 3 lijnen in B, vast aan de snuit bij (5,35), (6,36) en (8,38), uitwaaierend tot de framerand (6–7 px lang).
4. **Snorharen ver:** 2 lijnen van 1 px in B, vlak (helling ±1/3) van de wang (12–13,36–37) tot onder de sikkelpunt (21–23,39–40). Geen streepjes in E en geen raster in het crème; ze lopen vast door van wang naar schouder, niets zweeft.
5. **Gele pluk:** lager, op rij 29–31 (punten (6,29) en (5,31)), op de voorhoofdrand vóór het oog.
6. **Pluim:** 4 slanke vlammen met de punten (59,14), (54,16), (59,20) en (50,23). Hoofdkleur A (bleek citroen), 9 als schaduw, 8 als selout/binnenlijn, 1 aan de schaduwkant; een bruine wig (C) van de staart in de pluimbasis (53–54, rij 24–27).
7. **Voorpoten:** ver opgeheven wantje (12–19,44–50) met teenlijntje (14,48). Nabij: been met voorlijn 2 en schouderlijn, ronde poot (20–25,47–52) met teenlijntje (23,49).
8. **Lijf:** dijlijn 4 als boog (37,37) → (36,38–44) → (37,44–46) → (38,47); schouderlijn 2 (28,39–41) → (25,46). De buikvlek is driehoekig (top (32–33,43), basis rij 46–49), rechts begrensd door de dijlijn. Bil: 4 langs de rand, 3 onder en achter; de vachtpunt (48–49,44) komt uit het masker.
9. **Achterpoten:** teenlijntjes (27,58) en (47,61). Staartonderrand in een trap van 4–5–3: (47–50,49), (51–55,48), (56–58,47); geen recht stuk van 8 px meer. Scheen met 1 px verspringing op rij 57.
- **Oog:** Drowzee-oog uit r4/r5 (lid, spleet en glans), verplaatst naar (13–19,29–33).
- **Wangaanhangsel en vachtpiek:** zoals in r5, op de nieuwe schaal. Sikkel: punt (24–27,29), bolle kant tot x18 (rij 33–35), inkeping x21–22, onderpunt (22–24,38); terracotta schaduwkant op de nek. Vachtpiek (33–40,29–30) uit het masker.

## Silhouet t.o.v. het Gemini-masker
- Ontbreekt: (56–57,48) en (51–55,49), de afronding van de staartonderrand (keuring punt 9).
- Extra buiten het masker:
  - de dunne delen (`+`: snorharen, pluimpunten), 17 px;
  - de snorhaarlijnen zelf: (0,36), (8,38), (0,39), (7,39) en (2,42), die het masker als grijze rafel had;
  - de pluklijn (6,30);
  - de snuitbult (6,33–34);
  - de onderrand van de bef (12–13,39).
- Nieuw silhouet: `silhouet/silhouet_r6.txt`.

## Controle (`controle_uitvoer.txt`)
- Open randen 0.
- Losse pixels: alleen de pluimpunt (59,14) en twee diagonale snorhaarpixels (1-px-lijn).
- Clusters < 3 px: alleen oogpixels.
- 16 kleuren incl. transparant; png = raster.
- Vel: `vel.png` (keurvel: werk naast gemini64, foto1-kop, Dedenne en Drowzee, close-up van de kop) + afvinkvel `onderdelen.png` (per onderdeel sprite | Gemini, 12×).

## Afvinklijst (zie onderdelenvel)
- [x] kop
- [x] oor ver
- [x] oor nabij (grote donkere schelp)
- [~] oog: bewust Drowzee-lui
- [x] neus
- [x] mond (Y)
- [x] snorharen (3 + 2, vast)
- [x] gele pluk
- [x] wangaanhangsel
- [~] borst: de bef is iets smaller dan bij Gemini, de verre snorharen lopen erover
- [~] voorpoten: vorm komt overeen, poten iets kleiner dan bij Gemini
- [x] lijf
- [~] buik: driehoek, maar breder aan de basis
- [x] achterpoten
- [x] staart
- [~] pluim: 4 vlammen; Gemini is bleker en de vlammen staan dichter op elkaar

## Zwakke punten
1. De pluim is goudener dan Gemini's bleek citroen (9 domineert in de schaduwhelft).
2. De dijlijn in 4 op 5 is op 1× nauwelijks te zien.
3. De nabije voorpoot leest op 8× wat stijf (voorlijn x22 over 6 rijen).
4. Het raster is helemaal nieuw; alleen de controle en mijn eigen blik zijn gedaan, nog geen keurder.
Niets gecommit.
