# Alpaca-lijn: ontwerpronde 1 (zonder pixels)

Opdracht: drie verschillende ontwerpconcepten voor fase 1 van de Fighting-starter, als modeltekening (vlak, omlijnd, 3/4 naar links, 256×256), met per concept een ruwe silhouetschets van fase 2 en 3. Uitgangspunten uit `KEURING_RONDE5.md`: het type komt uit het lijf en niet uit spullen, er is één kenmerk dat het silhouet bepaalt, babyverhoudingen en verzadigde Pokémon-kleuren. Dit is een ontwerpronde: Jordi kiest een concept, en dat wordt de vaste modeltekening voor het pixelwerk.

Bestanden:
- `concept_A.png`, `concept_B.png`, `concept_C.png`: fase 1 als modeltekening, met fase 2 en 3 als silhouetschets en uitleg.
- `vergelijking.png`: de drie concepten naast de echte Gen 3-sprites van Torchic, Mudkip, Treecko, Mareep en Growlithe, plus Chimchar (DS, er is geen Gen 3-versie). Op 2×, op 1× in kleur, op 1× als silhouet en op 1× op gras. De concepten zijn verkleind tot ±900 px oppervlak (Gen 3-starters gemiddeld ±808 px).
- `scripts/concepten.py` en `scripts/vorm.py`: maken alle vellen opnieuw (`python3 docs/concept/ontwerp/alpaca/scripts/concepten.py`).
- **Ronde 2 (na Jordi's keuze voor A):** `lijn.png` toont fase 1–3 op schaal, met twee varianten van fase 3. Losse vellen met uitleg: `fase2.png`, `fase3_A.png` en `fase3_B.png`. Ze worden gemaakt met `scripts/lijn.py`. Zie de sectie onderaan.

Wat alle drie gemeen hebben: dezelfde alpacakop. Die is kort en rond, met een korte snuit en een lichte 'glimlachlip'. De ogen zijn groot en staan laag. Er zijn twee lange speeroren en een wolkuif op het voorhoofd. De kuif is wat de alpaca herkenbaar maakt, en in fase 3 verhardt hij bij elk concept tot de bombín. Zo groeit het 'kostuum' pas in de eindvorm uit het lijf, zoals bij Incineroar en Decidueye. In fase 1 draagt geen enkel concept iets.

## Concept A: Wolvuist (boksen)
- **Idee:** de wol aan de voorpoten groeit als twee rode bokshandschoenen, met een 'duim' en een polsrand van wol en zonder manchet. De crèmekleurige kuif valt als een hoofdbeschermer over het voorhoofd, en de V-punt tussen de ogen is meteen de frons.
- **Waarom het Pokémon leest:** het is één uitvergroot lichaamsdeel, zoals de handen van Makuhita. De vorm is een babyverhouding: een grote kop op een Mareep-wolbal met korte pootjes. Het blijft op vier poten, en de vuisten maken het silhouet (twee bollen vooraan).
- **Hoe je het type ziet:** vuisten + frons. Rood is de enige accentkleur, en die zit alleen op de vuisten. Kleuren: crème, rood, karamel en donkerbruin.
- **Lijn:** de vuisten groeien mee. In fase 3 verhardt de kuif tot de bombín, hangt de oorwol als vlechten en wordt de heupwol een pollera.
- **Zwakte:** het dichtst bij Jordi's oorspronkelijke grap (handschoenen), dus ook het dichtst bij 'te veel Hitmonchan'. Dat blijft binnen de perken omdat het wol is en hij op vier poten staat.

## Concept B: Nekkraag (nekworstelen)
- **Idee:** lama's en alpaca's vechten in het echt met hun nek: ze duwen en haken, zoals worstelaars. De halswol groeit uit tot een dikke kraag die breder is dan de kop en tot tegen de kaken opbolt. Het oogt als de nek- en schouderspieren van een worstelaar. Daarbij een strenge blik met donkere wenkbrauwvlekjes en een brede, schrap gezette stand.
- **Waarom het Pokémon leest:** het is alleen vacht, zonder enig voorwerp. Het silhouet is zwaar van voren en licht van achteren, met de kop bovenop een wolblok, zoals de bulldog-bouw van Snubbull en Makuhita. Het is een echt diergedrag dat een type wordt. Dat is precies hoe Game Freak werkt.
- **Hoe je het type ziet:** de bouw (bulk voor, geen nek), de wenkbrauwen en de stand. Kleuren: roestrood, crème, chocoladebruin en goud.
- **Lijn:** de kraag groeit in fase 2 in ringen langs de langere hals. In fase 3 wordt hij de **manta** (de omslagdoek van de cholita), met de bombín-kuif en vlechten. Van de drie is dit de meest natuurlijke weg naar de cholita-luchadora.
- **Zwakte:** het type is minder direct af te lezen dan bij A. Zonder de wenkbrauwen kan hij ook 'trots schaap' zijn.

## Concept C: Polleratrap (trappen)
- **Idee:** alpaca's trappen naar achteren als ze boos zijn. De wol rond de heupen groeit in gekleurde ruches (crème, rood, goud): de pollera van de cholita, maar dan als vacht, zoals de blaadjes van Tsareena of de veren van Oricorio. De kracht zit in de achterpoten. Hij staat met één achterpoot uitgetrapt en knipoogt uitdagend.
- **Waarom het Pokémon leest:** de kleur is in lagen opgebouwd, wat een Pokémon-trope is ('kleding uit het eigen lijf'). Het silhouet is asymmetrisch en dynamisch door de trap.
- **Hoe je het type ziet:** de trap-pose en de opvallende achterhand. Kleuren: zandbruin, rood, goud, donkerbruin en crème.
- **Lijn:** elke fase krijgt een laag erbij. Fase 3 trapt met een volle, wapperende pollera en de bombín.
- **Zwakte:** het type zit vooral in de **pose**, en een sprite staat stil. In de neutrale stand is het 'alpaca met een gekleurde rok'. Van de drie loopt deze het meeste risico op 'dier met kostuum'.

## Eigen keuring (criteria uit KEURING_RONDE5.md)
| criterium | A | B | C |
|---|---|---|---|
| nul spullen, type uit het lijf | ja (wolvuisten) | ja (kraag = vacht) | grotendeels (ruches zijn wol, maar lezen als rok) |
| één kenmerk dat het silhouet maakt | sterk (vuisten) | redelijk (bulk voor) | zwak in stand, sterk met trap |
| babyverhoudingen, kop ≥45% | ja | ja | ja |
| alpaca herkenbaar (kuif, speeroren, korte snuit) | ja | ja | ja |
| leesbaar op 1× (`vergelijking.png`) | ja, rood springt eruit | ja, maar minder uniek | matig, de ruches worden een streep |

**Vervangen tijdens deze ronde** (lazen als 'dier met kostuum', dus vervangen zoals de opdracht vraagt):
- een **bolhoed-kuif met rand en een lucha-masker**. Dat leest als hoed + masker, en een masker is bovendien Dark-taal (olinguito).
- een **hoofdband-kuif met lange slierten**. Dat leest als een stoffen hoofdband, of met twee slierten als vleugels of geitenhoorns.
- een **'spierwol'-variant** (schouderbulten). Die las als een rups van witte bollen.

**Wat de 1×-vergelijking laat zien:**
- De drie silhouetten lijken onderling sterk op elkaar: dezelfde kop en oren en vier poten. Het kenmerk moet het verschil maken, en dat lukt bij A het best.
- De concepten zijn lichter dan de echte starters, omdat crème wol een groot deel van het oppervlak inneemt (Mareep heeft hetzelfde probleem en lost het op met een blauwe kop). Bij het pixelen moet de wol een warme gele schaduwramp krijgen, zoals bij Mareep, en geen grijs.

## Mijn voorkeur: A (Wolvuist), met de kraag van B als bouwsteen voor fase 3
A heeft het sterkste silhouet en de duidelijkste type-lezing: op 1× zie je meteen twee rode vuisten aan een alpaca. Het houdt Jordi's oorspronkelijke grap (een knuffeldier met bokshandschoenen) en maakt er anatomie van. De frons van de kuif-hoofdbeschermer is het tweede, kleinere Fighting-signaal en ook het zaadje van de bombín.

B is het meest 'Game Freak' qua bron (echt diergedrag) en geeft de mooiste eindvorm (de manta). Als Jordi voor A kiest, stel ik voor de eindvorm van A de kraag/manta van B mee te geven. Dan krijgt fase 3 bombín (kuif), vlechten (oorwol), manta (halswol), pollera (heupwol) en wolvuisten: een volledige cholita-luchadora die helemaal uit de eigen wol groeit.

C zou ik niet kiezen: het type hangt aan een pose die een stilstaande sprite niet kan dragen.

Volgende stap na Jordi's keuze: de modeltekening vastzetten en pas dan pixelen op een Gen 3-skelet (Mareep voor de wol, Growlithe voor de driekwartstand), met een palet uit `normal_gba.pal` van Mareep en zonder automatische schaduw.

---

# Ontwerpronde 2: fase 2 en fase 3 bij concept A

Keuze van Jordi (23 okt): fase 1 = concept A (Wolvuist). Vanaf fase 2 worden de handschoenen **wolkragen om de poten**. Fase 3 mag rijker 'bekleed' zijn. Alles is getekend met dezelfde tekenaar en stijl als concept A (`scripts/vorm.py`: vlakke kleuren, donkere omlijning, basisvormen, 256×256, 3/4 naar links). Opnieuw maken: `python3 docs/concept/ontwerp/alpaca/scripts/lijn.py`.

**Vaste kleurrollen in de hele lijn:**
- crème = wol;
- karamel = vacht;
- rood = de 'vechtwol' (vuist → kraag → manta/pollera);
- donkerbruin = vilt (bombín) en hoeven;
- goud = zoom (alleen in fase 3).

Er komt nergens een kleur of voorwerp van buiten bij: elk 'kledingstuk' is wol die ergens uit het lijf groeit.

## Fase 2: lama (Wolkraag), `fase2.png`
- **Vorm:** langere poten en hals en een iets langere kop (lama). Het wollijf is slanker dan bij de alpaca. Hij staat nog op vier poten, met de voorste voorpoot iets opgetild in dekking.
- **Kragen:** de vuisten zijn **opengegaan**. De rode wol ligt nu als een dikke kraag om elk onderbeen, als boksbandages van wol, met de hoef eronder. Dezelfde rode wolbolletjes als de vuist, maar nu als ring.
- **Kuif:** de kuif verdicht tot een koepel met grotere, gladdere bollen en een randje. Dat is het zaadje van de bombín. De V-frons blijft, met strakkere wenkbrauwlijnen.

## Fase 3: lama met bombín (cholita-luchadora)
Onderdelen in beide varianten:
- **Bombín** = de kuif is verhard tot vilt. Gevilte wol is letterlijk het materiaal van een bolhoed. Hij staat klein en hoog op de kop, zoals cholita's hem dragen, en de laatste crème wol krult als pony onder de rand uit.
- **Vlechten** = de oorwol, gevlochten. Ze eindigen in rode wolkwasten (de *tullma*'s waarmee cholita's hun vlechten verlengen).
- **Manta** = de halswol, die als omslagdoek over de schouders valt, met een geschulpte wolrand en een rode zigzagband. Die band is een vachttekening die naar een aguayo-weefsel verwijst.
- **Pollera** = de heupwol, in drie ruches: rood, goud en crème.
- **Kragen** = een dikke rode kraag om elke voorpoot, en crème kragen om de achterpoten.

**Variant A (`fase3_A.png`): op vier poten.** Hij blijft een viervoeter, zoals de hele lijn. De bekleding zit op schouders en heupen, dus het blijft een dier met een vacht die als kleding leest.

**Variant B (`fase3_B.png`): rechtop.** Dit is de stap die Incineroar maakt: hij staat op de achterbenen als luchadora. De voorpoten worden armen, met de kragen als polsbanden, en één arm is in dekking geheven. Als vechter is dit sterker, maar hij komt dichter bij 'dier in kostuum'.

**Mijn voorkeur: variant A.**
- Jordi wilde de lijn op vier poten.
- De keuring van ronde 5 waarschuwt voor 'dier in kostuum'.
- Een staande lama met rok en omslagdoek leest snel als verklede knuffel.

In A blijft het één dier waarvan de wol op de juiste plekken 'kleding' is geworden.

**Risico in beide varianten:** de manta en de pollera zijn de grootste 'kledingvormen' van de lijn. Ze blijven Pokémon zolang ze (1) dezelfde geschulpte wolrand hebben als de rest van de vacht, (2) geen zomen, knopen of stoffen plooien krijgen, en (3) in de sprite dezelfde wolshading krijgen als het lijf.
