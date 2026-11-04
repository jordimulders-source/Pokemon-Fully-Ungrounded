# Salticonda – kleurronde 1 (A en E naast elkaar)

Jordi (letterlijk): "hoe zou je het beter maken? ik vind het er niet per se slecht eruit zien, ligt echt aan hoe we het inkleuren" en "laten we A en E beide proberen uit te werken, ter vergelijking".

Bestanden: `salticonda_A.png`, `salticonda_E.png` (+ `_raster.txt`, één teken per paletindex), `vel.png`.
Scripts:
- `../scripts/kleur1.py` maakt de sprites. De kop is een handgetekend raster (`KOP`). Windingen, gleuven, naden en staart zijn met de hand vastgelegd per variant; de toon per pixel volgt het licht van linksboven.
- `../scripts/check_kleur1.py` controleert alpha-diff, open randen en losse pixels.
- `../scripts/vel_kleur1.py` maakt het vel.

## Game Freak-studie (zware eindvormen, expansion-sprites)
| Sprite | Volume | Licht | Buitenlijn | Patroon |
|---|---|---|---|---|
| Hippowdon | grote egale vlakken; schaduw als brede band onderaan en rechts | linksboven, weinig hooglicht, veel basis | donkere tint van het lijf (olijf/bruin), niet zwart | grote donkere "gaten" met harde rand, weinig details |
| Torkoal | schild als koepel, facetten in 2–3 tinten | hooglicht op de koepelrand linksboven | donkerbruin; zwart alleen in de diepste schaduw | rode vlekken als losse vormen met eigen omlijning |
| Camerupt | vlak rood lijf, schaduw volgt de buik | lichtere rand op de rug | donkerrood | **blauwe ringen** (licht) als patroon op een grote massa: hét voorbeeld voor onze pekelringen |
| Sandaconda | opgerolde bol: één grote schaduwkant rechtsonder | hooglicht linksboven op de bol | donker olijf | dikke donkere band volgt de winding (curve, geen rechte streep) |
| Wailord | enorme ronde massa, 3 tinten blauw en een lichte buik | breed hooglicht bovenop | donkerblauw | buikvlak als grote rustige vorm |

Conclusies voor Salticonda:
- Grote, rustige vlakken, met de schaduw als brede band rechtsonder.
- Gekleurde buitenlijn; zwart alleen rechtsonder.
- Het patroon is één herkenbare vorm die de ronding volgt: ringen zoals bij Camerupt, een band die de winding volgt zoals bij Sandaconda.
- Geen ruis.

## Palet (exact de Silicobra-Uyuni uit `af/`)
| Index | Teken | Kleur | Gebruik |
|---|---|---|---|
| 1 | O | 54,44,42 | warm bijna-zwart, alleen rechtsonder; oogleden, pupil, neusgat |
| 2 | K | 100,86,76 | omlijningsbasis |
| 3 | h | 124,108,90 | omlijning aan de lichtkant, gezichtslijn |
| 4–8 | e d c b a | 146,128,104 → 248,244,232 | zout van schaduw tot hooglicht |
| 9–10 | f g | 220,204,170 / 186,164,126 | gezicht/kaak (warm oker) |
| 11–14 | q r s t | 184,244,228 → 24,92,104 | pekel: ringen, halsband, oogring, staartpunt |
| 15 | | | niet gebruikt |

Geen ijsblauw, geen Nacli-kubussen: hetzelfde palet als de goedgekeurde pre-evolutie. 14 kleuren in gebruik.

## Wat ik deed
- **Volume:** het licht komt van linksboven. De toon is een mengsel van de positie in de rij (links licht, rechts donker) en de positie in de winding: bovenkant licht, onderkant schaduw, en vlak boven elke ring een slagschaduw. Daardoor leest elke winding als een buis en het geheel als kegel. Rechtsonder ligt een brede schaduwband (e), aan de grond donkerder.
- **Pekelringen:** in de gleuven. Bij E 3 px dik, bij A 2 px (dunnere windingen). Bovenaan licht (q links, r), onderaan donker (s, t). Ze buigen in het midden naar beneden (cilinder van bovenaf gezien) en eindigen precies in de inkeping van het silhouet, met turquoise omlijning (s/t) aan de rand. Samen lezen ze als gestapelde cellen. Vonkjes heb ik bewust niet gezet: de lichte q-pixels links op elke ring doen dat werk al zonder ruis.
- **Halsband:** turquoise, onder de kin, loopt aan beide kanten taps uit. Hij herhaalt de pekel-halsband van de pre-evolutie, de belangrijkste herkenning.
- **Zoutkorst:** Y-naden in een middentint, nooit zwart. Drie takken vanuit één punt, trapsgewijs: A 7 Y's, E 5. Ze verdelen de rug van de windingen in grote platen, die de ronde anacondavlekken vervangen. Geen kruisen en geen bakstenen.
- **Kop** (handgetekend, gelijk voor A en E):
  - de zoutkuif als koepel met naden;
  - het half dichte oog zoals bij de pre-evolutie: een eyelid-koepel met donkere rand, de lidlijn O met de hoeken hoog en het midden laag, de turquoise ring (t boven, q/r onder), de pupil O en een glanspixel a;
  - de zachte gezichtslijn (h) tussen het witte gezicht en de korst;
  - de anacondastreep achter het oog (e) met een oker onderrand (g);
  - een lichte snuit met een donker neusgat bovenop de neusbult (Sandaconda);
  - een warme kaak (f/g) en een korte mondlijn.
