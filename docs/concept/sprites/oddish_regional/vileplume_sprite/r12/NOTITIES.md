# Vileplume r12: Jordi's punten op r11 (20 nov)

Jordi: "veel beter, het rondje in het midden van de anemoon moet alleen consistenter, ogen van b zijn goed alleen moet je nog met kleurtinten werken, zoals bij de oorspronkelijke vileplume wss met tinten rood gewerkt is" · "wat betreft de voorste anemonen die in de achterste overlopen, kan je ook fixen met kleurtinten, ik vind juist dat de achterste niet voldoende overlapt met de meest linkse, daar zit een gaatje tussen" · "nu is dat in het model zelf ook niet mooi gelukt" · "dus ik stel voor dat je die achterste in zijn geheel een beetje naar links schuift" (= T, middelste bovenaan).

Basis: r11 met ogen B (`python3 r11/bouw.py B`). Bouwen (vanuit `vileplume_sprite/`): `python3 r12/bouw.py [dx=3]`, `python3 r12/vel.py`.
Bestanden: `vileplume_r12.png` (P, 4 bpp, 16 plekken, index 0 transparant, transparency=0; palet = r11), `vel.png` (r12 | r11 | model 8× / 12× T+L, VL, VR, gezicht / gezicht 12× naast de Vileplume uit de game + 1×), `uitvoer.txt`, `toets.txt`.

## Gewijzigd t.o.v. r11: 185 px (buiten de zones 0; lijf, poten, krater geassert)
| zone | px | wat |
|---|---|---|
| mondjes | 57 | Eén sjabloon voor alle vijf: 6×3, hoeken open; boven 4× zwart, midden zwart–R2 R2 R2 R2–zwart, onder 4× R0. Model: ringen 12–14 natieve px breed (5,2–6,0 spritepx). Plek = gemeten modelmidden (`anemonen.py` MOND), x0=round(cx−2,5), y0=round(cy−1,5): VL x22–27 y21–23, VR x40–45 y19–21, L x12–17 y13–15, R x46–51 y11–13, T x31–36 y5–7 (daarna met T mee naar x28–33). Lijnpixels naast de ring worden R3 waar het model ≥ 40 % licht is (lichte rand). Oude mondpixels krijgen de modeltint. |
| ogen | 2 | Vileplume uit de game: per oog links licht (216,72,88), rechts donker (112,24,16). Hier links geel (254,164,60), rechts roodoranje (249,90,35) van de krater. Vorm en plek gelijk aan r11: (22,32)+(23,32), (31,31)+(32,31). |
| T | 130 | T als geheel (tentakels, mondje, omlijning; eigenaar uit r7) 3 px naar links, over L heen. De krater blijft staan (geen T-pixel op een kraterpixel). Het gaatje met L is dicht op rij 5–9; op rij 1–4 zitten tussen de vingertoppen nog openingen, zoals tussen de andere toppen. Rechts komt een spleet vrij tussen T en R. Op rij 4–8 (x39–41) is die opgevuld met R in schaduw (R1); daarboven is hij transparant. Blootgekomen rand: zwart rechts/onder, R0 links/boven. |
| naad | 11 | Overlap voor/achter met tinten: de achterste anemoon langs de naad een tint donkerder (R2/R3 → R1, R1 → R0), de randpixel van VL/VR een tint lichter (R0/R1 → R2, R2 → R3). Geen zwart. Weinig pixels, omdat r11 de naad al donkerrood/schaduw had gemaakt. |

## Toets
16 kleuren, bbox x2–60 y1–62, zwart 16,2 %. Lijnpixel midden in een vlak: 0. Lichte kleur op de buitenrand: 0.
Losse pixels: 29 (r11: 31). De nieuwe zijn de 4 ooppixels (elke tint 1 px, zoals in de game) en verschoven losse T-toppen. Daarnaast nieuw door de mondjes: (19,14), (21,14), (22,15), (48,16), (51,19).

## Twijfels
- De R1-strook rechts van T (x39–41, rij 5–8) is vlak; R had daar geen eigen inhoud.
- De naad blijft zacht. Wil Jordi meer scheiding, dan kan de schaduw aan de achterkant 2 px breed (voorstel, niet gedaan).
- Het sjabloon is 6 breed. Het VL-mondje is in het model wat smaller (5,2); voor de consistentie is hij even groot gemaakt als de rest.
- De verschuiving is 3 px. Met `python3 r12/bouw.py 4` gaat T verder over L heen.
