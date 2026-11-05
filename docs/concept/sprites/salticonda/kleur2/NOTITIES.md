# Salticonda – kleurronde 2 (3/4, geëvolueerde kop, twee kopvarianten)

Jordi over kleurronde 1 (letterlijk): "teveel zijaanzicht, plus het lijkt qua hoofd niet echt op een evolutie van silicobra, zijn hoofd is bijna hetzelfde als silicobra. Ik weet nu wel dat ik de dikkere versie meer zie zitten iig"
Aanvulling (letterlijk): "ja en misschien nog het design iets aanpassen zodat de staart duidelijk én een staart is maar ook een zoutkegel. Lijkt nu al prima hoor, maar kan nog net iets beter denk ik"

## Bestanden
- `salticonda_A.png` (kop A, **koepel**) en `salticonda_B.png` (kop B, **kroon van zoutplaten**), met `_raster.txt` (één teken per paletindex, zoals kleur1).
- `bron/kop_A.txt`, `bron/kop_B.txt`, `bron/staart.txt`: de handgetekende rasters van kop, hals, halsband en staart.
- `vel.png`: pre-evolutie, kleur1-E, A en B op 4× en 1×, op licht en donker, naast Ekans, Sandaconda en Hippowdon; onderaan de staart op 8×.
- Scripts (`../scripts/`):
  - `onderlaag2.py`: onderlaag van het lijf;
  - `kop3d.py`: onderlaag voor de kopstand, alleen gebruikt om het oog en de mondlijn te plaatsen;
  - `kleur2.py`: bouwt A en B;
  - `check_kleur2.py`: controle;
  - `vel_kleur2.py`: maakt het vel.

## Studie: hoe Game Freak een opgerolde slang in 3/4 zet
- **Ekans:**
  - de windingen zijn ellipsen, iets van boven gezien;
  - de banden tussen de windingen buigen in het midden naar beneden en lopen aan de zijkanten omhoog weg;
  - de kop staat boven op de stapel, met de snuit naar links;
  - het bovenvlak van de kop is zichtbaar en er staat maar één oog in beeld;
  - de staart komt achter de stapel omhoog.
- **Sandaconda:** een bleke snuit met een neusbult en het neusgat bovenop. De zware kop rust laag op het lijf.
- **Steelix** (studie voor een brede, platte kop in 3/4):
  - de snuit wijst naar linksonder, naar de kijker;
  - het bovenvlak van de kop loopt schuin weg;
  - het oog staat hoog aan de nabije kant, onder een zware wenkbrauw;
  - de kaak is breed.
- **Hippowdon/Torkoal:** zware massa, met de schaduw als brede band rechtsonder en een platte grondlijn.

## Wat ik deed
**Lijf (3/4, van iets boven):**
- Drie dikke windingen als ellipsen. De onderlaag is een 3D-stapel van drie ringen, met dezelfde camera voor alles: iets van boven, licht van linksboven. Daardoor kloppen de ellipsen en is het bovenvlak van elke winding zichtbaar.
- De onderste winding zakt uit onder zijn gewicht. Dat geeft een **brede, platte voet**, zoals Jordi bij E wilde.
- Massa als E: 63×59, 2420–2429 px.

**Pekelringen:**
- Ze liggen in de gleuven, op het bovenvlak van de lagere winding, direct onder de hogere.
- Ze volgen de ellips: in het midden laag, aan de zijkanten omhoog, en ze lopen rond de flank weg. Het zijn geen rechte strepen meer.
- Opbouw van boven naar onder: licht (r, met q links), midden (s), donker (t). De onderrand van de winding erboven is slagschaduw (d).

**Zoutkorst:** vier Y-naden op de voorvlakken (drie takken vanuit één punt, trapsgewijs), in een middentint, nooit zwart.

**Kop (handgetekend, dezelfde in A en B op de kuif na):**
- **Groter en zwaarder:** de kop is ±34 px breed tegen 27 bij Silicobra. Het is een brede, platte anacondakop met een stevige kaak. De snuit is twee kolommen ingekort, zodat hij korter en zwaarder oogt en meer naar de kijker staat.
- **3/4:**
  - het bovenvlak van de snuit loopt schuin naar linksonder;
  - de wenkbrauwbult aan de verre kant steekt net boven de omtrek uit;
  - er staat één oog in beeld, aan de nabije kant.
  - De gezichtslijn (h, overgenomen van de pre-evo) daalt in stapjes van het oog naar de neus.
  - De mondlijn loopt in één doorlopende curve van de snuitpunt omhoog naar de kaakhoek. De segmenten zijn 8–9–8 px en sluiten diagonaal op elkaar aan; vooraan buigt hij om de snuitpunt.
