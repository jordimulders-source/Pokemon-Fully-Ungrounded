# Kleur ronde 10 (maker-agent, 3 nov)

Ronde 10 bouwt verder op ronde 9 (zonder pupil); ronde 10b op ronde 9b (met pupil). Gemaakt met `rijen_ronde10.py`, dat per pixel controleert dat de oude waarde klopt.

Jordi letterlijk:
- "de neus is nog steeds een raar uit stekend streepje"
- "de bovenkant van de binnenste klauw moet nog iets meer belijning, plus de staart idd, die vertaalt niet helemaal lekker vanuit het 3d model"

## Wat er veranderde
- **Neus** (zone x 3–11, y 13–20, silhouet mag mee):
  - Een ronde knop van 4x3 zoals in de render: donker 2, glans 7 linksboven op (11,16).
  - Omlijning 1 aan de buitenkant: (10,16), (9,17), (10,18) en (11,19).
  - Een zachte onderrand 4 naar de crème kin op (13,17) en (12,18); de crème snuit erboven en erachter blijft.
  - Het uitsteeksel van 1 px is weg: de buitenrand loopt nu x 11 → 10 → 9 → 10 → 11.
  - Silhouet erbij: (10,16), (9,17), (10,18).
- **Nabije klauw:**
  - Een donkere selout 4 op de lijfrij boven de hand, (23–28,25), met de hoek (22,25) in 5. Die sluit aan op de bovenrand van de onderarm.
  - De hand zelf, de klauwvorm en de inkeping zijn niet veranderd (script: bevroren K/k/Z geraakt = []).
- **Staartpunt** (zone x 44–58, y 15–33, silhouet mag mee):
  - De punt krult terug met lucht in de bocht: een spleet van 1 px op x 52 (y 24–26), die naar onderen breder wordt (x 51–52 op y 27–28, x 49–50 op y 29) en zo linksonder open uitkomt, zoals de haak in de render.
  - De koepel heeft een lichte boog (5/4) linksboven die doorloopt langs de hangende punt.
  - De punt en de schacht hebben elk een eigen omlijning 1 langs de spleet.
  - De ring op de schacht in de bocht heeft een boven- en onderrand als boog; de schacht is daarvoor 1 px naar rechts verbreed (x 58).
  - Silhouet erbij: (57,20), (48,21), (57,21), (48,22) en x 58 op y 22–28.
  - Silhouet weg: (52,24), (52,25), (52,26), (51–52,27), (51–52,28) en (49–50,29).

## Controles (script)
- Buiten de neus- en staartzone: alpha-diff 0.
- Kleur buiten neus, staart en klauwrand: gelijk aan ronde 9.
- Geen open randen.
- Losse binnenpixels: ronde 10 heeft er 94 (ronde 9: 96), ronde 10b 98 (ronde 9b: 100).

## Zwakke punten
- De lucht in de staartbocht is maar 1 px breed in de bocht zelf. Op 2x leest hij als haak; op 1x is de spleet net zichtbaar.
- De schacht is 1 px breder dan in de render (x 58), zodat punt én schacht een eigen omlijning hebben.
- De neusglans 7 op donker 2 is subtiel; op 1x leest de neus als ronde donkere knop zonder glans.
- De klauwrand is selout 4 en niet zwart. Hij is duidelijk zichtbaar op 4x en 8x; op 1x is hij een zachte donkere rand.

## Lessen
- Een "haak" in een dicht silhouet leest nooit echt. Lucht van 1 px in de bocht, open naar de punt toe, doet meer dan elke kleurtruc.
- De render is bij dunne delen (neus, haak) de maatstaf. Bij het automatisch verkleinen verdwijnen ze; daarna met de hand overtrekken in een aangewezen zone.
