# Gnometrotter: gedeelde reductie en palet (voor Rock, Ice, Grass, Ice-hybride, Grass-hybride)

Vastgelegd door de Rock-maker (23 nov). Alle vijf modellen hebben dezelfde omtrek in het 1024×559-beeld (figuur x 274–749, y 41–522); met deze parameters worden ze even groot en staan ze op dezelfde voetlijn (Jordi: "zoals bij wormadam", "hooguit paar pixels afwijking").

## Reductie (script: `reductie_gedeeld.py <model.png> <uit.png> [palet.png]`)
- **Geen natief raster.** `pitch.py` vond alleen een zwakke kam (x 12,4 / y 13,4, score 1,3; Gnomad had een duidelijk raster). Het model heeft trapjes van ±3,5 px en lijnen van ±4 px: te fijn en ongelijk om terug te halen. Daarom rechtstreeks van het 1024×559-beeld.
- **Pitch P = 8,1 modelpx per spritepx** (schaal 1/8,1; figuur 482 hoog → 59,5 px; Gnomad 50 px, Gnomini ±41 px).
- **Verschuiving/fase:** modelrand y = 523 → spriterand 60 (voeten op rij 59, zoals Gnomad); model x = 512 → spriterand x 32.
  Spritepixel (X,Y) beslaat model x [512+(X−32)·8,1 ; 512+(X−31)·8,1), y [523−(60−Y)·8,1 ; 523−(59−Y)·8,1).
- **Uitsnede/doelpositie:** 64×64; figuur komt op x 3–60, y 0–59 (Rock: 1973 px in de kale reductie).
- **Silhouet:** in de figuur als ≥ 50 % van het vlak geen achtergrond is (achtergrond = min(R,G,B) ≥ 235). Rock: de stok kreeg drempel 0,35 (anders breekt hij; 8 px erbij). Doe dat bij de zusters ook voor de stok, zodat de omtrek gelijk blijft.
- **Kleur kaal:** vlakgemiddelde van de niet-achtergrondpixels → dichtstbijzijnde paletkleur (`_kaal.png`). Geef `gnometrotter_rock.png` als derde argument om op het gedeelde palet te kwantiseren (dan zijn alleen de materiaalindexen fout, die vervang je per vorm).
- `kijk.py` (`model_op_schaal`) zet het model met dezelfde geometrie op 64×64 voor vergelijken; `zoom.py sprite x0 y0 x1 y1` geeft sprite | model op 12× met raster.

## Palet (16, indexen vast)
| idx | Rock | gedeeld? |
|---|---|---|
| 0 | transparant (152,208,160) | ja (= Gnomad) |
| 1 | zwart (24,20,32) | ja (= Gnomad) |
| 2 | donker gesteente, outline base (70,66,68) | **materiaal** (Gnomad: muts donker) |
| 3–5 | donker gesteente vlak (98,93,90) (128,123,117) (158,153,145) | **materiaal** (Gnomad: muts) |
| 6 | roze donker / outline base (172,72,102) | ja (= Gnomad 6) |
| 7–8 | roze schaduw/midden (213,102,136) (244,153,181) | ja (= Gnomad 7–8) |
| 9 | blauw donker / outline base (56,109,142) | ja (= Gnomad 9) |
| 10–11 | blauw schaduw/midden (82,148,197) (122,188,232) | ja (= Gnomad 10–11) |
| 12–14 | licht gesteente baard/haar (166,163,158) (194,192,187) (224,223,219) | **materiaal** (Gnomad: crème/riem) |
| 15 | roze hooglicht (251,184,202) | ja (= Gnomini roze hooglicht) |

Ice/Grass: vervang alleen 2–5 (muts, rugkam, riem, stok, zolen) en 12–14 (baard, haar) door het eigen materiaal; 0, 1, 6–11 en 15 blijven exact gelijk. Roze vlakken gebruiken 7, 8, 15 met 6 als lijn; blauw 9–11 met 9 als lijn; gesteente 3–5 (licht: 12–14) met 2 als lijn.

## Onderdelen (Rock: `zones.py` → `model_zone.npz`, 1024×559)
1 muts+rugkam, 2 haar L, 3 haar R, 4 baard, 5 neus, 6 lijf, 7 arm L+hand (stokarm, vuist), 8 arm R, 9 hand R, 10 riem (+gesp), 11 stok, 12 broek/benen, 13 zool L, 14 zool R. Volgorde voor→achter: neus, haar L, haar R, baard, arm L, stok, hand R, arm R, muts, riem, lijf, broek, zolen.
Omdat de omtrek gelijk is, kunnen de zusters de Rock-zones als start nemen (`zones.py` werkt op familie-kleur, dus voor Ice/Grass de familiedrempels in `fam.py` aanpassen).

## Werkvolgorde Rock (herbruikbaar)
`fam.py` → `zones.py` → `reductie.py` (kaal.png + zone/lijnkans) → `maak.py` (technisch opschonen → red.png) → `dc.py` (Dragonfly Cave-omlijning + gesp → `gnometrotter_rock.png`) → `tel.py` (afwijking per zone) → `controle.py` → `vel.py`.
Oogstrook (Jordi "1 akkoord"): model x 440–515, y 160–200, zwart ≥ 40 % → mutskleur 3 (neusrand uitgezonderd).