- **Sandaconda als idee:** een lichte snuit met een neusbult en één neusgat vooraan. Een tweede neusgat las als een tweede oog en heb ik weggehaald.
- **Oog:**
  - hoog op de kop, onder een zware wenkbrauwschub: een lichte richel met een eigen bovenlijn, met daaronder het donkere bovenlid;
  - het lome halve oog blijft, maar smaller en zwaarder dan bij Silicobra: alleen twee rijen turquoise iris met de pupil en één glanspixel;
  - geen rond oog met een ring meer.
- **Anacondastreep:** van het oog naar achteren (e), met een oker onderrand (g). De achterkop erboven is lichter gemaakt, zodat de streep leest.
- **Halsband:** de turquoise pekelband van de pre-evolutie, nu rond de dikke hals. Hij loopt onder de kin door en ligt op de bovenste winding; de onderrand buigt mee met de ellips.

**Kuif, uitgegroeid (de twee varianten):**
- **A – koepel:** de kuif van Silicobra, maar groot. Het is één zoutkoepel met naden over het achterhoofd en hij vormt de top van de kegel. Dit is het meest herkenbaar dezelfde kuif.
- **B – kroon:** drie zoutplaten die schuin naar achteren oplopen en elkaar overlappen (de voorste over de achterste), met de hoogste in het midden. Hij maakt de kegeltop puntiger en leest meer als volwassen kroon.

