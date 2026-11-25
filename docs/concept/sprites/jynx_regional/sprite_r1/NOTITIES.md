# Regionale Jynx (sirene, Fairy/Dark) frontsprite, ronde 1 (kandidaat)

Model: `gemini/r5.png` (Jordi: "ok vertaalt dit naar een sprite?"). Methode: Dundragoon (`dundragoon/sprite_r1/NOTITIES.md`), model overnemen, niet hertekenen.

Bestanden: `jynx_regional_r1.png` (64×64, mode P, index 0 transparant, 16 kleuren incl. transparant), `kaal.png` (kale reductie), `vel.png` (r1 8× | kaal 8× | model op dezelfde schaal 8× / close-ups 12× gezicht, vleugel rechts, vleugel links, klauwen naast het model / 1× op wit, crème, donker, zwart + model 1×), `bouw.py`.
Gereedschap (`../gereedschap/`, gekopieerd van Dundragoon en aangepast): `pitch.py`, `natief.py` (→ `natief.png`), `klassen.py` (klasse per modelpixel), `gemeen.py` (schaal, palet, overlap), `vel.py`, `raster.py` (spriteraster over het model), `controle.py`, `zones.py` (afwijkingen per zone), nieuw: `dekking.py` (modeldekking per klasse per spritepixel, voor de reparaties).
Bouwen: `cd docs/concept/sprites/jynx_regional && python3 sprite_r1/bouw.py` (`kaal` als argument toont alleen de kale reductie).

## Metingen
- **Rasterpitch:** één duidelijke kam op **10,24 px** (1024/100) in x en y, fase x 9,25 / y 9,20 (zelfde raster als Dundragoon). Natief raster 99×99, figuur **x15–86, y11–87 (72×77), 3563 px**.
- **Klassen** (`klassen.py`): achtergrond = wit dat vanaf de beeldrand bereikbaar is (het gezicht is even wit als de achtergrond); zwart L < 45; gezicht wit/lichtgrijs; lippen purperrood (B > G); mondbinnenkant roze; haar of veren per samenhangend vlak tussen de zwarte lijnen, op meerderheid G/R ≥ 0,6 (haar is geler/grijzer bruin: 0,60–0,71; veren 0,44–0,57); vlakjes ≤ 6 px binnen het gezicht = iris; grijsbruin onder in de voeten = klauwen. Twee correcties: wit tussen voeten en rok (gat in het model) = achtergrond, één los roze pixeltje in het haar = haar.
- **Tinten per groep** (histogram van de modelhelderheid): veren lijn < 95, schaduw 95–125, midden 125–152, licht ≥ 152 (het model heeft licht op de vleugels en rokzijkanten, midden in het rokmidden, schaduw rechts); haar donker < 80, schaduw 80–105, midden ≥ 105; gezicht schaduw < 235; lippen donker < 70.

