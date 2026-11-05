# Evolutiekeuring: olinguito (fase 1) → Coathief (fase 2, kleur ronde 3)

Vraag van Jordi (25 okt): "we moeten kijken of de sprite sterker lijkt dan de olinguito, of het logisch is dat die in coathief evolved".

Gekeurd: `../../../olinguito_v2/af/olinguito.png` (goedgekeurd) en `coathief.png` (ronde 3). De lichtere klauwen van ronde 3b zijn niet meegekeurd. Het vel staat in `evolutie_vel.png`: bovenaan het paar op 4×, 2× en 1×, op licht en donker, en daaronder 12 echte paren, elk op 2× en 1× met hun oppervlak.

## Eindoordeel: TWIJFEL

Als stap is het logisch. De kopverhouding, het verschil in silhouet en de tint van het palet bewegen zoals bij echte evoluties. Coathief oogt **ouder, maar niet sterker**:
- het oppervlak groeit maar ×1,10, waar echte paren een mediaan van ×1,64 hebben;
- de klauwen, het kenmerk van de lijn, worden kleiner;
- de uitdrukking is neutraal en niet confronterend.

Zonder het silhouet te wijzigen kun je de uitdrukking en de klauwen grotendeels repareren. Het formaat niet.

## Metingen

Hoe er gemeten is:
- Het oppervlak is het aantal niet-transparante pixels in de eerste 64 rijen.
- De kop is met de hand als rechthoek afgebakend. Oren en kam tellen mee; vlammen, kraag en manen niet. De kopcijfers zijn daarom een benadering van ±5 procentpunt.
- Kop/lijf is kop-px gedeeld door de rest-px. De staart telt mee bij de rest.
- Soliditeit is px gedeeld door de oppervlakte van de box.
- IoU is de overlap van de twee silhouetten, als ze over elkaar worden gelegd.

| fase 1 → fase 2 | px 1 | px 2 | ×opp | box 1 | box 2 | kop/hoogte | kop/opp | kop/lijf | soliditeit | IoU |
|---|---|---|---|---|---|---|---|---|---|---|
| **olinguito → Coathief** | **1174** | **1297** | **1,10** | 52×56 | 56×62 | 50% → 31% | 43% → 26% | 0,74 → 0,35 | 0,40 → 0,37 | 0,41 |
| zigzagoon → linoone | 1127 | 1089 | 0,97 | 50×35 | 64×29 | 71% → 86%* | 36% → 28% | 0,55 → 0,39 | 0,64 → 0,59 | 0,60 |
| poochyena → mightyena | 989 | 1647 | 1,67 | 44×40 | 62×58 | 62% → 50% | 33% → 26% | 0,50 → 0,36 | 0,56 → 0,46 | 0,51 |
| sentret → furret | 982 | 1416 | 1,44 | 31×61 | 42×54 | 56% → 46% | 59% → 30% | 1,42 → 0,43 | 0,52 → 0,62 | 0,46 |
| houndour → houndoom | 950 | 1635 | 1,72 | 36×45 | 62×64 | 44% → 45% | 20% → 27% | 0,24 → 0,38 | 0,59 → 0,41 | 0,28 |
| cyndaquil → quilava | 903 | 1144 | 1,27 | 42×37 | 57×44 | 62% → 39% | 41% → 19% | 0,71 → 0,24 | 0,58 → 0,46 | 0,43 |
| torchic → combusken | 602 | 1136 | 1,89 | 25×43 | 45×58 | 65% → 41% | 70% → 25% | 2,38 → 0,33 | 0,56 → 0,44 | 0,38 |
| mudkip → marshtomp | 770 | 1120 | 1,45 | 37×39 | 44×50 | 85% → 54% | 72% → 43% | 2,62 → 0,77 | 0,53 → 0,51 | 0,48 |
| treecko → grovyle | 846 | 1368 | 1,62 | 41×45 | 56×53 | 47% → 38% | 32% → 19% | 0,46 → 0,23 | 0,46 → 0,46 | 0,42 |
| growlithe → arcanine (steen) | 1154 | 2622 | 2,27 | 45×46 | 64×61 | 61% → 39% | 46% → 18% | 0,86 → 0,21 | 0,56 → 0,67 | 0,39 |
| purrloin → liepard | 759 | 1402 | 1,85 | 39×44 | 64×57 | 57% → 37% | 61% → 25% | 1,57 → 0,34 | 0,44 → 0,38 | 0,21 |
| teddiursa → ursaring | 756 | 2258 | 2,99 | 31×39 | 59×64 | 64% → 31% | 69% → 18% | 2,18 → 0,22 | 0,63 → 0,60 | 0,32 |
| skitty → delcatty (steen) | 880 | 1300 | 1,48 | 46×40 | 51×55 | 72% → 53% | 62% → 49% | 1,62 → 0,98 | 0,48 → 0,46 | 0,45 |

