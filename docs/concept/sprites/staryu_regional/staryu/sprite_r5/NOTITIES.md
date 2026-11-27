# Regionale Staryu (koekje) r5: keuring + eindkeuring Dragonfly Cave op r4 (verse keurder, 27 nov)

**Eindoordeel: PASS.** r4 was al een eerlijke en trouwe reductie. Deze ronde verandert alleen de uitvoering:
- 17 pixels;
- 1 paletindex;
- silhouet alpha-diff 0 (met assert);
- niets getekend, niets gladgestreken.

Bestanden:
- `staryu_r5.png`: 64×64, P, transparency 0, 14 kleuren.
- `bouw.py`: r4 → r5, met per pixel een assert op de r4-waarde en een reden.
- `vel.py` → `vel.png`:
  - bovenaan r5 | r4 | model op schaal, 8×, wijzigingen blauw omkaderd;
  - onderaan 1× en 2× op wit en donker: r5, r4, model, Gen 3 Staryu, Starmie, Taillow, Skinguin, Dundragoon, Zapacha, Princadee.

Bouwen: `cd staryu_regional/staryu && python3 sprite_r5/bouw.py && python3 sprite_r5/vel.py`.

Meetmaat in deze notities: D = de gemiddelde modelhelderheid van alleen de deegpixels onder een spritepixel (natief raster van het r4-model, zonder chips en zwart). Zo telt het donker van een chip of de buitenlijn niet mee.

## Stap 1: keuring (blind, vóór het lezen van de makernotities)
**Eis 1, accuraat op het model: ja.**
- **Vorm:** het silhouet is de exacte 2×-reductie van het model (alpha-diff 0 met `kaal.png`). De kanteling en de ongelijke armen staan erin; niets is rechtgezet.
- **Onderdelen:** alle chips staan op hun modelplek en hebben de modelmaat (afgeronde 4×4 met een kruisvorm, zoals een cirkel op 2× uitvalt). Het juweel staat op dezelfde plek (midden 27,5; 32,0). Ook de naden vanuit de inkepingen staan erin.
- **Getoaste rand:** in het model is de rand rechts en onder donkerder, zoals een gebakken koekje.
- **Deegtonen:** gemeten volgt de deegtoon de modelhelderheid per pixel. De mediaan D is 117 voor schaduw, 159 voor midden en 192 voor licht.
- **Niet zichtbaar op 64 px:** de dubbele ring van het juweel valt op 9 px weg. Dat telt niet als afwijking.

**Eis 2, Gen 3:**
- **Volume (eerst getoetst): voldoende.** Elke arm heeft licht linksboven en schaduw rechtsonder: bovenarm met naad en randschaduw rechts, rechterarm en rechterbeen met een sikkel van 2–3 px, en een licht midden. Dit komt uit het model; het is geen pillow shading en geen effen tweekleur.
- **Belijning: schoon.** De buitenlijn is 1 px en heeft per arm precies één wissel van selout naar zwart: 128 randpixels, 15 runs. Er staat geen zwart binnen het silhouet. Chips, naden en juweel hebben binnenlijnen in hun eigen donkerste tint.
- **Tinten: binnen de norm.** Het deeg loopt van L 203 via 170 en 131 naar selout 91 (stappen 33/39/40), met hue 38° → 34° → 25° → 21°.

**Kleine punten, door mij uitgevoerd:**
1. **Sikkel te zacht.** Op een paar plekken aan de schaduwkant gaf de 5×5-gladstrijking van de maker middendeeg waar het model duidelijk schaduw heeft (D 109–139). Het gaat om de onderkant van de linkerarmtip, de binnenkant van het rechterbeen in de inkeping en de tip van de rechterarm.
2. **Juweelring om en om.** Links liep de ring 10, 10, 10, **9**, 10, 9. Dat is precies de afwisseling die verboden is.
3. **Losse lichte pixel.** Op (38,47) staat één lichte pixel in de schaduw onder de chip van het rechterbeen.
4. **Te grote stap in het juweel.** Van rood naar licht is de stap L 52, groter dan de ±30–40 van Taillow.

## Na het lezen van NOTITIES.md (r4)
- **Wat klopt:** de maker meldt een eerlijke reductie, 180 px technische opschoning en geen tekenwerk. Dat klopt met mijn meting.
- **Wat ik niet deel:**
  - Zijn twijfel "op 8× wat vlekkerig": de plukken volgen de modelvlakken en blijven staan. Er is niets weggepoetst.
  - Zijn twijfel over het juweel: op 1× leest het als een rond rood juweel.
- **Wat de maker niet zag:** punten 1–4. Punt 1 komt van zijn gladgestreken toonkaart, die het volume aan de schaduwrand iets afvlakte. Punt 2: zijn om-en-om-controle keek alleen naar de buitenlijn, niet naar de juweelring.

