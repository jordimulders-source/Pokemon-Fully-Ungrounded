# Uku Pacha r3: notitie van de maker

**Bestand:** `uku_pacha_r3.png` (64×64, geïndexeerd, index 0 = transparant, **16 kleuren incl. transparant**, zelfde palet als r2). Vel: `vel.png` (r3 | r2 | model op 8×, koppen en kronkels op 12× naast het model, r3 op 1×/2× op licht en donker).
**Silhouet:** alpha-diff met r1/r2 = **0**. **Lijnen weggehaald: geen** (kronkelzone r2 282 lijnpixels, r3 274: alle modellijncellen opnieuw geprojecteerd, alleen dubbele dikte gedund).

Alleen de vier benoemde reparaties van de coördinator; buiten de kronkelzone (rij ≥ 41) zijn alleen 4 ogpixels en 2 nekpixels veranderd (pixeldiff r2 → r3: 349 px, waarvan 6 boven rij 41: (39,4), (39,5), (39,6), (41,6), (26,19), (25,20)).

## Scripts (volgorde; reproduceerbaar, diff 0)
`koppen.py` (op `raster_auto.txt` uit r2) → `kronkel_lijnen.py` → `banden.py 2.0` → `afwerk.py` → `check.py`, `lijnfreq.py`, `vel.py`. Meetgereedschap: `punt.py`, `zoom.py`.

## 1. Kronkels per band (belangrijkst)
- `blokken.py` (r2: elk blokje tussen twee segmentlijnen één toon → mozaïek) is vervallen.
- **Lijnen in twee lagen** (`kronkel_lijnen.py`): in het model is de spiraal (omlijning, binnenste ovaal, middenring, binnenboog rechts) zwart/bijna-zwart (modelklasse 0–1, samenhangende stukken ≥ 8 cellen); de schubsegmenten zijn kort en navy (klasse 2–4). Eerst de spiraal geprojecteerd en los gedund (zodat segmenten haar niet opeten) → **K, doorlopend**; daarna de segmenten, gedund met de spiraal vast.
- **Toon per band** (`banden.py`): het model heeft geen gesloten contouren die de banden afsluiten (de band leest door zijn toon). Daarom op het natieve modelraster de helderheid van de vlakcellen per toongroep (lichte buikband = modelklassen 13–15, donkere lijfbanden = 5–12) gladgestreken (gauss σ = 2 natieve cellen ≈ 1,4 spritepixels, genormaliseerd binnen de groep), en per spritepixel op de ladder van zijn groep gezet. Het licht-donker van de band volgt zo de modelronding (boven/links lichter, onder/rechts donkerder); losse schubblokjes gaan erin op. σ getest op 1,5 / 2 / 2,5 / 3,5: bij 1,5 blijft het mozaïek deels staan, vanaf 2,5 verdwijnt de donkere onderband van de rechterkronkel (die het model wel heeft); 2 gekozen.
- **Segmentlijnen delen de band niet meer op:** waar een segmentlijn alleen tussen s/m/b ligt, is hij één tint donkerder dan de band (d) in plaats van navy (94 px); op donkere stukken en in de lichte buik blijft hij navy. Geen segmentlijn verdwenen.

## 2. Rechteroog
Model 1-op-1 verkleind (natieve cellen x 61–65, y 10–13 gemeten per spritepixel): geel (40,5), (41,5), (39,6), (40,6); donkere hoek (41,6) (modelcel (64,13) donkergroenblauw); zwarte rand/spleet (38,5), (39,5) (modelcellen (60,12), (62,11–12)); wenkbrauw (40–41,4) (modelcellen (63–65,10)); (39,4) basis (b) i.p.v. zwart (modelcellen daar grijs). De gele T is weg.

## 3. Buitenomlijning kronkels
Rond de kronkels (rij ≥ 43, geen vleugel) is de buitenrand rondom zwart, zoals het model (DC-kleuring van de omlijning pas in de eindkeuring). Elders blijft de r2-omlijning.

## 4. Zwakke punten 2 en 3 uit r2
- 1-px blokjes: de zes van r2 zijn weg (opgegaan in de band). Over: **(15,53)**, een pocket van 1 px tussen een spiraallijn (14,53) en een segmentlijn (16,53) waar linkerkronkel en buik elkaar raken; dichtzetten zou twee lijnen samenvoegen, dus laten staan.
- 2×2-lijnklonten: nekknik (25–26,19–20) naar een 1-px trap (2 px: (26,19) → s, (25,20) → b; lijn blijft diagonaal doorlopend); (26,42), (12,48) en (26–27,62) zijn weg door de nieuwe projectie. Over: **(41–42,39–40)**, de vleugelklauw, een 2 px brede uitsteeksel van alleen omlijning (geen binnenruimte om te dunnen), en (5,22) in de open bek (donker mondbinnenwerk, geen lijn).

## Lijnfrequentie (ter info, niet toegepast)
Arbok: banden staart 6–7 px, buik 5–8 px; automatisch mediaan 3,0 / gemiddeld 4,0 px. r3: mediaan 3,0 / gemiddeld 4,5 px (de 94 segmentlijnen in d tellen in die meting niet als lijn; inclusief die zit r3 op het niveau van r2, gemiddeld 3,8 px).

## Zelfgenoemde zwakke punten
1. **De spiraal van de rechterkronkel leest beter dan in r2, maar nog niet zo vloeiend als in het model.** De binnenboog rechts (model x 74–77 → sprite x 48–50) ligt maar 2–3 px van de buitenrand (x 51–53), dus de buitenste band is daar smal; de bovenkant van het binnenovaal valt samen met de buitenrand boven het gat onder de vleugel (zoals in het model). Verder kom ik zonder lijnen weg te halen of te hertekenen niet.
2. Restpunten uit 4: (15,53) en de vleugelklauw (zie hierboven).
3. De segmentlijnen in d zijn een nieuwe tint voor een lijn (het model heeft ze navy); gekozen omdat de opdracht vraagt dat ze de toonopbouw van de band niet opdelen. Als Jordi ze navy wil: één regel in `banden.py`.
