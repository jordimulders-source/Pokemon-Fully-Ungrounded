# Pitahaya-draak fase 3, sprite r13 (maker): de 5 pixels van Jordi in r12

Jordi (letterlijk): "check bij de 5 pixels die ik gelijnd heb of de schaduwkleur nog klopt" — (8,30) (9,30) (10,30) (grijs w, onderste vleesrij) en (8,31) (9,31) (ondertanden W).

- **Basis:** `../sprite_r12/pitahaya3_r12.png` (kaakvariant r12; wordt alt gekozen, dan dezelfde pixels op alt zetten, ze overlappen niet).
- `python3 maak_r13.py` schrijft F/G/H + `pitahaya3_r13_afwijkingen.txt` (wijzigingen alleen in x 7-10, y 26-32; silhouet gelijk). `python3 vel.py <tijdelijke map>` maakt `vel.png`: kop 12× (x0-22, y18-36) F | G | H | r12 | model, hele sprite 6×, 1× en 2× op licht en donker naast Salamence/Tyranitar/Sceptile.

## Oordeel over r12
De schaduw klopt niet: met licht linksboven valt schaduw in de bek onder de bovenkaak (bovenrij y26, klopt) en achterin (rechts), niet onderin vooraan. Het grijs op y30 x8-9 scheidde alleen vlees van tanden. En witte tanden (W) onder grijs vlees zijn lichter dan het vlees dat dichter bij het licht ligt: omgekeerd.

## Model gemeten (mediaan per spritepixel)
- y29 x8-10: wit vlees (±250).
- y30 x8-10: donkerroze tandvlees (154,55,91) / (154,95,117) / (131,49,77).
- ondertanden y31: x8 (107,90,93) donker, x9 (179,174,178) lichtgrijs; hoektand (6,31) (146,138,143). De ondertanden staan in het model dus in de schaduw (grijs), niet wit.

## Varianten (lichtlogica)
- **F** (6 px): vlees wit tot onderaan (8-9,30 W), alleen achterin (10,30) w. Tandvlees d als korte scheiding op (8-9,31) (zoals het model, waar tandvlees tussen vlees en tanden zit), tanden 1 px lager in de lip: (8,32) W, (9,32) w (rechterhelft van de tand in schaduw). Licht: vlees vooraan in het licht, tanden voor in de lip ook licht.
- **G** (4 px): vlees wit (8-9,30), achterin w (10,30). Ondertanden in de schaduw van de bovenkaak zoals in het model: (8,31) w, (9,31) q (naar achteren donkerder). Scheiding vlees/tand door toon, geen extra lijn.
- **H** (3 px): vlees vooraan wit (8,30), schaduw groeit naar achteren (9-10,30 w, aansluitend op de grijze achterkant (11,27)). Ondertanden allebei lichtgrijs w (model ±179). Scheiding vooraan door toon (W vlees / w tand), achterin loopt het grijs vlees-tand door.

## Eerlijk
- G volgt het model en de lichtlogica het best; de tanden lezen als tanden in de schaduw, het vlees als wit.
- F leest het duidelijkst als losse tanden, maar verschuift de tanden 1 px t.o.v. het model en zet een (korte) donkere lijn terug.
- H is de rustigste, maar achterin (9,30)/(9,31) lopen vlees en tand in één grijs over.
