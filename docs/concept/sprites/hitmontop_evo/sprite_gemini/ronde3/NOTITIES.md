# Hitmongroove: sprite naar het Gemini-model, ronde 3 (maker)

Basis: `ronde2/capoeira_B.png` (benen B gekozen; A vervalt).

Jordi over r2, letterlijk: "de ogen mogen nog wat meer hitmontop, mond is goed, rest van het hoofd ook wel, de benen met wit zijn beter, al mis ik daar nog wat schaduwing, waardoor het net lijkt alsof er iets weggelaten is. De torso ziet er ook nog een beetje gek uit, maar ik weet niet zo goed hoe we dat beter kunnen maken, voor de rest komen we nu echt ergens".

## Opgeleverd
| Bestand | Wat |
|---|---|
| `capoeira.png` + `raster.txt` | De beste variant volgens mij: torso c. |
| `capoeira_torso_a.png`, `_b.png`, `_c.png` + `raster_torso_*.txt` | De drie torsovarianten. Alleen de torso (rij 27-40) verschilt; de rest is pixel voor pixel gelijk. |
| `vel.png` | Zie hieronder. |

Inhoud van `vel.png`:
- r3 c, a, b, r2 B en het model op 8×;
- de ogen: r3, Hitmontop en het model op 12×;
- de torso: a, b, c en het model op 12×;
- de benen: r3 en het model op 8×;
- r3 op 1× en 2×, licht en donker.

Het tekenwerk staat met de hand in `hand_ogen.txt`, `hand_benen_wit.txt` en `hand_torso_[abc].txt`. De scripts doen alleen montage, png, controle en het vel.

## 1. Ogen (meer Hitmontop)
- Het oog is pixel voor pixel overgenomen van `graphics/pokemon/hitmontop/anim_front.png`: 4×4 rond (`.XX.` / `XwXX` / `XXXX` / `.XX.`).
  - Het wit staat linksboven, zoals bij Hitmontop. Dat past ook bij het licht linksboven.
  - De zwarte massa zit onder en rechts van de glans.
- Het oog staat op de gemeten middens van de modelogen:
  - oog 1: midden (17,65; 39,05), dus kolom 16-19, rij 37-40;
  - oog 2: midden (19,95; 45,95), dus kolom 18-21, rij 44-47.
- Mond en de rest van de kop zijn niet veranderd.
- **Let op:** Hitmontops oog is niet gedraaid, terwijl de kop van Hitmongroove ondersteboven staat. Een 180° gedraaide versie (glans rechtsonder) is mogelijk als Jordi dat wil.

## 2. Benen (wit met volume)
- Het wit heeft nu een schaduwkant in grijs 7, zoals het grijs in het model. Wit staat aan de lichte kant, grijs aan de schaduwkant richting de gele wikkelband.
  - Linkerbeen: rij 15-20.
  - Rechterbeen: rij 17-20.
- Op de bovenste rijen is de band 3 breed (wit, wit, grijs); daar is de glans 8 in het geel vervallen.
- De rest van de benen is niet veranderd.

## 3. Torso: drie varianten (silhouet ongewijzigd, binnen 1 px op het model)
| Variant | Wat |
|---|---|
| **a** | Cilinder langs de schuine lichaamsas (45°): een lichte band langs de hele linkerbovenkant en een sikkelschaduw langs de rechteronderkant. Leest strak en gespierd, maar de onderste helft wordt een groot donker vlak. |
| **b** | Als a, plus ronde aanzetten: een eigen bolletje boven de steunarm en een korte binnenlijn bij de vrije arm. Leest het meest anatomisch, maar de extra 5-lijntjes maken het onrustig. |
| **c** (gekozen, = `capoeira.png`) | Mijn lezing van het model: vooral basistint zoals het model, een kleine ovale glans linksboven-midden en een sikkel langs de rechterkant die naar de steunarm breder wordt. Dichtst bij het model en het minst "veelhoek". |

## 4. Palet
Er komt geen tint vrij: A had geen eigen kleuren, en alle 16 worden in B gebruikt. Het grijs in het wit gebruikt daarom het bestaande grijs 7. Er is geen tweede, lichtere grijstint en geen voetglans.

## Controle (alle vier de pngs)
- 16 kleuren, inclusief transparant.
- 0 losse omlijningspixels in een vlak.
- 0 randpixels zonder donkere rand.
- Silhouetverschil met het model: 43 px, net als in r1 en r2.
- Kleine vlakjes die overblijven zijn bedoeld: de diagonale lijnen, de vlecht, de glimpjes en de diagonale wit-grijsband.
- In variant b staan extra losse 4/5-pixels; die horen bij het schouderbolletje.

## Zwak punt
- Oog 2 raakt de verticale V-lijn (kolom 17). In het model staan ze ook vlak naast elkaar. Doordat de V-lijn donkerbruin is, versmelten ze niet. Tussen het oog en de punt van de V staat één bruine pixel (18,44): die scheidt ze.

Niet gecommit, geen keurder gestart.
