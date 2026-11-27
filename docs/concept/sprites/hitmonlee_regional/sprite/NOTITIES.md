# Regionale Hitmonlee (glas, omhaal) – sprite-notities maker

**Kandidaat:** `kandidaat.png` (64×64, geïndexeerd, 16 paletplaatsen = 15 kleuren + index 0 achtergrond), `kandidaat_8x.png`.
Figuur 59 × 64 px (onderaan, horizontaal gecentreerd). Laatste ronde = `r13/` (vel: `r13/vel.png` = r13 | r12 | model).

## Onderlaag (model overnemen)
- **Raster:** het model heeft een raster van **5,12 px** (200×200 cellen), niet 10,24: op 8× zoom zijn ringlijnen en
  lijntrapjes 1 cel van 5,12 (zelfde valkuil als pitahaya). `natief.py` → `natief.png` (136×148, mediaan van de binnenste 3×3 per cel).
  `test/natief.png` (10,24) en rondes r1–r2 gebruikten nog het grove raster; vanaf r3 alles op 5,12.
- **Verkleinen** (`onderlaag.py`): 2×2-reductie met lijnregel (één natieve lijnpixel (gem. < 80) in het blok → donkerste pixel,
  anders mediaan van de niet-lijnpixels; blok met ≥3 achtergrondpixels = achtergrond) → 68×74 → **schrappen** zoals Gengas:
  10 rijen (2x-rijen 4, 8, 13, 17, 22, 28, 45, 55, 64, 70) en 9 kolommen (1, 5, 16, 37, 42, 50, 56, 60, 65) die het meest op hun buur
  lijken, ≥4 uit elkaar, oogzone beschermd → 59×64 (verhouding blijft). Elke pixel = een modelpixel; silhouet daarna niet meer veranderd.
- **Palet** (r4, gemeten met k-means in Lab op het model + Gen 3-stappen): 1 lijn zwartbruin, 2 donkerrood (selout/ringlijn),
  3–4 rood glas, 11–12 zalm/bleekroze glans, 5–9 gloed (oranjerood → oranje → lichtoranje → geel → geelwit hart), 10 wit (glans),
  13–15 doorschijnend (bruinmauve/tan/crème). Per pixel dichtstbijzijnde kleur in Lab = kale reductie (`r4/`).
- Meetgereedschap: `meet.py` (per spritepixel uit het 2×2-blok: gemiddeld, donkerste, lichtste, op één na lichtste, zonder lijn,
  aantal lijnpixels), `raster.py` (natief model met spritepixelraster + sprite ernaast), `check.py` (kleuren, losse clusters, lijnstatistiek), `vel.py`.

## Rondes
| ronde | wat |
|---|---|
| r1–r2 | proef op het 10,24-raster (verworpen: raster te grof) |
| r3 | onderlaag 5,12 + 2×2-lijnregel (v1 gekozen boven v2: ringlijnen blijven) |
| r4 | Lab-palet, kale reductie (basis voor alle afwijkingstellingen) |
| r5 | toonkaart in de romp (eerste versie, later vervangen door r11) |
| r6 | A trapbeenringen, B oog + verre oog, C standbeenringen |
| r7 | D binnenlijnen alleen waar het model ≥2 natieve lijnpixels heeft (Krassault/Abra-regel), 34 px |
| r8 | E kussentjes, teentjes, duimglans |
| r9 | F ontkorrelen (vultint-clusters < 3 px → buurtint uit dezelfde groep), 105 px |
| r10 | G buitenlijn: zwart waar rechts/onder achtergrond is, donkerrood selout boven/links, geen om-en-om (62 % zwart) |
| r11 | H toonkaart rood glas/gloed opnieuw: gladgestreken modelkleur (σ 1 natieve px; 1,5 en 2 vergeleken), tint = dichtstbijzijnde Lab-kleur in de materiaalreeks, harde tintgrenzen |
| r12 | F opnieuw na r11, 75 px |
| r13 | I glasrand: 12 binnenrandpixels → bleekroze, alleen waar de twee lichtste natieve pixels wit zijn |
Elke wijziging staat per pixel in `rN/log.txt`.

## Pixels die niet 1-op-1 uit de kale reductie komen (r13 t.o.v. r4: 449 van 1391 = 32 %)
- **Buitenlijn (60):** alleen de tint (zwart ↔ donkerrood), niet de plek.
- **Trapbeenringen rij 11–22 (42):** de reductie gaf willekeurige lijn/band-spikkels. Rijtype uit het model (natieve donkerrijen):
  lijnrijen 11, 13, 15, 17, 20, 22 binnenin = 2; bandrijen = op één na lichtste natieve pixel (de verlichte ringkleur) binnen de ringtinten.
  Rij 11 is de lijn onder de voet die in geschrapte 2x-rij 10.5 zat (1 rij verschoven). Ringlijnen zijn recht; het model heeft licht gebogen ringen.
- **Standbeenringen rij 44–53 (25):** idem, lijnrijen 44, 46, 48, 51, 53.
- **Ogen (73, incl. de r5-toonkaart in die zone):** per pixel uit de natieve 2×2-blokken (lijst in `r6/bouw.py`): bovenlijn r29, dikke
  zwarte linkerhoek, rode iris, glans (20,30) met bleke reflectie (20,31), oranje onderkant, onderlijn; verre oog 3×4 met glans (28,27).
- **Overig (249):** toonkaart (tintwissels binnen hetzelfde materiaal, geen vormwijziging), ontkorrelen, binnenlijnen weg zonder modellijn,
  kussentje trapvoet (31–33 × 3–5), kussentje standvoet (50–51 × 54–56), teentjes (52–58 × 60–62), duimglans (5,53), glasrand (12 px).
- Geen enkele vorm is getekend; silhouet = model (2×2-masker + schrappen).

## Twijfelpunten (eigen)
1. 32 % afwijking van de kale reductie: vooral tintwissels door de toonkaart (r11) en ontkorrelen; vorm onveranderd. Toch boven de ±25 %-vuistregel, dus bewust laten keuren.
2. Gloed gebruikt 5 tinten (5–9), rood glas 4 (3, 4, 11, 12): meer dan "≤3 per kleurgroep"; gekozen omdat de gloed een verloop is.
3. Ringen recht i.p.v. licht gebogen; ladderachtig (lijn/band om en om). Trapbeen 6 ringen, standbeen 5 (model ongeveer evenveel).
4. Onderste deel trapbeen (doorschijnend, rij 23–31) nog wat vlekkerig tan/bruin; het model is daar ook rommelig maar zachter.
5. Linkerhand: duimtop en vingertoppen (glasbolletjes) lezen niet als aparte bolletjes; vrij druk.
6. Kussentjes in crème/tan/wit: het palet heeft geen neutraal grijs (het model is grijswit).
7. Schrappen nam 5 van de 10 rijen in voet + trapbeen (daar veel witte rijen): het trapbeen is ±1–2 px korter dan bij gelijkmatig verkleinen.
8. Oog is 7×5 px, zoals in het model (klein t.o.v. de romp).