**Staart (Jordi's aanvulling):** ik las het net als Claude, dus geen extra variant.
- De staart komt achter de onderste winding vandaan, ligt kort op de grond en buigt dan omhoog.
- Hij loopt taps toe als een **klein zoutkegeltje**: van 9 px aan de voet naar 2 px aan de punt, in zouttinten met licht links en schaduw rechts.
- Er zitten drie pekelringen in die net als op het lijf in het midden doorbuigen. Zo is hij een miniatuur van de grote kegel.
- Op de punt zit een kleine turquoise accupool.
- Hij zit vast aan het lijf (de winding ligt ervoor, met een donkere lijn) en leest daardoor als staart.
- Vergeleken met E is hij rechtop gezet en kegelvormig geworden. Uitsnede op 8× onderaan het vel.

## Palet
Precies dat van kleur1, de Silicobra-Uyuni uit `af/`. Er zijn 14 kleuren in gebruik, met een gekleurde buitenlijn (h aan de lichtkant, K, en O alleen rechtsonder en aan de grond). Geen ijsblauw en niets van Nacli.

## Controle (`python3 scripts/check_kleur2.py`, `scripts/check2.py`)
- Beide: P-modus, transparency = 0, index 0 transparant, 14 kleuren.
- **Open randen: 0. Gaatjes: 0. Losse silhouetpixels: 0.**
- Losse pixels (8 buren): 33 bij A en 36 bij B. Allemaal bewust:
  - het oog: glans, pupil en lid;
  - de uiteinden van de pekelringen waar ze om de flank lopen;
  - de eindpunten van de Y-naden;
  - de turquoise staartpunt;
  - de diagonale stappen van de omlijning.
- Toonruis op het lijf is met een meerderheidspass weggehaald.
- Rechte randen ≥ 5 px:
  - **bovenkant:** geen meer; de koepeltop van A is afgerond;
  - **onderkant:** alleen de grondlijn (13 px onder de voet, 12 px onder de staart, plus twee korte stukjes). Dat is bewust: zoals bij Hippowdon en Torkoal ligt een zware massa plat op de grond.

## Checklist SPRITE_NORM
1. **Leest op 1× als Pokémon:** ok. Naast Ekans, Sandaconda en Hippowdon leest hij als een zware, opgerolde slang op een zoutkegel, met de kop als top (vel, 1×-rij, licht en donker).
2. **3/4 naar links-voor, de kop meer gedraaid dan het lijf:** ok.
   - Het lijf is een stapel ellipsen, iets van boven gezien, met de bovenvlakken zichtbaar. Er zijn geen zijaanzicht-strepen meer.
   - De kop wijst met de snuit naar linksonder, met het bovenvlak van de snuit, de verre wenkbrauw en één oog in beeld.
   - Snuitdier: één oog, het neusgat vooraan.
3. **Ledematen:** geen. De staart telt: hij zit vast aan het lijf, komt onder of achter de onderste winding vandaan en loopt taps toe.
4. **Geen Escher:** ok.
   - Elke winding ligt op de volgende en de lagere is wijder.
   - De kop ligt over de bovenste winding en de halsband ligt ertussen.
   - De staart ligt achter de onderste winding.
5. **Lijf over een echt skelet:** Ekans (opbouw van stapel, kop en staart). Massa en verhoudingen van E, met geleidelijke curven. De rechte stukken zitten alleen aan de grond.
6. **Kop:**
   - Eindvorm, bewust groot en zwaar, want het moet zichtbaar een evolutie zijn. Hij beslaat ±40% van de hoogte inclusief de kuif.
   - De schedel is niet te lang: de snuit is juist ingekort.
7. **Ogen geïntegreerd:** ok. Donker bovenlid onder een lichte wenkbrauwrichel, iris donker boven (t) en licht onder (q/r), een pupil en een glanspixel. Geen bril, geen zwevende wenkbrauw: de richel zit direct op het lid.
8. **Kenmerken op 1× leesbaar:** ok. Kuif (koepel of kroon), oog, halsband, de drie pekelringen, de staartkegel met turquoise punt.
9. **Omlijning:**
   - per kleurgroep: zout h/K/O, pekel s/t;
   - zwart alleen rechtsonder en aan de grond;
   - licht van linksboven;
   - geen open randen (script).
10. **Geen Chernobyl:**
    - het gezicht is niet misvormd;
    - het warme oker (f/g) staat alleen op gezicht en kaak, zoals bij de pre-evolutie;
    - er zijn geen losse delen.

## Eerlijk oordeel
- **Beter dan kleur1 op beide punten van Jordi:**
  - de stapel staat nu duidelijk in 3/4, van iets boven, met ellipsringen in plaats van strepen;
  - de kop is groot, plat en zwaar, met kaak, neusbult, zware wenkbrauw en een uitgegroeide kuif. Hij is niet meer de Silicobra-kop op een groot lijf.
- Het blijft herkenbaar dezelfde lijn door het palet, het halve oog met turquoise iris, de halsband en de kuif.
- **A (koepel):** rustiger en het dichtst bij Silicobra (dezelfde kuif, maar groot). Het geheel leest als één zoutkegel met de koepel als top.
- **B (kroon):** imposanter en "ouder"; de kroon maakt de kegeltop puntiger. Mijn lichte voorkeur, omdat hij het meest als volwassen evolutie leest zonder de kuif te verliezen.
- **De kop staat 3/4 op het niveau van Ekans en Seviper** (snuit naar links-voor, bovenvlak zichtbaar, één oog), niet frontaal zoals Steelix. Dat is bewust: een slangenkop die nog verder naar de kijker draait, verliest zijn snuit.
- **Keuzes voor Jordi** (smaak, geen fouten):
  - koepel (A) of kroon (B);
  - staartpunt turquoise (nu) of helemaal zout.

## Lessen
- Een 3D-onderlaag (een stapel ringen, iets van boven gezien, met één vaste camera) geeft in één keer kloppende ellipsen en ringen die in het midden doorbuigen. Rechte strepen op een opgerolde slang lezen als zijaanzicht.
- Een mondlijn of gezichtslijn in stapjes moet diagonaal doorlopen. Een gat van 1–2 px tussen twee segmenten maakt er losse streepjes van (las als dubbele mond).
- Rechtopstaande kuifplaten met diepe gleuven ertussen lezen als knokkels of een vuist. Overlappende platen die schuin naar achteren aflopen, lezen als kroon.
- Twee neusgaten naast een oog lezen op 1× als een tweede oog. Bij een slangenkop in 3/4: één neusgat, vooraan op de neusbult.
- Een te lange snuit oogt als profiel en als eendenbek. Twee kolommen eruit (foreshortening) draaide de kop zichtbaar naar de kijker en maakte hem zwaarder.
- Een zware eindvorm krijgt een brede voet door de onderste winding onder zijn gewicht te laten uitzakken (breder en platter onder de evenaar). Dat leest meteen als "bulky wall".
- Een losse staart die naast het lijf rechtop staat, leest als paal of kaars. Laat hem achter de winding vandaan komen, kort over de grond lopen en dan pas omhoog buigen.