\* Linoone is een lang, plat dier: de kop beslaat bijna de hele hoogte.

**Echte paren, kort:**
- Oppervlak: mediaan ×1,64 (van ×0,97 tot ×2,99). Alleen Zigzagoon → Linoone groeit niet, maar Zigzagoon is als fase 1 uitzonderlijk groot en pluizig, en Linoone vult wel de volle 64 px in de breedte.
- Kophoogte in fase 2 is mediaan ×0,69 die van fase 1.
- De kop krimpt in absolute px vaak (mediaan ×0,83). De rest groeit mediaan ×2,2.

**Olinguito → Coathief:**
- Oppervlak ×1,10. Van de 12 paren groeit alleen Linoone minder.
- Kophoogte ×0,61 en kop/lijf van 0,74 naar 0,35. Die passen allebei bij de echte paren.
- Kop-px ×0,67 (499 → 335). Dat is normaal: Torchic en Cyndaquil zitten even laag.
- De rest groeit maar ×1,43 (675 → 962), tegen een mediaan van ×2,2. De staart neemt daarvan 258 px (20% van de sprite). Zonder kop en staart groeit de romp met poten van 499 naar 704 px (×1,41).
- Box 52×56 → 56×62. De box is daarmee al bijna vol: de extra grootte moet uit massa komen, niet uit een grotere box.
- De oorzaak ligt ook bij fase 1. De olinguito is met 1174 px groot voor een fase 1: tabel D1 vraagt 700–950 px, en alleen Growlithe en Zigzagoon zitten in dezelfde orde. Coathief valt met 1297 px binnen D1 voor fase 2 (1100–1550), maar haalt D5 niet (fase 2 ≈ 1,5–1,7× fase 1, dus ±1760–2000).
- Poten: rijbreedtes van 5–7 px per poot, net als bij Liepard en Houndoom. De poten zijn dus niet te dun.
- De klauwen van de opgetilde poot zijn kleiner dan bij de olinguito:
  - lichte klauwpixels: 28 bij de olinguito, 16 bij Coathief;
  - lengte: bij de olinguito ±10 px, twee dikke witte klauwen aan elkaar; bij Coathief ±5–6 px, dunne tan haken.
- Oog: bij beide een rode iris van ±2×2 met een zwart bovenlid.
  - Bij de olinguito omlijst de zwarte band het oog.
  - Bij Coathief valt het oog weg in de zwarte kop, en de twee crème vlekken erboven en eronder zijn op 1× helderder dan het oog.
- Palet:
  - Lijf: olinguito `6a4630` / `4c3121` / `8a603e`, Coathief `8e5226` / `5e3216` / `b87636`. Dezelfde bruine tint, verzadigder en warmer.
  - Kop: olinguito `6b5442` / `54443c`, Coathief `40352f` / `2a201c`. Dezelfde grijsbruine tint, donkerder.
  - Weg: het roze (neus, voeten) en het lichte oor.

## Oordeel per punt

