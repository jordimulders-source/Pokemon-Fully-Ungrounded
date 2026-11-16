# Pitahaya-draak fase 2, sprite r3 (maker), op r2

Reparaties 1, 2, 4 en 5 uit `keuring_r2/KEURING.md`, plus reparatie 3 als variant. Alles uit het model (3×3-modelblok per spritepixel uit `natief.png`); niets getekend.
- `maak_r3.py` → `pitahaya2_r3.png` (hoofdversie); `python3 maak_r3.py --lipB` → `pitahaya2_r3_lipB.png`.
- **Bewijs:** het script assert dat diff met r2 buiten de zones 0 is en het silhouet gelijk blijft. Hoofdversie 29 px gewijzigd, lipB 31 px. Palet en maat gelijk (12 + transparant, 58×33); zwart binnen 6,5 %.
- Afwijkingen per pixel: `pitahaya2_r3_afwijkingen.txt` en `pitahaya2_r3_lipB_afwijkingen.txt` (letters zoals de keurder: d r p P = roze donker→licht, g G = groen, W wit, K zwart).
- `vel.png`: hoofdversie | lipB | model op 8×; bek op 12× (zelfde volgorde); onderaan 1× en 2× op licht en donker (links hoofdversie, rechts lipB).

## 1 Mondhoek x15–19, y44–51 (19 px)
- Eigen meting: per blok het gemiddelde van de roze modelpx. Bij "dichtstbijzijnde toon" wisselden P en p om en om, want de lichte modelstreep ligt precies tussen die twee tonen. Daarom een strookregel, ook uit het model: staat P bij de twee dichtstbijzijnde tonen → P, anders staat p erbij → p, anders r. Daarna clusters < 3 px één ronde samengevoegd met de buurtint (3 px). Het resterende dambord (17,47)/(17,48) is opgelost met 1 px naar de tint van het modelblok: (17,48) P → p.
- Resultaat: de lichtroze streep loopt doorlopend langs de bekrand van (19,44) naar (15,50). Rechts daarvan p, en r alleen waar het model donker is. (15,49) W → P: het blok heeft < 4/9 wit (de keurder schatte roze; de meting geeft lichtroze).

## 2 Linker lipband (7,50)–(7,53): d → r (4 px)
Het model is daar 70–100 % roze. Zoals de keurder voorschreef: r (177,40,84) dient ook als selout. Het witte vlees raakt de buitenlijn niet meer.

## 4 Dambord (5 px)
- Voorvoet x11–13, y57–58: de gladde groene toonkaart (σ 1,5) geeft dezelfde tinten als r2, want het om-en-om zit op de G/g-grens in het model. Opgelost met 1 px per 2×2 naar de tint die het modelblok het dichtst benadert: (11,58) G → g, (13,57) g → G.
- Een clusterregel wisselde hier alleen om en om (alle 6 px tegelijk omgekeerd); verworpen.
- (9,36): (10,37) r → p. (39,46): (39,46) d → r.

## 5 Onderste lipband (2 px)
- (9,53) en (10,53) W → p. Gemeten: 5/9 roze, en het roze blokgemiddelde ligt het dichtst bij p (gelijk aan de keurder).
- (12,54) blijft K: (12,55) is transparant, dus de buitenlijn zou open komen te liggen (voorwaarde van de keurder niet vervuld).

## Variant B, verre lip (alleen in `_lipB`)
(11,46) en (12,45) w → r (modelblokken 54–72 % roze volgens de keurder). Dit maakt een nieuw 2×2 w/r-dambord op (11,45)/(12,46), dat inherent is aan de dunne diagonaal. De roze strook splitst het grijze gehemelte zichtbaar van het witte vlees.

## Resterend
- Dambordjes buiten de zones zijn alle lijn/vulling of groen/roze aan een rand: (30,36) p/h, (37,42) G/r, en vier K/g op de poten. Niet in de opdracht, dus niet aangeraakt.
