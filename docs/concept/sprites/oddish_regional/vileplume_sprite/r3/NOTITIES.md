# Kelp-/anemoon-Vileplume frontsprite, ronde 3 (kandidaat)

Bestanden: `vileplume_r3.png` (64×64, geïndexeerd 4 bpp, 16 paletplekken, index 0 transparant met transparency=0; 14 kleuren gebruikt incl. transparant), `kaal.png` (kale reductie), `bouw.py`, `vel.png` (r3 8× | r2 8× | model 8× op dezelfde schaal / close-ups 12× krater, anemoon voor-links, lijf+poten naast het model / 1× op licht en donker + model 1×).
Opnieuw bouwen (vanuit `vileplume_sprite/`): `python3 gereedschap/natief.py; python3 r1/kaal.py; python3 r3/bouw.py r3`. Toets: `python3 gereedschap/toets.py r3/vileplume_r3.png`.

## Wat uit het model komt
- **Natief raster** 5,12 px (200×200; figuur x36–163, y28–171 = 128×144). De randsterktezoeker gaf 10,24 (zoals bij de Oddish), maar krater en tentakels staan op het halve raster.
- **Formaat:** S = 0,43 → figuur **x4–58, y1–62 = 55×62 px** (1617 px). 56 breed zou 63–64 hoog geven en past niet met 1 px marge, dus 55. Vileplume in de game: x4–59, y5–56 (56×52); de top (anemonenring) is hier 55 breed, de poten maken hem 10 px hoger. Voeten op y62 (1 px marge).
- **Kale reductie** (`r1/kaal.py`): oppervlakteweging, meest voorkomende modelklasse per spritepixel, lijnen (zwart/R0/W0) vanaf 30 % dekking. Palet = mediaan van de modelpixels per klasse; geen eigen kleuren.
- **Krater:** kale reductie: zwarte rand, grijze ring, bruine binnenrand, roodoranje (249,90,35) bovenin en geel (254,164,60) in het midden (gemeten in de kom). Fel oranje-geel binnen zwart.
- **Lijf, armen, poten:** kale reductie + technische opschoning (zie telling).

## Toegestane afwijking (Jordi, optie A): klonteren
Per anemoon (VL, VR voor; L, R, T achter; mondjes en schijfmaten gemeten op het natieve raster, `gereedschap/anemonen.py`):
- 9 klonten (Jordi: ±8–10), sectoren van 40° gedraaid tot de lichte modeltentakels zo veel mogelijk in de kernen vallen. Richting = massamidden van de modeltentakels in de sector; punt = 92e percentiel van waar die tentakels eindigen (dus ook de punten boven de achterste anemonen); lengte 0,45 terug naar het mondje (kort). Bij de voorste anemonen vallen er geen weg; bij de achterste zijn de verborgen klonten niet zichtbaar.
- Klont = dik lijnstuk van 2,4 spritepx, in de modeltentakeltint (R3; bij T R2, zoals het model).
- Lijf ertussen in de modelschaduw (R2, R1 aan de onderrand).
- Lijnen: R0 aan de schaduwkant (rechts/onder) van elke klont en tussen klonten die elkaar raken; zwart waar een achterste anemoon aan een voorste grenst (donkere rand om elke anemoon); bij een punt tegen de achtergrond komt de lijn buiten de klont.

## Pixels die niet uit de kale reductie komen: 818 (van 1617)
Per zone: **anemonen 721** (waarvan mondjes 35) · **lijf+armen 37** · **poten 56** · **krater 4**.
Per stap: klonteren + mondjes 591 · klont- en anemoonranden 274 (overlapt) · kratergrijs 1 · lijn midden in poot/lijf → vultint 17 · poten 3 px 45 · buitenlijn 109 · losse pixels 31 · kraaglijn 3 · ontkorrelen 28.
- Anemonen: bijna volledig opnieuw opgebouwd uit modelmetingen; dat is de afwijking van optie A.
- Mondjes (35): ovaal R0-ring met R2 binnen, precies op de bbox van de modelring (VL x22–26 y21–23, VR x40–45 y19–21, L x11–16 y13–15, R x46–51 y11–13, T x31–36 y5–7). De reductie maakte er een streepje van; benoemde reparatie zoals een oog. Het model is 2,2 spritepx hoog, de ovaal 3.
- Poten (56): het model is 6 natieve px = 2,6 spritepx (lijn-vulling-lijn); de reductie wisselde 2 en 3 px, en 2 px = twee lijnen zonder vulling. Elke rij is nu 3 px (W0 – vulling – zwart, zoals het model); de extra pixel staat aan de kant met de meeste modeldekking.
- Lijf (37): kraaglijn (U, 3 px), lijn midden in een vlak → vultint, buitenlijn, ontkorrelen.
Geen pixel is vrij getekend: alles is een modelklasse, een modelmeting of een benoemde regel.

## Toets
- Kleuren: 14 incl. transparant (zwart, 4 rood, W0 + 3 wit/grijs, kratergrijs, kraterbruin, roodoranje, geel).
- Stappen anemonen (L): R0 66 → R1 93 → R2 130 → R3 163 (±30–37). Lijf: W0 58 → 182 → 209 → 239.
- Losse pixels (geen gelijke 8-buur): 11, alle bewust: 4 zwarte/R0 puntjes op tentakelpunten aan de buitenrand, 3 in de krater (bruin, oranje, grijs uit het model), 1 R0 op de buitenrand van R, 1 R0 op de onderrand van VL, 2 rond de oksel van de rechterarm (lijn van de arm).
- Lijnpixel midden in een vlak zonder lijnbuur: 0. Lichte kleur op de buitenrand: 0.
- Tintvlakjes < 3 px: R2 6 en R3 1 die alleen tegen lijnen/achtergrond liggen, W2 1 (voet); verder 0.
- Belichting: selout linksboven (R0 aan de rode bovenrand, W0 links aan lijf en poten), zwart rechts/onder. Zwart 16 % (Gen 3 ±12–19 %).

## Resterende twijfels (eerlijk)
- **De anemonen lezen nu als bloemen met brede bloemblaadjes**, niet meer als franje van dunne tentakels: dat is het gevolg van klonteren op 2,4 px. Of dit het "dikke, korte tentakels" is dat Jordi bedoelde, moet hij zien; smallere klonten (2,0) gaven weer ruis.
- De kroon van de achterste anemonen (L, T, R) heeft 4–5 dikke punten tegen de achtergrond; het model heeft daar 6–8 dunne. Silhouet bovenaan dus minder stekelig.
- "Kort" heb ik gelezen als: punt op de plek van de modelpunt, lengte 0,45 van de straal terug naar het mondje. Dat is een eigen lezing van "korte"; vraag Jordi bij twijfel.
- De krater is donkerder dan in het model: de grijze ring is maar op een paar plekken 1 px (meest zwart), omdat de ring in het model 2–3 natieve px = 1 spritepx is.
- De kraaglijn (U) bovenop het witte lijf staat zo in het model, maar kan op 1× als glimlach lezen.
- Mondjes 3 px hoog waar het model 2,2 is.
- Breedte 55 i.p.v. 56 (marge).
