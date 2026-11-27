# Regiaqua frontsprite, ronde 1 (maker)

Bestanden: `regiaqua_r1.png` (64×64, geïndexeerd, index 0 transparant, 11 kleuren incl. transparant), `kaal.png` (kale reductie), `vel.png` (r1 8× | kaal 8× | model op dezelfde schaal / 1× en 2× op wit, crème, grijs, donker, zwart + model 1× / r1 8× naast Regice en Registeel gba).
Bouwen (vanuit `docs/concept/sprites/regiaqua/`): `python3 sprite/r1/natief.py && python3 sprite/r1/kaal.py && python3 sprite/r1/bouw.py && python3 sprite/r1/vel.py` (scipy nodig).

## Metingen
- Rasterpitch model (`pitch.py`/`natief.py`): 10,24 px (1024/100), fase x 9,25 / y 9,20. Figuur natief 81×65 (x8–88, y17–81).
- Schaal 62/81 = 0,765. Sprite x1–62, y12–61 (62×50), 1810 px, onderkant op rij 61 zoals Regice, horizontaal gecentreerd. Niet gespiegeld.

## Kale reductie (`kaal.py`)
Klasse per natieve pixel: achtergrond (flood fill van wit vanaf de rand; witte strepen binnenin blijven figuur), zwart, stip (cyaan), watertoon 0–6 (helderheidsclusters 60/86/110/140/166/205). Per spritepixel 8×8 subpunten: achtergrond als figuur < 50 %, anders de klasse met het grootste gewogen aandeel (zwart ×1,4, lichte tonen ×1,6, stip ×2), zodat strepen en lichtvegen scherp blijven en niet uitmiddelen. Silhouet, beide losse handen met witte opening, inkepingen, richels en draaistrepen komen hieruit; silhouet-diff 0.

## Afwijkend van de kale reductie: 340 px (silhouet ongewijzigd)
- lijf 206: buitenlijn 79, tussentoon opdelen 95, zwart binnen → binnenlijn 15, ontkorrelen 24
- stippen 25: stippen 22, tussentoon 3
- hand links 60: buitenlijn 31, tussentoon 19, ontkorrelen 6, binnenlijn 4, lijn 1 px 4
- hand rechts 49: buitenlijn 32, tussentoon 8, ontkorrelen 4, binnenlijn 5, lijn 1 px 1
Stappen (`bouw.py`):
1. stippen: kale stippixels → omringende watertoon; 7 blokjes 2×2 op de gemeten modelplek (centra omgerekend), 1 px tussenruimte: rij van 4 op x22/25/28/31 y31, boven x27 y28, onder x25 en x30 y34; linksboven 1 lichtere pixel (zoals Regice). Kleur cyaan (0,206,188) + (176,255,236).
2. zwart binnen het silhouet (richels, vingerlijnen) → binnenlijn in de donkerste eigen tint (10,38,68).
3. buitenlijn 1 px: schaduwkant (normaal rechts/onder) zwart, lichtkant binnenlijntint; dunne zijkanten volgen de kant.
3b. tussentoon 2 (vrijwel gelijk aan zijn buren) → toon 1 of 3 volgens de modelhelderheid van dat vlak: een tint minder, hardere grenzen.
4. ontkorrelen: alleen losse pixels (8-samenhangend) van toon 0–4; 2-px stukjes (streepjes) en glans (toon 5–6) blijven.
5. dubbele lijn in de vingerinkepingen (modelzwart + buitenlijn): (45,8) (45,9) (46,7) (47,7) (48,52) → watertoon van de buren.
Geen pixels getekend: elke vorm, streep en lichtveeg komt uit het model.

## Palet
0 transparant · 1 zwart (16,16,24) · water toon 0 (16,64,100), 1 (22,98,128), 3 (60,156,174), 4 (98,186,198), glans 5 (150,214,220), 6 (228,246,246) · stip (0,206,188) / licht (176,255,236) · binnenlijn/selout (10,38,68).
Modelmedianen (9,55,84) … (224,241,245), een stap lichter gezet richting Gen 3 (Kyogre/Sharpedo-gba: donkerste vulling L≈60, stappen ±30).

## Twijfels
- Water heeft 4 tinten + 2 glanstinten (zoals Kyogre-gba), meer dan "≤3 per groep"; minder tinten zou de draaistrepen van het model wegpoetsen.
- Links liggen de onderkanten van de richels (30–31, 37–38) zwart in een verder donkerblauwe lichtkant: schaduw onder de overhang, zoals het model.
- Stippen staan op een raster van 3 px (Gen 3-Regi's); het model heeft iets meer ruimte tussen stip 3 en 4 en tussen de rijen.
