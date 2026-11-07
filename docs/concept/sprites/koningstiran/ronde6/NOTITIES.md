# Sapa Inca – ronde 6 (naar Jordi's krabbel op ronde 5b)

Basis: `ronde5b/sapa_inca.txt`; de wijzigingen staan onderaan in het blok "ronde 6". Bestanden:
- `sapa_inca.png`, `sapa_inca.txt`, `bouw.py`, `kijk.py`
- `uitlijn.py` → `uitlijning.npy`, `krabbel_punten.txt`
- `overlay.py` → `overlay.png` (rode lijnen op ronde 5b en ronde 6, 8×)
- `controle6.py` (diff per zone t.o.v. ronde 5b)
- `vel.py` → `vel.png` (4×; het hele lijf op 6× naast ronde 5b; overlay; 1×)

Jordi: "ja nu heb je er een paar bruine pixels neergezet. De staf is een rechte streep die nog steeds achter zijn vleugel lijkt te zitten, omdat die dus niet over de vleugel heen overlapt, dat moet een klein beetje, totdat die hem vast pakt. Daarnaast is het ook weer een rechte lijn als die achter zijn lichaam verdwijnt, ook niet mooi. Het lichaam zelf is ook niet zo goed, is wat teveel uitgedijt en dus niet mooi een ovalerige afwerking. Plus de gele buik is nu een soort van ballonvorm met tuitje geworden. De poten zijn nog niet netjes afgewerkt qua kleur en schaduw. Ik heb een rood puntje gezet op de onnodige bruine pixels".

## Uitlijning van de krabbel (`uitlijn.py`)
Brute-force zoeken naar de schaal en de verschuiving waarbij het kleurverschil tussen de krabbel (zonder rood) en de geschaalde ronde 5b het kleinst is: **8,25 px per spritepixel, verschuiving x +11, y +6** (gemiddeld kleurverschil 10,4). Rood = R > 190, G < 45, B < 55.
Rode lijnen in spritecoördinaten (x per rij):
- **Rechterflank (omtrek):** (36,33) → (37,35) → (38,37) → x39 op rij 39–47 → (38,48) → (37,49–50) → (36,51) → (34–35,52).
- **Binnenlijn rechts (rand buik/flank):** x34 op rij 38–45 → (33,46–47) → (32,48–50) → (31,51) → (30,52–53).
- **Boog linksonder (buik/lijf):** (20,45) → (21,47) → (22,48) → (23,49) → (24,50) → (25,51–52).
- **Rode stip:** (17–18,48), de bruine pixels.

## Wat er veranderde
1. **Bruine pixels weg:** de lichte flankpixels (17–18,48) en de opvulling eronder zijn weg; daar is nu lucht.
2. **Staf vóór de vleugel:** de staf (zelfde kolom x14–16, schacht x15) loopt nu op rij 37–41 vóór de bovenarm langs, met vleugel links én rechts ervan. Op rij 42 vouwt de vleugelpunt er met een lichte vouwrand (l) overheen, en op rij 47 komt hij eronder tevoorschijn.
3. **Achter het lijf:** de staf buigt onder de vleugel in een boog (rij 47–48 recht, 49 +1, 50 +1, 51 naar rechts) naar het lijf. Hij verdwijnt achter de ronde onderkant van het lijf op (24,51); de oude knik en de wig zijn weg.
4. **Lijf:** de rechterflank volgt de rode lijn (rij 48–52 1 px naar binnen, ronde onderhoek). Linksonder is de opvulling weg: de omtrek volgt de rode boog (x21 → x25) en gaat over in de linkerdij.
5. **Buik:** onderaan rond in plaats van een tuitje. Het goud loopt in een boog langs de rode lijn linksonder naar een ronde onderkant (x25–30, rij 51–52). De zachte overgang a → l → m aan de rechterkant ligt op de rode binnenlijn.
6. **Poten:** licht van linksboven: omlijning a links, lichtste tint (y) bovenaan dij en scheen, zwart alleen aan de schaduwkant rechts. De dij heeft een donkere zoomrij (aaaa/aaaaK), dan volgt een smallere scheen en dan de voet. Links is de scheen 2 px + zwart, rechts 3 px + zwart. Opbouw naar Honchkrow/Staraptor: dij, scheen en voet elk een eigen vlak.

## Diff t.o.v. ronde 5b (`controle6.py`)
| Zone | Gewijzigd |
|---|---|
| kroon | **0 px** |
| gezicht en ogen | **0 px** |
| opgeheven rechtervleugel | **0 px** |
| staf + zon boven de hand | **0 px** |
| linkervleugel (behalve waar de staf eroverheen loopt) | **0 px** |
| staf vóór de vleugel + vouwrand (x14–16, rij 37–42) | 17 px |
| staf onder de vleugel + boog + rode stip (x12–23, rij 47–52) | 27 px (silhouet −16) |
| buik + lijf (x20–39, rij 34–52) | 41 px (silhouet −4) |
| poten (rij 53–62) | 13 px |
| rest | 0 |
- Silhouet: **−20 px**, +0 (1640 → 1620). 0 open randen; aandeel zwart 0,13.

## Zelf gekeken (1× en 6× naast ronde 5b, overlay)
- Het lijf is smaller en de buik eindigt rond. De staf ligt boven de hand vóór de vleugel en hangt onder de vleugel in een boog naar het lijf. Linksonder is geen klont of bult meer.

## Eerlijk: wat nog niet klopt
- **Buik:** de onderkant loopt nog steeds iets taps naar het kruis (x25–30); hij is rond, maar Jordi kan er nog een lichte "druppel" in zien.
- **Staf onder de vleugel:** het laatste stuk (rij 51, x18–23) is een korte horizontale strook die het lijf in gaat; op 6× leest de boog als boog, maar het eind is vlak. Doordat de opvulling linksonder weg is, hangt de boog nu vrij in de lucht onder de vleugel. Dat leest als staartveer (hybride), maar het kan ook als losse sliert lezen.
- **Vleugel:** onder de vleugelpunt is op rij 47 nog een stukje donkere flank (x19–21) zichtbaar.
- **Poten:** links blijft de scheen dun (2 px + zwart, het oude silhouet); de voetjes zijn niet herzien.

## Lessen
- Een krabbel op een vergrote screenshot uitlijnen kan met een kleurverschil-zoektocht over schaal en verschuiving (grof rooster, daarna fijn); de bounding box is onbruikbaar door randen in de screenshot.
- Rood in de krabbel streng filteren (R > 190, G < 45), anders tellen de rode kroontinten mee.
