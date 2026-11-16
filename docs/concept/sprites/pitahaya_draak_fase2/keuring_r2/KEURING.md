# Keuring r2 – pitahaya-draak fase 2 (teju), `sprite_r2/pitahaya2_r2.png`

Keurder: onafhankelijk, blind geoordeeld vóór het lezen van `sprite_r2/NOTITIES.md`.
Hulpmiddelen hier: `vel.py` (vel1x_2x.png, vel8x.png), `vergelijk.py` (model64 = 3×3-blokgemiddelde van `natief.png`, uitlijning ox 2, oy −39, silhouet-xor 67 px, bijna allemaal anti-aliasrand), `zij.py` (sprite naast modeluitsnede met spritepixelraster: kop_raster, bek_raster, oog_raster, rug_raster, poten_raster), `meet.py` (tinten, randpixels, clusters < 3 px, 2×2-dambord).
Coördinaten: (x,y) in de sprite.

## Oordeel: FAIL (klein; 4 gerichte reparaties, verder goed)

### Eis 1: trouw aan het model
- Silhouet, pose, kop, oog (zwart ooglid, pupil, wit rechts; lichtroze wenkbrauwbult), neusgat (7,40), kaaklijn, tanden (1 px, les fase 1), rug met schubben en groene punten, groene veinlijnen, staartkrul met gat, dijen met de gele randlichten rechts (staan in het model): trouw. Niets toegevoegd.
- **Kernkenmerk bek:** leest op 1× als wijd open bek met licht vruchtvlees, op 2× zijn de pitjes duidelijk. Grijs gehemelte boven / wit onder klopt met het model (gemeten). Twee kleine trouwfouten, zie reparatie 2 en 3.
- Spike-toppen rij 29–33 zijn op enkele plekken 1 px lager dan het model (model 30–50 % gevuld); valt binnen wat 64 px kan tonen, telt niet.

### Eis 2: Gen 3-techniek
- Zwart binnen de figuur 5,4 % (ok), palet 12 + transparant, licht linksboven ok, buitenlijn 1 px met roze/groene selout aan de lichtkant ok.
- Fout: 2×2-dambord binnen één kleurgroep op 4 plekken, en een ruisige mondhoek van wisselende p/P-losse pixels (reparatie 1 en 4).
- Lichte losse pixels in vlakken apart geteld: W (15,49) (1 px wit naast pit en roze), en 11 losse P/p-pixels in de mondhoek (x15–19, y44–51). Tanden (4,43) en (8,43) zijn bewust 1 px en tellen niet.

## Reparaties (op prioriteit; alles "neem over uit het model", niets tekenen)
1. **Mondhoek x15–19, y44–51** (nu P/p om en om: P (18,44)(18,45)(18,47)(17,48)(16,50)(15,51), p (17,45)(18,46)(19,47)(18,48)(16,49)(17,49)(15,50); dambord (18,45)/(18,46)): neem de zone over uit het modelblok met alleen r/p/P (blokgemiddelde → dichtstbijzijnde modeltoon), daarna clusters < 3 px samenvoegen met de buurtint uit het model, zodat de lichtroze modelstreep als één doorlopende strook langs de bekrand blijft. Ook (15,49) W → uit het model (blok is daar overgang wit/roze; kies roze als het blok niet ≥ 4/9 wit is).
2. **Linker lipband onderkaak (7,50)–(7,53)**: model is daar 70–100 % roze (lipband), sprite heeft de donkere selout d en daardoor raakt het witte vlees ((8,51),(8,52)) direct de buitenlijn. Neem de lipband over uit het model: (7,50)–(7,53) d → r (177,40,84), de modeltoon van de lipband, die hier tevens als selout dient. Silhouet blijft gelijk.
3. **Verre lip (dunne roze strook tussen gehemelte en wit vlees)**: in het model loopt die diagonaal van (8,48) via (9–10,46–47) naar (11,46) en (12,45) (modelblokken 54–72 % roze). De sprite heeft alleen het linkerdeel (x9–10). Neem (11,46) en (12,45) over uit het model als r; pit (13,46) blijft. Maker verwierp dit omdat het de ovaal splitst, maar het staat zo in het model; zet het als variant naast de huidige als Claude twijfelt.
4. **Dambord in één kleurgroep**: voorvoet links (11,57)–(13,58) g/G om en om → neem over uit de gladde modelluminantie (r1-stap T) met clusterregel; (9,36) r/p en (39,46) d/r → 1 px naar de tint die het modelblok het dichtst benadert.
5. (Laag) Onderste lipband (9,53),(10,53): sprite wit, model 45–90 % roze; neem over uit het model (p). (12,54): sprite zwart, model 100 % roze; neem over als p alleen als de buitenlijn op rij 55 sluit.

Diff buiten deze zones: 0 vereist (bewijzen met script, zoals r2).