| # | Punt | Oordeel | Reden |
|---|---|---|---|
| a | Sterker/ouder | **FAIL** | Ouder: ja. De kop gaat van 50% naar 31% van de hoogte en het lijf is langer, met donkere volwassen poten. Sterker: nee. Op 1× in het vel is Coathief nauwelijks groter (×1,10 tegen een mediaan van ×1,64), de lange dunne staart en poten geven weinig massa (soliditeit 0,37), het USP wordt kleiner (de klauwen) en het oog verdwijnt. Door de lage kop en het neutrale oog oogt hij eerder sluipend dan confronterend, terwijl de SPEC om confrontatie vraagt. |
| b | Dezelfde lijn | **FAIL** (twijfel) | Wat doorloopt: kop links en staart rechtsboven met een haak, één opgetilde voorpoot met lichte klauwen, het roodbruine oog, de lange snuit, de tint van lijf en kop (zie palet) en het donker rond het oog (masker → bivakmuts). Wat breekt: de klauwen worden kleiner en donkerder terwijl ze per fase zouden moeten groeien, het oog is minder zichtbaar, en het roze en het oor verdwijnen. Een buitenstaander ziet "twee wasbeerachtigen", maar herkent de lijn vooral aan de pose en niet aan een duidelijk doorlopend kenmerk. |
| c | Logische stap | **PASS** | Het voelt als opgroeien, ondanks het kleine formaat (zie a): van kind (grote kop, schattig-sinister) naar puber of bandiet (kleine kop, lang lijf). Het is geen "dier met een hoed": geen voorwerpen, en de bivakmuts is een vachtpatroon. Er is ruimte voor fase 3. Het masker kan een verhaal vertellen: band (kind) → volle bivakmuts (crimineel) → het smalle natuurlijke masker van de wasbeer als Robin Hood-masker (nobel). Fase 3 moet dan wel overeind of bekleed en veel massiever worden. |
| d | Silhouet | **PASS** | IoU 0,41, terwijl de echte paren mediaan 0,42 hebben (0,21–0,60): het silhouet verschilt normaal veel. Olinguito: ronde grote kop, rug in een boog, staart die over de rug naar voren krult. Coathief: lange lage snuit, horizontale romp, staart recht omhoog met een haak bovenaan. De opbouw blijft familie: kop links, staart rechtsboven, klauw vooraan. |

## Voorstellen

### Zonder silhouetwijziging (kleur, uitdrukking, oog)
1. **Oog wint van de vlekken.** Zet de bovenste crème vlek een tint terug, naar de middentoon, zodat het oog met zijn glans op 1× het helderste en roodste punt van de kop is. Eventueel 1 px extra rode iris binnen het zwart.
2. **Frons.** Teken een donkere wenkbrauwlijn (2–3 px) boven het oog, schuin omlaag naar de snuit. Het bovenlid wordt dan een boze blik. Dat geeft confrontatie zonder dat de kop beweegt.
3. **Klauwen in olinguito-crème** (sluit aan op 3b): gebruik dezelfde lichte klauwkleur als de olinguito (bijna wit, niet tan) en geef ook de staande voeten een lichte klauwpunt binnen het silhouet. Dan loopt het USP zichtbaar door.
4. **Massa met schaduw.** Maak een sterkere lichtvlek op schouder en heup en een donkerdere buikrand. Het lijf leest dan zwaarder en gespierder bij hetzelfde aantal pixels.
5. **(Optioneel) een familiebrug in kleur.** Geef het oor 1–2 px lichte binnenkant, zoals het oor van de olinguito, of laat de mondhoek in het oudroze van de olinguito. Een klein detail, maar een buitenstaander koppelt de twee zo sneller.

### Met silhouetwijziging (vragen aan Jordi)
- **A. Meer massa (belangrijkste).** Wil je Coathief naar ±1500–1650 px brengen (×1,3–1,4 van de olinguito)? De box zit al op 56×62, dus de extra px moeten van binnenuit komen:
  - de rug 3–4 px hoger, zodat de romp dikker wordt;
  - de staart iets lager laten beginnen, met de top op ±y 6 in plaats van y 1, om ruimte te maken.
- **B. Langere klauwen** aan de opgetilde poot: ±2–4 px langer, minstens zo lang als bij de olinguito (±10 px). Het USP moet per fase groeien en niet krimpen.
- **C. Dikkere voorpoten of schouder:** +1 px per voorpoot en een schouderbult. Dat is ±+80–120 px en oogt sterker.
- **D. Alternatief buiten Coathief.** De olinguito verkleinen naar de fase-1-norm (±900–950 px) geeft een sprong van ×1,37–1,44 zonder Coathief te raken. De olinguito is goedgekeurd, dus dit alleen als je dat wilt.

Gevolg voor fase 3: met de olinguito op 1174 px wordt de norm van D5 (fase 3 = 2,3–2,6× fase 1) 2700–3050 px. Dat is groter dan Arcanine en past amper in 64×64. Reken fase 3 dus vanaf Coathief: 2300–2600 px (D1). Dat is ×1,4–1,6 als Coathief naar ±1600 gaat, en ×1,8–2,0 bij de huidige 1297.