## Stap 2: eindkeuring en uitvoering

### Gidscitaten (`docs/lessen/bronnen/dragonflycave_spriting_guide.txt`)
- r. 96: "The 'outline shadows' are always black (or ever-so-slightly off-black)". Zwart alleen aan de schaduwkant van de buitenlijn.
- r. 421–422: "we take the base outlining shade for every color and color all of the outline except the shadows in that color, and remove the clusters so that the outline is always one pixel wide."
- r. 453–455: "Put some of the shadow/outline highlight color on the outlines in the very most highlighted parts … place pixels of the outline highlight color on the inside of the outline rather than the outside."
- r. 117: "The outlines must be reasonably dark". De selout is L 91, de outline base van Gen 3 Staryu L 90.

### (a) Schaduw en volume: 16 px, alle 4 → 3, behalve waar vermeld
Regel: middendeeg met D < 140 aan de schaduwkant, naast de zwarte buitenlijn, wordt schaduw. Zo loopt de sikkel per arm gebogen langs de rand en dunt hij uit naar de tip. Er zijn geen rechte banden bijgekomen.

| zone | px | pixels (D) |
|---|---|---|
| linkerarm, onderkant tip + onderrand | 5 | (12,27) 128, (12,28) 126, (13,29) 139, (13,30) 139, (14,30) 128 |
| rechterbeen, binnenkant in de inkeping + onderrand links | 6 | (30,44) 121, (31,46) 139, (31,47) 109, (32,47) 119, (32,48) 118, (33,48) 121 |
| linkerbeen, rechts bij de inkeping | 1 | (21,46) 120 |
| rechterarm, tip | 2 | (46,27) 137, (45,28) 115 |
| rechterbeen, rechts | 1 | (39,39) 126; de sikkel loopt nu taps 3-2-1 px |
| rechterbeen, schaduw onder de chip | 1 | (38,47): een losse lichte pixel tussen schaduw (vlekje < 3 px) |

Bewust niet gedaan:
- **(37,24) en (38,24), D 137/133, in de inkeping tussen bovenarm en rechterarm.** Die zouden (36,24) als losse middentoon tussen chip en schaduw laten staan.
- **(14,46) en (15,47) op de onderkant van het linkerbeen.** Dan blijft (15,46) als een vlekje van 1 px over.
- **(40,43) en (40,44).** Dan wordt de rechterkant van het rechterbeen een smalle streep 3-4-3.

De lichte plukjes, de barstjes en de naden zijn ongemoeid gelaten.

### (b) Belijning: 1 px
- **Juweelring (23,32): 9 → 10.** Het model is daar licht (D 119, de roze rand van de zetting). De ring loopt nu boven en links in 10 en vanaf linksonder (24,34) via onder naar rechts in 9, met één wissel per kant.
- **Gecontroleerd en goed bevonden:**
  - buitenlijn 1 px, 6 wissels zwart/selout (één per top of inkeping), nergens om en om (trace);
  - 5 outline highlights (3) op de lichtste lijnpixels;
  - geen lichte kleur op de buitenrand, geen zwart binnen het silhouet, geen losse zwarte pixels;
  - chips met een rand in hun eigen donkerste tint (6), niet in zwart;
  - naden in deegschaduw, niet in zwart.

### (c) Kleurtinten: 1 paletindex
- **Juweel licht 12: (244,128,122) L 162 → (240,112,106) L 150.** De stap rood → licht gaat van 52 naar 40, zoals Taillow (37–49) en Gen 3 Staryu (41–47). Hue blijft 3°.
- **Juweelschaal nu:** 9 L 41, 10 L 78, 11 L 110, 12 L 150, glans 13 L 223. Dat is 3 roodtinten met glans en rand, zoals Gen 3 Staryu.
- **Ongewijzigd en binnen de norm:**
  - deeg: L 203/170/131 + selout 91, hue 38/34/25/21 (vergelijk Zapacha 37/31/22/21);
  - chip: rand L 34, midden 66, glans 171.

### Controle r5
- 14 kleuren, alpha-diff 0, 17 px gewijzigd (assert).
- Zwart is 8,1 % van de figuur.
- Vlekjes < 3 px die over zijn:
  - outline highlights;
  - barststukjes;
  - de diagonale sikkeltrap van de linkerarm;
  - 3 middendeegpixels tussen een chip en de lijn, die het model daar licht heeft;
  - chipglans en juweel.

## Ter info voor Jordi (geen ontwerpvragen)
- Geen. De dubbele ring van het modeljuweel kan op 9 px niet; wat leest is een rond rood juweel met een glans linksboven en een donkere rand rechtsonder.
