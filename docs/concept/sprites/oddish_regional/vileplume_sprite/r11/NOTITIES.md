# Vileplume r11: Jordi's punten op r10 (20 nov)

Jordi: "wat er bij de voorste 2 foutgaat is niet zo zeer de vorm van de anemonen, maar meer de ronde vorm erom heen die er niet goed bij past, daarnaast zijn de cirkels erin ook nog niet goed. De linkerpoot mag nog iets meer een knievorm hebben, ogen moeten we een andere kleur geven zodat het niet samenvoegt met de anemonen". Keuzes: omtrek voorste 2 = zoals het model; mondjes voorste 2 = zoals het model; ogen = "een kleur die goed contrast geeft".

Basis: `r10/r10_voor_r3.png`. Opnieuw bouwen (vanuit `vileplume_sprite/`): `python3 r11/bouw.py [A|B|C]` (standaard B) en `python3 r11/vel.py`.
Bestanden: `vileplume_r11.png` (64×64, 4 bpp, 16 paletplekken, index 0 transparant, transparency=0; palet = r10, geen kleur vervangen), `vileplume_r11_ogenA/B/C.png`, `vel.png` (r11 | r10 | model 8× / 12× VL, VR, linkerpoot, gezicht: r11 | r10 | model / 1×), `vel_ogen.png` (opties 1×, 8×, gezicht 12×), `uitvoer.txt` (tellingen + tekstraster), `toets.txt`.

## Wat er veranderd is (114 px t.o.v. r10; buiten deze zones 0, geassert in bouw.py)
| zone | px | wat |
|---|---|---|
| ring (rand van L/T/R tegen VL/VR) | 37 | De gesloten zwarte ring weg. Onderste helft van VL/VR (de schijf die over L en R valt): donkerrode rand R0, zoals het model. Bovenste helft: R0 alleen direct tegen een vingertop, anders schaduw R1 van de achterste anemoon. R0-stipjes zonder lijnbuur → R1. |
| vingers (bovenrand VL/VR) | 18 | Randpixels in de bovenste helft die geen tentakel zijn (tussenlijn/schijf), plus hun buur richting mondje als dat ook geen tentakel is → R1 (achterste anemoon in schaduw). Zo steken de r3-tentakels als vingers uit met inkepingen van 1–2 px, zoals het model. Tentakels zelf niet verlengd of ingekort. |
| mondjes VL, VR | 34 | Uit het model gemeten (dekking per spritepixel op het natieve raster). VL: zwart x22–25 y21, zwart (22,22) en (26,22), binnen R2 x23–25 y22, onderkant R0 x22–25 y23. VR: zwart x40–44 y19, zwart (40,20) en (44,20), binnen R2 x41–43 y20, onderkant R0 x41–43 y21. In het model is de ring boven/opzij zwart en onder donkerrood, met licht tentakelweefsel eromheen: lijnpixels (R0/zwart/R1) direct naast de ring worden R3 waar het model ≥ 40 % licht is (anders liep de ring in de tentakellijnen op, het "niet goed" van r10). Oude r3-ringpixels buiten de nieuwe ring: modeltint (R3/R2). |
| linkerpoot | 21 | Knie uit het model (natief: heup u84–89, knie naar voren tot u80 bij v130–140, daaronder u82, scheen u84–90). Linkerkant per rij: r43–44 x24, **r45–48 x23 (knie)**, r49–55 x24, r56–58 x25, kap r59 x25–26. r10 liep x23 door tot r50 en had één verspringing (r51), dus geen knie. Opbouw lijn W0 – vulling – zwart; vultinten als r10. Rechterpoot 0 px. |
| ogen | 4 | Zelfde 4 pixels als r10 (links (22,32)+(23,32), rechts (31,31)+(32,31)), alleen kleur. |

Krater, achterste anemonen (buiten hun randpixels tegen VL/VR), lijf, armen, mond, rechterpoot: 0 px.

## Ogen (vel_ogen.png), alle drie bestaande paletkleuren
- **A** leisteen W0 (44,64,68), de lijnkleur van het lijf en de mond. Rood is weg, maar het linkeroog ligt direct onder de zwarte kroonrand en het rechteroog naast het einde ervan: donker op donker, op 1× smelt het weer.
- **B (standaard)** kratergeel (254,164,60), beide pixels. Grootste contrast met alle buren gemeten (RGB-afstand ≥ 129 tot zwart, R1 en het witte lijf; A: 74). Op 1× en 8× duidelijk twee oogjes.
- **C** kratergeel + zwart (pupil rechts): het zwarte deel valt weg tegen de kroonrand, leest als 1 px.
Een nieuwe kleur (bv. blauw) kan alleen door een kraterkleur te vervangen (alle 16 plekken in gebruik, geen dubbele); niet gedaan.

## Toets (`toets.txt`)
- 16 kleuren incl. transparant; bbox x2–60 y1–62 (gelijk aan r10); zwart 15,2 %.
- Losse pixels 31 (r10: 38). Nieuw: alleen (45,19) R2 rechts naast de bovenrand van het VR-mondje (r3-tentakelpixel; model daar licht). Weg: 8, o.a. de 4 losse ooppixels van r10 en losse stipjes aan de oude ring.
- Lijnpixel midden in een vlak: 0. Lichte kleur op de buitenrand: 0.

## Twijfels (eerlijk)
- **Scheiding voor/achter is nu zacht** (donkerrood i.p.v. zwart). Dat volgt het model, maar op 8× smelten VL/VR boven meer met L/T/R samen dan in het model, waar de achterste anemonen naast de voorste duidelijk donkerder zijn. Als Jordi meer scheiding wil: de R1-schaduw op de achterste anemonen 1 px breder maken (eigen voorstel, niet gedaan).
- **Vingers**: de r3-tentakels lopen bijna overal tot de rand van de schijf, dus er vallen maar 18 px inkepingen; de bovenrand is minder rafelig dan in het model. Meer vingers = tentakels inkorten, en dat viel buiten "tentakels alleen aanpassen waar de omtrek ze afsnijdt".
- **Buitenmaat**: gemeten op het model (uitsneden met natief raster) ligt de buitenmaat van VL/VR binnen ±1 px van de r3-ellipsen, en de onderrand is per kolom gelijk aan de kale reductie. Ik heb daarom alleen de rand (ring) en de bovenrand (vingers) veranderd, niet de buitenmaat. Als Jordi met "de ronde vorm" ook de maat bedoelt: vragen.
- 37 randpixels van de achterste anemonen zijn veranderd (de ring lag op hun kant).
- Geel als oogkleur is de kraterkleur: contrast het best, maar het is ook een ontwerpkeuze (gloeiende ogen). A is de klassieke donkere variant.
- Knie: 1 px naar voren op r45–48, dan 2× 1 px terug; op 1× subtiel. Verder naar voren (x22) staat niet in het model.
