# Sneeuwmonster fase 2 – sprite ronde 1 (maker)

Bestanden: `sneeuwmonster2_r1.png` (64×64, geïndexeerd, index 0 transparant), `kaal.png` (kale reductie), `bouw.py` (alle stappen), `vel.png`.
Gereedschap: `../gereedschap/` (gemeen, pitch, klassen, kaal, steen, controle, zones, vel).

## Werkwijze
1. **Natief raster gemeten** (`pitch.py`, stenenzone uitgesloten): 8,53 en 4,27 scoren vrijwel gelijk → echte cel 4,27 px (1024/240); de mondlijn is 1 cel. De geplakte stenen zitten op ±3,7 px (eigen zone).
2. **Kale reductie** (`kaal.py`): elke modelpixel krijgt een klasse (bg, zwart, sneeuw, hout, grijs, steen, gloed, geel; `klassen.py`), daarna per spritepixel oppervlakgewogen (9,107 modelpx per spritepx). Silhouet = <50 % achtergrond. Sneeuw: aandeel dunne lijnpixels (L<130) ≥0,28 → lijntint, ≥0,15 → schaduwtint, anders toon uit de gemiddelde helderheid van het vlak. Hout: meerderheid van de drie modeltonen. Band/ogen: grijs gaat voor bij ≥30 %.
3. **Stenen als eigen zone** (`steen.py`): vorm = spritepixels met ≥45 % steen; rand zwart of gloed waar het model aan de rand gloeit (rechts/onder); binnen worden de pixels met het hoogste gloedaandeel scheur, precies zoveel als het modelaandeel gloed (28 % / 21 %); 1 grijs facet op de lichtste modelplek.
4. **Gen 3-opschoning**: tintvlekjes <3 px van vlaktinten → buurtint (zelfde groep); losse lijnstippen zonder lijnbuur weg; buitenlijn 1 px: lichtkant (leeg alleen links/boven) = gekleurde selout (sneeuw: tint 2, hout: donker hout), anders zwart; binnenlijnen in/onder de emmer donker hout i.p.v. zwart.

## Palet (16 incl. transparant)
0 transp · 1 omlijning (24,32,56, = fase 1) · sneeuw 2–6: lijn (72,108,136), schaduw (118,158,186), midden (160,194,214), licht (204,228,240), hoog (240,250,252) — tussen de modeltinten (koeler cyaan) en fase 1 in, zelfde helderheden als het model · hout 7–9 (104,60,32) (160,104,56) (204,144,88) uit het model · grijs 10–11 (88,92,104) (160,166,176) uit band/ogen · steen 12 (52,50,58) · gloed 13–15 (216,72,32) (240,136,40) (248,208,64).

## Afwijkingen van de kale reductie (310 px, `zones.py`)
- **omlijning/vacht 130**: 123 daarvan zijn de buitenlijn (selout/zwart) en ontkorrelen; geen vormwijziging (silhouet = kaal, diff 0 in de alfa).
- **emmer 55**: buitenlijn + binnenlijnen zwart→donker hout; ontkorrelen; 1 pixel (30,3) gevuld: inkeping in de bovenrand die het model niet heeft.
- **ogen 20 (beschermd)**: de reductie gaf een plusje en een vlek zonder spleet. Maat en plek gemeten op het model: linkeroog x21–24, y19–23 (4×4,2 px), spleet rij 21; rechteroog x30–34, y20–24 (4,6×4,6 px), spleet rij 22. Gezet als ronde grijze schijf (grijs 10, licht 11 linksboven) met zwarte spleet over de hele breedte, zoals de dichte ogen van het model. Niet getekend: maat, plek en spleetrij uit de meting.
- **mond 8 (beschermd)**: de 1-cel-lijn viel half weg. Lijn in lijntint 2 op de gemeten modelplek: rij 25 x21–28, rij 26 x29–33 (het model zakt rechts), krul links (20,24), zwart eindje (34,25) waar het model zwart heeft.
- **baardfranje 62 (beschermd)**: de zigzag valt bij de reductie uiteen (lijn 0,47 spritepx). Per spritekolom de rij met de modellijn gemeten (profiel per natieve kolom, zie `bouw.py` stap 6) en de grote tanden gehouden (kleine tandjes < 1 spritepx vallen samen): pad x14–40, diepste punten x26 en x32–33 (rij 33), hoogste x18/x20 (rij 27) en x35/x40; steile tanden verticaal verbonden; 1 px lichtblauw (tint 5) eronder zoals de schaduwrand onder de lijn in het model. Oude lijnstukjes in die zone (2/3) eerst naar wit.
- **stenen 35**: zie stap 3 (alleen modelaandelen, niets getekend).

## Maat
bbox x8–55, y3–58 (48×56 px), 1781 px; onderkant rij 58 (fase 1: rij 52 bij 42 px hoog; Snorlax 58, Ursaring 62), horizontaal gecentreerd (8 links, 8 rechts).

## Controle
16 kleuren incl. transparant; geen lichte kleur op de buitenrand; losse zwarte pixels: (34,25) = zwart mondeindje uit het model, (23,40) = rand van de onderste steen. Kleine "vlekjes" in tint 2/3 zijn diagonale lijnstukjes (4-buren), geen ruis.

## Zelf nog zwak (voor ronde 2)
- Stenen: scheuren binnenin nog vooral een oranje klodder rechts-midden; het model heeft een zigzagscheur dwars door de steen.
- Emmer: rechterhelft vrij effen donker; duigen lezen niet (in het model wel, als donkere lijntjes onder de band).
- Linkerarm: veel losse vachtstreepjes in tint 2/3 (model heeft daar ook strengen, maar drukker dan nodig?) – meten, niet gladstrijken.
