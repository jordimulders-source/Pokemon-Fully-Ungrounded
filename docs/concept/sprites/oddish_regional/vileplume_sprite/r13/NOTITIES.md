# Vileplume r13: Jordi op r12 (21 nov)

Jordi: "nee dit is prima, op wat details na, het gat linksbovenin tussen 2 anemonen in moet op een natuurlijke manier dicht, de zwarte lijnen tussen anemonen moet natuurlijker en de poten zien er niet mooi uit, misschien moeten we die 1 pixel dikker maken?"

Basis: r12 (bevroren). Bouwen (vanuit `vileplume_sprite/`): `python3 r13/bouw.py` en `python3 r13/vel.py`.
- Elke wijziging controleert de oude waarde.
- Buiten de drie zones is het verschil met r12 0 (assert).

Bestanden:
- `vileplume_r13.png`: dikke poten, standaard.
- `vileplume_r13_dunnepoten.png`: r12-poten, met dezelfde gat- en lijnreparaties.
- Beide: P-modus, 16 plekken, transparency=0, palet r12.
- Verder: `vel.png`, `uitvoer.txt`, `toets.txt`.

## Gewijzigd t.o.v. r12 (r13: 83 px, dunnepoten: 23 px)
- **Gat (11 px).** Tussen L en de krater lagen 3 transparante pixels: (23,11), (24,11) en (25,10). Daarnaast zat een gaatje in de linkerrand van L: (5,10) en (6,11).
  - L loopt er nu doorlopend overheen, in de tinten van L: licht links, R1/R0 aan de kraterkant tegen de zwarte kraterrand.
  - L's eigen zwarte randjes rond de gaten zijn L-tint geworden, anders bleven er dubbele lijnen binnenin over: (24,10), (22,11), (21,11), (6,10), (5,11) en (7,11) (tentakelscheiding R0).
- **Lijnen (12 px).**
  - **T|L:** de dubbele lijn wordt één zwarte lijn op x21 (rij 6–8). De T-rand ernaast krijgt T-tint: (22,6)=R3 en (22,8)=R2.
  - **L|krater:** de trap op rij 12–14 was 2 px dik. Die is nu 1 px op x24; de L-kant is R1.
  - **Naad VL|VR:** boven (rij 18–19), tegen de lichte rand van VR, staat nu selout R0 in plaats van zwart.
  - **Strook T|R:** de vlakke R1-strook loopt in de buitenste kolom over naar R2.
- **Poten (60 px).** Elke rij van 3 px (lijn, vulling, zwart) wordt 4 px (lijn, 2× vulling, zwart). De extra pixel is een kopie van de vulling, dus de poot groeit 1 px naar rechts. Voetkappen gaan van 2 naar 3 px. Knik, plek en voeten blijven gelijk. Rijen die al 4 px waren (heup, rij 45 links en rij 44–46 rechts) blijven zo.

## Toets
16 kleuren, bbox x2–60 y1–62, zwart 15,2 %, lijnpixel midden in een vlak 0, lichte kleur op de buitenrand 0, losse pixels 28 (r12: 29). Dunnepoten: ook 0/0.

## Eerlijk (8× naast r12)
- **Gaten:** beter. Ze zijn weg en L loopt er gewoon overheen.
- **Poten:** dik leest beter en ligt dichter bij het model, waar de poot ±3,4 spritepx is. De knik blijft zichtbaar.
- **Lijnen:** maar een klein beetje beter. De dubbele en trapvormige stukken zijn weg. Maar de lange rechte zwarte naad VL|VR (x36, rij 20–28) en de rechte rand van T (x38, rij 3–9) staan er nog. In het model is de naad een gebogen lobrand. Die zou ik pas veranderen als Jordi die lijnen bedoelt. Ook de losse zwarte streepjes binnen de anemonen (tentakellijnen van r3/r7) heb ik niet aangeraakt, omdat het geen lijnen tussen anemonen zijn.