## Maat
- **Schaal 58/77 = 0,753** (1,33 natieve px per spritepixel). Figuur **x5–58, y5–62 (54×58), 2130 px**. Niet gespiegeld (model kijkt al naar links), verhoudingen ongewijzigd, onderkant op rij 62, horizontaal gecentreerd.
- Keuze: Gen 3-Jynx is 56×54 / 1978 px. Bij 1978 px zou de schaal 0,745 zijn; ik nam 58 rijen hoog (+8 % px), omdat het model hoger dan breed is (gespreide vleugels i.p.v. Jynx' brede haar) en het gezicht dan 16 px breed blijft. Kleiner kan op verzoek met één getal in `gemeen.py`.

## Wat uit het model komt (kale reductie, `kaal.png`)
Oppervlakteweging per spritepixel over het natieve raster: achtergrond als < ½ pixel figuur; **zwart wint** vanaf 30 %; daarna **iris, roze, lippen, klauwen** vanaf 30 % (kleine modeldelen); daarna de **veerlijn** (veren L < 95) vanaf 30 % als de veren de grootste groep zijn; anders de groep met het grootste oppervlak, tint naar de gemiddelde modelhelderheid (veren zonder de lijnpixels).
Silhouet, haar met scheiding bovenop en lokken, gezicht met inham, beide ogen (wimper + iris), lippen met mondopening en tong, beide vleugels met veerscheidingen, halskraag, rok met alle vouwlijnen, schaduwkant rechts, beide voeten met klauwen: allemaal uit deze reductie.

## Pixels die afwijken van de kale reductie: 391 px (silhouet-diff 0)
Per zone (`zones.py`): **haar 156, vleugels 60, gezicht 76, lijf+rok 63, poten+klauwen 36.** Per stap:
- **binnenlijnen (246 px):** zwart dat niet aan de achtergrond grenst wordt de donkerste eigen tint (Gen 3: binnenlijnen niet zwart): tussen veren → veerlijn, in/naast het haar → haar donker, **gezichtscontour → haar donker** (rondom gelijk). Zwart binnen het gezicht (wimpers, ooghoek, mondopening) blijft zwart; de oogvakken (x19–21 en x25–30, y15–17) zijn daarvoor beschermd. Per zone: haar 95, gezicht 58 (contour), vleugels 37, rok/lijf 50, poten 34 (allemaal K>lijntint).
- **buitenlijn (69 px):** lichtkant (rand die naar linksboven wijst, normaal uit de afgevlakte silhouetrand, drempel 0,30) = gekleurde selout (veren → veerlijn, haar → haar donker); schaduwkant = zwart. Ook zwart uit het model wordt aan de lichtkant selout. Klauwpunten blijven klauwgrijs. Gecontroleerd: nergens selout tussen twee zwarte randpixels (geen om-en-om).
- **ontkorrelen (74 px):** tintvlekjes < 3 px (wit < 2) nemen de meest voorkomende buurtint van dezelfde groep aan; lijntinten, lippen, iris en klauwen niet. O.a. haar S>H 31 / S>D 24, gezicht g>W 14, vleugels/rok m↔+/s 26.
- **gezicht naar het model (5 px), gemeten met `dekking.py`:**
  - kin (23–26,27) → gezichtsschaduw: model W 50–60 % / K 40 % (witte punt die doorloopt, contour eronder op (24–25,28)); de reductie gaf een dubbele contour;
  - (22,10) → wit: model W 49 % > K 42 % (ronde bovenkant gezicht, contour (22,9) blijft);
  - (21,18) → lipdonker: het model heeft twee bultjes in de bovenlip (natief x37 en x39); de reductie hield er één ((23,18)). Nu bultje–wit–bultje;
  - (28,27) → haar donker: de kincontour (27,27)→(29,26) had een veerlijnpixel ertussen (model K 21 %).
- Geen andere pixels die niet uit het model komen. Geen schaduw, banden of glans toegevoegd.

## Palet (index: kleur)
0 transparant (152,208,160) · 1 zwart (24,16,16) · veren 2 lijn/selout (120,48,24) 3 schaduw (176,84,40) 4 midden (216,118,62) 5 licht (240,152,96) · haar 6 donker/lijn/selout (84,50,28) 7 schaduw (124,80,46) 8 midden (164,114,72) · gezicht 9 schaduw (208,200,196) 10 wit (248,248,244) · lippen 11 donker (96,28,48) 12 midden (144,54,74) 13 tong roze (216,138,138) · 14 iris (160,64,60) · 15 klauwen (100,80,64).
Gemeten modeltonen: veren 134,68,33 / 174,86,40 / 221,122,65 / 228,134,77; haar 93,56,33 / 123,79,48 / 160,111,71; gezicht 224,217,206 / 254,254,253; lippen 100,32,50 / 140,54,72; tong 205,141,134; iris 133,65,54; klauwen 96,74,56.
**Kleurafwijking richting Gen 3:** het model heeft veren-midden en -licht maar 12 helderheid uit elkaar; in de sprite 28 (licht iets lichter, midden iets donkerder), zodat de verdeling uit het model (licht op vleugels/rokzijkanten, midden in het rokmidden) als volume leest. Lijntinten iets dieper voor contrast. Stappen veren 168/140/108/68, haar 123/89/58.

## Controle (`controle.py`)
- 64×64, mode P, transparency 0, 16 kleuren incl. transparant; veren 3 tinten + lijn, haar 2 tinten + donker, gezicht 2, lippen 2 + roze, iris 1, klauwen 1.
- Geen lichte kleur op de buitenrand; zwart 7,4 % van de figuur (alleen schaduwkant + gezichtsdetails).
- Eén "losse zwarte pixel": (25,16) = binnenhoek van het rechteroog, staat zo in het model (natief (42,26)).
- Tintvlekjes < 3 px die over zijn: veerlijn 19× = stukjes van modellijnen (veerscheidingen, halskraag, vouwen) die op 0,75× breken; haar donker 6×, iris 2, lippen 5, tong 1, klauwen 6: kleine modeldelen.

## Resterende twijfels (eerlijk)
- **Haar is vlak** (één middentint met donkere lokken, schaduw alleen op het achterhaar rechts): zo staat het in het model. Gen 3-Jynx heeft hooglichten in het haar; er is in het model geen helderheidsverschil om die op te zetten, dus niet gedaan (zou eigen schaduw zijn). Keuze voor Jordi/keurder.
- **Gezichtscontour** is haar donker i.p.v. het zwart van het model (Gen 3-regel binnenlijnen). Het gezicht springt daardoor iets minder; zwart terugzetten is één regel in `bouw.py`.
- **Vouwlijnen in de rok** en veerscheidingen zijn op deze schaal 1-px trappetjes met hier en daar een onderbreking (19 losse stukjes); ze staan op de modelplekken, maar onderaan de rok zigzaggen ze wat.
- **Voeten/klauwen**: drie klauwtjes per voet staan op de modelplekken, maar op 8× zijn de voeten druk (veerlijnen tussen de tenen). Op 1× lezen ze als twee klauwvoeten.
- **Lippen** zijn verhoudingsgewijs donkerder dan in het model (1-px donkere rand rond een klein vlak: 18 px donker tegen 12 px midden).
- **Ogen**: uit de reductie, op het model gecontroleerd (wimper + iris rechts, wimper + ooghoek + iris links); niet "wakkerder" gemaakt dan het model.
