# Charlatan-Alakazam: kleur r6

Vanaf het raster van r5 (`basis_r5.txt`). Stap: `python3 apply.py basis_r5.txt raster.txt r6`, daarna `vel.py`, `controle.py`, `lijnkaart.py raster.txt lijnkaart_r6.png 0 0 64 64 10 0.3` en `box1x.py`. Er zijn 85 px gewijzigd, allemaal binnen de opdrachtzones (pixeldiff buiten de zones: 0, met script bewezen).

## Gedaan
1. **Onderarmen grijs** (SPEC; Jordi: "onderarmen en bovenbenen wil ik sowieso niet zwart hebben"). De zwarte omlijning blijft staan; de bovenarmen blijven zwart. De grens bij de elleboog is de bestaande lijn (links rij 33, rechts x39/40).
   - Links x12–20, y34–39. Tinten: a linksboven (12–13,34) en (12,35), dan b, c en onderaan d (17–20,39) als schaduwsikkel. Rij 39 x17–20 hoort bij hetzelfde blok tot de lijn op rij 40 en is daarom meegenomen.
   - Rechts de lange horizontale arm x40–48, y32–37. Bovenaan a (44–46,33), dan b (rij 32–34), c (rij 35–36) en d onderaan (rij 37 en (48,36)). Het korte stuk onder de kaak (x37–40, y28–33) blijft zwart als bovenarm.
   - In het model zijn deze stukken één zwart vlak zonder binnenlijnen. Er is dus geen binnenlijn overgenomen.
2. **Tapse vingerlijnen:** (12,39), (14,39), (14,40), (52,32), (53,32) en (52,34) d → c. De d bij de vingertoppen blijft staan.
3. **Rechteronderarm:** (49,31–34) c → b. Met de grijze onderarm ernaast past dat; de lijn x48 scheidt onderarm en pols.
4. **Schoppen links:** (9,39) o → w.
5. **Linkerknie:** (19,48) n → m en (20,47) m → n. De glans is nu een blok van 2×2 op (19–20,46–47).

## Controle
- Alpha-diff 0. Open randen 0. Losse o 0.
- Clusters kleiner dan 3 px: 11. Vijf daarvan komen uit deze ronde en zijn de tapse uiteinden van de vingerlijnen: de c-pixels (12,39) en (14,39–40), en de d-resten bij de vingertoppen (54–55,32), (53–54,34) en (12,40–41). De overige 6 zijn dezelfde als in r5 (krulvulling, streng, teenlijn, klauwen, selout).
- Lijnkaart: 46 rood en 90 blauw (r5: 45 en 91). Het verschil is (9,39): de modellijn daar is nu wit.
- 1×: `box1x_r6.png`.

## Zwakke punten
- **Onderarmen in het model:** daar zijn ze zwart. Het grijs volgt SPEC; de toon verschilt dus bewust van het model.
- **Elleboog links:** de overgang van de grijze onderarm naar de zwarte romp loopt via de bestaande lijn x21. Die is één pixel dik.