- **Staart:** banden (e/c) langs de spits en een turquoise punt (r/s) als accupool. De omlijning is K/O, want de staart ligt aan de schaduwkant.
- **Buitenlijn:** h aan de lichtkant (links/boven), K in het midden, O alleen rechtsonder (lijf en staart).

## Bewijs: silhouet bevroren
`python3 scripts/check_kleur1.py`:
- A: **alpha-diff 0** met `silhouet1/variant_A.png`
- E: **alpha-diff 0** met `silhouet2/variant_E.png`
- PNG in palet-modus, transparency = 0, index 0 transparant, 14 kleuren.
- Open randen: **0** (elke randpixel is h, K, O of een pekelomlijning s/t).
- Losse pixels: het script vindt er 29 (A) en 32 (E). Dat zijn allemaal bewuste details: de glans, het neusgat, de pupil, de kuifnaden en de diagonale stappen van de Y-naden. Buiten de kop en de naden zijn er **0** (nagelopen; de laatste twee per variant met `lone` opgelost).

## Checklist SPRITE_NORM
1. **Leest op 1× als Pokémon:** ok. Naast Hippowdon, Torkoal, Camerupt, Sandaconda en Wailord leest hij als een zware slang op een zoutkegel (vel, rij "1x naast de referenties").
2. **3/4 naar links-voor:** ok. De kop kijkt naar links-voor met één oog in beeld (de snuit dekt het verre oog). De kegel heeft geen voor of achter, maar de spiraal en de staart rechts geven richting.
3. **Ledematen:** geen poten. De staart telt, zit vast aan het lijf en komt onder de onderste winding uit.
4. **Geen Escher:** ok. De kop ligt over de bovenste winding, elke winding ligt op de volgende (slagschaduw boven elke ring) en de staart ligt onder de onderste.
5. **Lijf over een echt skelet:** Ekans (silhouetrondes). Gladde curven; de silhouetten zijn bevroren.
6. **Kop:** eindvorm, bewust klein (wall).
7. **Ogen geïntegreerd:** donker bovenlid, iris donker boven en licht onder, glans. Opgebouwd als bij de pre-evolutie, geen brilogen.
8. **Kenmerken op 1× leesbaar:** kuif, oog, halsband, ringen en staartpunt: ok.
9. **Omlijning:** per kleurgroep (zout h/K, pekel s/t); zwart alleen rechtsonder; licht linksboven; geen open randen (script).
10. **Geen Chernobyl:** geen misvormd gezicht, geen beige vlakken uit het niets (f/g alleen op gezicht en kaak, zoals bij de pre-evolutie), geen losse delen.

## Eerlijk oordeel
- **A (4 windingen, ronde 1):**
  - Vier smalle ringen boven elkaar lezen het sterkst als gestapelde accucellen: het meest "Electric".
  - De kop staat iets losser van het lijf door de lucht onder de kin.
  - Het geheel is kleiner (1697 px) en minder imposant dan E. Op 1× is A de drukste van de twee: vier strepen.
- **E (3 windingen, ronde 2):**
  - Zwaarder en rustiger. Drie dikke buizen met elk een duidelijke lichte bovenkant en schaduwonderkant.
  - Leest het meest als "zoutkegel" en "bulky wall".
  - De ringen zijn dikker en vallen minder als strepen op.
  - Mijn voorkeur.
- **Beide:** herkenbaar de evolutie van Silicobra-Uyuni door hetzelfde palet, hetzelfde oog, dezelfde kuif en de pekel-halsband.
- **Keuzes voor Jordi** (smaak, geen fouten):
  - turquoise ringen over de hele voorkant of alleen in de gleuven aan de randen;
  - wel of geen vonkjes.

## Lessen
- Een omlijningsregel die "binnenpixels met een lijnkleur" vervangt, wist ook bedoelde binnenlijnen (oogleden, pupil, gezichtslijn). Beperk zo'n regel tot een zone (hier de rechterrand van de kop waar hij in het lijf overloopt).
- Een halfdicht oog leest pas als oog met een eyelid-koepel (lichte huid met donkere bovenrand) boven de lidlijn. Zonder die koepel wordt de turquoise ring een masker of bril.
- Pekelringen zijn 2–3 px, met de lichte kant boven en de donkere onder, en een slagschaduw van de winding erboven. Dan liggen ze in een gleuf; zonder dat lijken ze geschilderde strepen.
- Buisschaduw per winding (bovenkant licht, onderkant donker) maakt van een kegel met strepen een stapel windingen.
- Meet het aandeel per tint: te veel van de donkerste tint (meer dan ±25%) maakt het zout grauw. De schaduwdrempel iets opschuiven gaf meer middentint.
