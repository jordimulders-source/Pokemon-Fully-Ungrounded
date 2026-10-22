# Kritiek ronde 1: starters fase 1 (alpaca, olinguito, nachtaap)

22 okt. Een review van `alpaca/`, `olinguito/` en `nachtaap/` (`anim_front.png`, ronde 1) naast echte Pokémon.
Contactvellen in `kritiek/`:
- `1_starters_gen1-9.png`: fase 1 van alle 27 starters naast onze drie, met onderaan een silhouettest;
- `2_type_zonder_uitleg.png`: Psychic, Fighting en Dark (vooral schattige en kleine soorten), met onze starter achteraan in elke rij;
- `3_zelfde_dier_en_eindvormen.png`: hetzelfde dier met een ander type (Zigzagoon tegenover Galar-Zigzagoon, Wooloo tegenover Mareep) en de eindvormen waar onze lijnen heen gaan.

Typen zijn gecontroleerd in `src/data/pokemon/species_info/`. Let op twee herziene typen: in deze repo is Sableye Rock/Ghost en Noctowl Flying/**Dark**.

## Feedback van Jordi (letterlijk)

> "ze lijken qua spriting totaal niet op Pokémon, en conceptueel ook niet, je ziet er hun type niet aan af, de kleuren zijn generiek, het hele design is generiek. Het zijn gewoon dieren en geen Pokémon."

Het algemene concept van alle drie is "wel ok". Per sprite:
- **Alpaca:** mag nog **fluffier**.
- **Olinguito:** de **pose waardeert hij**, maar hij wil **langere klauwen** en een **wat donkerdere kleur**.
- **Nachtaap:** de **ogen zijn geinig**, maar mogen **nog mysterieuzer**; de **knieën zijn wat groot**; de **krulstaart is geinig**.

Daarnaast vroeg hij om:
- de lat van Oranguru, Abra en Espurr: "als je die ziet, weet je vrijwel zeker dat het Psychic is". Zo duidelijk moet het type van onze starters zijn;
- de alpaca spiegelen aan schattige Fighting-soorten (Stufful/Bewear en anderen). De lijn mag ook verwijzen naar **vechtsporten van buiten Zuid-Amerika**. De eindvorm blijft de cholita-luchadora met bombín;
- de olinguito spiegelen aan schattige of kleine Dark-soorten, vooral de dieven;
- de nachtaap spiegelen aan mysterieuze en nachtelijke Psychics, met de ogen als typesignaal.

---

## De kern: waarom het "gewoon dieren" zijn

Een Pokémon is **dier × idee × type**. Torchic is een kuiken, maar dan als eivormig balletje met een vlamkuif. Litten is een kat, maar dan als worstelaar in de dop, met een vlammend vachtpatroon. Riolu is een jakhals, maar dan als vechter met een masker en vuisten. Onze drie hebben alleen het eerste ingrediënt: ze zijn een goed getekend **dier**. Het idee (de rol) en het type zitten in de tekst van `POKEMON.md`, niet in de sprite.

Wat de vellen laten zien:

1. **De anatomie is realistisch, niet gestileerd.** De alpaca staat als een boerderijdier in zijprofiel op vier pootjes, als tafelpoten. De olinguito heeft het gezicht en de bouw van een echte kleine beer. De nachtaap is letterlijk een tarsier, met kikkerdijen en grote knieën. Echte starters zijn eerst een **vorm** (bal, ei, peer, druppel) en daarna pas een dier. Torchic is een ei met een kuif, Mudkip een peer met een vin, Rowlet een bal met een strik, Wooloo een wolbal met een gezicht en Mareep een wolk met een staartbol.
2. **Er is geen onrealistisch kenmerk.** Elke starter heeft één ding dat in de natuur niet bestaat: de kuif van Torchic, de vin van Mudkip, de schuimsjaal van Froakie, de scalchop van Oshawott, het neusballon van Popplio, het bloemmasker van Sprigatito, de vlam van Fuecoco en de "haarkuif" van Quaxly. Ook gewone dieren hebben er één: de bol aan de staart van Mareep, de cirkel op de buik van Sentret, de ringen van Furret, de hand aan de staart van Aipom, de sjaalstaart van Minccino, de bladmanen van Skiddo, de bloem van Deerling. Bij ons komen de oorkwastjes van de alpaca het dichtst in de buurt, maar die lezen als een schattig strikje (Fairy), niet als iets van een vechter. De bes van de olinguito leest als een snack, niet als buit. De spiraal van de nachtaap is het goede idee, maar is 1 px dun.
3. **De kleuren zijn natuurlijke vachtkleuren.** Ik heb de verzadiging gemeten (`kritiek/sat.py`, zonder omlijning; vellen met `kritiek/grid.py`): fase 1 van de starters zit gemiddeld op **0,54**. De laagste (Scorbunny 0,21, Oshawott 0,30, Rowlet 0,31) zijn witte figuren met **één fel accent in de typekleur** (rode neus en voeten, blauwe/gele scalchop, groen strikje). Onze alpaca zit op 0,39 (crème met roze), de nachtaap op 0,23 (grijsbruin) en de olinguito op 0,66. De olinguito is dus wél verzadigd, maar in de tint van **Normal-knaagdieren** (Sentret, Zigzagoon, Bidoof, Skwovet). Verzadiging alleen is het probleem niet: Espurr (0,22) en Poochyena (0,15) zijn ook kleurarm en toch onmiskenbaar Psychic en Dark. Het gaat om **welke tint** je kiest en **waar je het contrast legt**.
4. **Je ziet het type niet.** Zie de drie typeanalyses hieronder.
5. **De gezichten zijn dierengezichten, geen karaktergezichten.** De alpaca en de olinguito hebben kleine stip-ogen. Starters hebben grote ogen met een grote glans, en een wenkbrauw of ooglid die een houding uitdrukt: Grookey ondeugend, Litten afstandelijk, Pancham dwars, Riolu alert.
6. **De silhouettest faalt.** In het zwart (onderste rij van vel 1) is de alpaca een schaap en de olinguito een eekhoorn of Sentret. De nachtaap is herkenbaar als tarsier, maar niet als iets met een type. Bij Torchic, Mudkip, Chimchar, Litten en Sprigatito breekt juist het element-onderdeel het ovaal: de kuif, de vin, de vlam en de oren.
7. **Spritetechnisch zijn ze geïllustreerd, niet "Pokémon-gespriet".** Procedurele vachtruis, veel kleine klontjes tinten en dithering geven een getextureerde dierenillustratie. GBA- en DS-sprites gebruiken grote **egale kleurvlakken** met een paar duidelijke schaduwvormen. De vorm draagt het beeld, niet de textuur. De wol van de alpaca is "vlekkerig" en daardoor juist níet fluffy. Fluffy lees je aan een **geschulpte buitenrand** (Wooloo, Mareep, Altaria, Swablu), niet aan ruis binnenin.
8. **Fase 1 wijst nauwelijks vooruit.** Bij de starters zit de eindvorm al in fase 1: Litten (de kraagvlam en het patroon van een worstelaar) wordt Incineroar met zijn kampioensriem, Froakie (sjaal van schuim) wordt Greninja (sjaal van tong), Rowlet (strikje) wordt Decidueye (capuchon), Fennekin (oorvlammen) wordt Delphox (toverstok en gewaad) en Sprigatito (bloemmasker) wordt Meowscarada (goocheldief). Bij ons wijst alleen het krulletje van de nachtaap al naar de eindvorm.

### Het trio als geheel
De klassieke starters vormen een kleurendriehoek: groen, rood en blauw. Onze drie zijn alle drie **warmbruin-beige** en vallen naast elkaar weg (zie de onderste rij van vel 1 op 1×). Fighting, Dark en Psychic hebben ook vaste kleurwerelden: warm rood met contrast, donker met een gloeiend accent, en violet/roze/goud. Voorstel voor de driehoek:

| starter | helderheid | hoofdkleuren | accent |
|---|---|---|---|
| alpaca (Fighting) | **licht** | warm wit + cacao | **rood** |
| olinguito (Dark) | **donker, warm** | kastanje + bijna-zwart | **goud** |
| nachtaap (Psychic) | **midden, koel** | lavendelgrijs + zilverwit | **magenta** |

Zo zijn ze naast elkaar in het keuzescherm meteen uit elkaar te houden. Daarnaast deelt elk van de drie **één klein Andes-geweven detail** (een streep in aguayo-stijl, een geometrisch borduursel). Dat is regioherkenning zonder dat het het type overstemt.

---

## 1. Alpaca (Fighting): "een schaap, geen vechter"

### Wat werkt
- De grote kop en de kuif van krullen zijn een goed begin voor de schattigheid. De V-frons is precies het goede idee, maar op 1× te klein.
- De oorkwastjes zijn een echt Andes-detail met een eigen ramp: goed voor de varianten en voor de cholita-lijn.
- Frame 2 met de platte oren en de open bek heeft karakter.

### Wat niet werkt
- **Zijprofiel op vier stompjes** is de pose van een boerderijdier, geen starter. Alle viervoetige starters (Tepig, Litten, Fennekin, Cyndaquil, Sprigatito) staan driekwart naar de speler toe, met de kop naar je gedraaid.
- **Crème en beige met roze** is de Wooloo-kleurwereld (Normal), en het roze trekt naar Fairy. Er is **geen enkel Fighting-signaal** behalve een frons van een paar pixels.
- **Niet fluffy genoeg** (Jordi): de omtrek is bijna een gladde ovaal en de "wol" is binnenin ruis. Wooloo en Mareep halen hun fluffiness uit een grote, regelmatig **geschulpte rand** met 8–12 bollingen.
- De kop is een realistische alpacasnuit; hij moet een **karaktergezicht** worden.

### Hoe schattige Fighting-soorten hun type tonen (vel 2, rij Fighting)
| soort | waarom toch onmiskenbaar Fighting |
|---|---|
| **Stufful / Bewear** | Een knuffelbeer, maar het kleurpatroon is opgedeeld als **kleding**: bij Bewear lijkt de roze kop op een capuchon of masker boven een zwart "pak", en bij Stufful lijkt het wit-roze spiraalpatroon op een doelwit. De **armen zijn omhoog** (zwaaien, knuffel-wurggreep) en de poten zijn groot. Zacht lijf, harde houding. |
| **Pancham** | Panda, maar met een **frons** en een **blad in de mond** (de banchō- of straatschoffie-pose). Een zwart-wit kleurblok als een uniform, en kleine vuistjes. |
| **Riolu** | Een **zwart masker** over de ogen, een blauw-zwart kleurblok en pootjes als vuisten, in een **gevechtshouding**. |
| **Mienfoo** | Lange vacht aan de armen die als **kungfu-mouwen** leest, gekleurde "broek" en een **kraanvogelstand** op één been. |
| **Makuhita** | Een sumoworstelaar zonder kleding: de kop heeft de vorm van een **knotje**, er zit een **mawashi-band** in de tekening en de handen zijn **ronde wanten**. Wijde, gehurkte stand. Superschattig en superduidelijk. |
| **Tyrogue** | Een tekening van **tape of bandage** om de handen, een "broekje", en een frons. |
| **Hawlucha** | Een **luchadormasker** als gezichtstekening, plus een borst-vooruit-pose. Voor onze eindvorm de belangrijkste referentie. |
| **Kubfu** | Een **knotje** als kungfuleerling, een vastberaden frons en een **vuist** naar voren. Schattig hondje, toch vechter. |
| **Clobbopus** | De tentakels eindigen in **ronde bokshandschoenen** in een contrastkleur. Het hele idee in één onderdeel. |
| **Meditite** | Een **meditatiehouding** en een kop als een tulband (Fighting/Psychic). |
| **Mankey** | **Altijd boos**: een frons, gebalde vuisten en een opgeheven arm. |
| **Paldea-Tauros (Combat)** | Zwart, gespierd, kop omlaag om te **chargen**. Het type zit hier in de houding. |
| **Timburr** | Draagt een **balk** (bouwvakker), een dikke arm en een koppige frons. |

**Hieruit volgen de middelen** om een fluffy alpaca Fighting te laten lezen zonder dat hij zijn schattigheid verliest:
1. **Handschoenen of tape uit het eigen lijf** (Clobbopus, Makuhita, Tyrogue): wol die als ronde bokshandschoenen of polsbanden om de voorpoten groeit, in de **accentkleur**.
2. **Tekeningen die op sportkleding lijken** (Bewear, Makuhita, Mienfoo, Hawlucha): een band als gordel of mawashi, een kuif als hoofdband of knot, een gezichtsmasker.
3. **Een wenkbrauw die iets wil** (Pancham, Kubfu, Mankey): dikke wollen wenkbrauwen van 2 px in een V, boven grote glanzende ogen. Grote ogen houden hem schattig, de wenkbrauwen maken hem vastberaden.
4. **Een houding die klaarstaat** (Riolu, Kubfu, Mienfoo): het gewicht naar achteren, een voorpoot opgeheven in de dekking, de kop iets omlaag. Niet staan, maar klaarstaan.
5. **Kleurcontrast als uniform** (Pancham, Riolu, Bewear): grote, duidelijke kleurblokken in licht en donker plus één rood accent, in plaats van zachte ton-sur-ton-tinten.
6. **Rood als typekleur** (de Fighting-kleur is roodbruin, #C22E28): op de handschoenen en kwastjes, niet roze.
7. **Zacht blijft zacht**: de wolwolk, de ronde vormen en de grote kop blijven. Stufful en Makuhita bewijzen dat één of twee duidelijke vechtsignalen genoeg zijn op een zacht lijf.

**Vechtsporten per fase** (Jordi: dat mag ook van buiten Zuid-Amerika): fase 1 **boksen** (wollen handschoenen), fase 2 de lama als **kickbokser of capoeirista** (een lama schopt; wollen scheenwraps zoals bij muay thai, en capoeira is Braziliaans, dus regionaal), fase 3 **lucha libre** als cholita-luchadora met bombín. Zo groeit de lijn van het "kleine bokserballetje" naar "de trappende atleet" en dan naar "de kampioene in de ring", zoals Litten → Torracat → Incineroar.

### Herontwerprichtingen

**A. "Wolbokser" (favoriet)**
- **Silhouet:** een grote **wolwolk** als lijf, met een geschulpte rand van ±10 regelmatige bollingen (Wooloo/Mareep), goed voor ±60% van het silhouet. Hij staat op vier poten maar **driekwart naar voren** (zoals Tepig en Litten), en de korte achterpootjes verdwijnen grotendeels in de wol. Een korte hals en een grote kop met een kuif steken uit de wolk. De **voorpoten zijn dikker** en eindigen in **ronde wollen handschoenen** (5–6 px doorsnee) die naar voren uitsteken. Die breken het ovaal, net als Mudkips vin.
- **Typekenmerk:** de **rode wolhandschoenen** (Clobbopus-logica), met daaronder een smal **goudgeel polsbandje** (een aguayostreep die als tape leest). De oorkwastjes worden rood, in dezelfde ramp als de handschoenen. Eén accentkleur maakt het geheel rustig.
- **Kleuren:** wol warm wit `#FFF8EC` / `#F2DDC8` / `#CDAA98` / selout `#8E6A68`; vacht (gezicht en poten) cacao `#B8714A` / `#8C4A32` / `#5E2C22`; accent rood `#FF7A6E` / `#E8383D` / `#9E1B32`; klein tweede accent goud `#F6C445` (alleen de polsband).
- **Gezicht:** groot en driekwart naar voren, met grote ogen en een stevige glans. **Dikke wollen wenkbrauwen** (2 px, V-vorm) die uit de kuif groeien, wangen een beetje opgeblazen en een klein, vastberaden mondje. Een knuffel die je niet moet uitdagen.
- **Pose:** in frame 1 staat hij in de dekking: het gewicht achterover, één handschoen iets opgeheven, de kop iets omlaag. In frame 2 **steigert** hij op zijn achterpoten met beide handschoenen omhoog (de bokserhouding), of geeft hij een jab met één poot. Dat wijst vooruit naar het rechtop staan van fase 2 en 3.
- **Vooruitwijzing:** de **kuif heeft de vorm van een mini-bolhoedje** (een ronde koepel met een krulrand), het zaadje van de bombín. De handschoenen worden de polswraps van de luchadora en de rode kwastjes haar kleurige linten en pompons.

**B. "Sumo-wolbal"**
- **Silhouet:** een bijna perfecte bol (Makuhita, Wooloo) met een brede, gehurkte stand. Hij zit wat lager en heeft vier dikke stompjes.
- **Typekenmerk:** een **geweven band om het middel** als mawashi of kampioensgordel (rood met één gouden streep), en een kuif als **sumo-knotje**. In frame 2 doet hij de **shiko**: één poot hoog opgetild om te stampen.
- **Kleuren:** wit `#FFF8EC` / `#E9D6C2`; cacao `#8C4A32`; band rood `#D8343A` + goud `#F6C445`.
- **Gezicht:** grote ogen, een strenge frons en wangen bol van inspanning.
- **Vooruitwijzing:** de gordel wordt de riem van de luchadora (Incineroar-lijn). Het risico is dat hij te statisch en te rond wordt; de band moet groot genoeg zijn om op 1× te lezen.

**C. "Gemaskerde kleine luchador"**
- **Silhouet:** als A, maar met de nadruk op de kop.
- **Typekenmerk:** de vacht van het gezicht vormt een **luchadormasker**: een crème "masker" rond de ogen met een rode rand en een vlam- of druppelvorm boven de ogen (Hawlucha). De rest van de wol is donkerder.
- **Kleuren:** wol cacao-rood `#B5654A` / `#7A3A2E`; masker crème `#FFF0D6`; accent rood `#E8383D`, goud `#F6C445`.
- **Vooruitwijzing:** het meest directe naar lucha libre. Het nadeel: de lucha komt al in fase 1, dus fase 3 verrast minder, en de "witte knuffel" gaat verloren.

**Mijn keuze: A.** Het is de fluffiest en de schattigst, het type is meteen leesbaar (rode handschoenen, frons, dekking), en de lijn bouwt op van boksen (fase 1) via trappen (fase 2) naar lucha libre (fase 3). B's gordel kan in fase 2 terugkomen.

---

## 2. Olinguito (Dark): "een Sentret met een bes"

### Wat werkt
- **De pose** (Jordi): de sluipende inbreker met bungelende klauwen en buit op schoot vertelt een verhaal. Die blijft.
- Frame 2 ("hehe", ogen dichtgeknepen, hoektand) is de goede persoonlijkheid.
- De lange staart met de krul geeft hem een eigen silhouet.

### Wat niet werkt
- **Oranjebruin** is de kleur van Sentret, Zigzagoon, Bidoof en Skwovet: Normal-knaagdieren. Zet hem naast Kanto-Zigzagoon en Galar-Zigzagoon (vel 3) en je ziet het probleem én de oplossing.
- **Ronde, onschuldige stip-ogen** en een teddybeersnuit. Het gezicht zegt "lief", niet "dief".
- **De klauwen zijn te kort** (Jordi): 2–3 px, dus op 1× zijn ze bijna weg.
- **De rode bes** leest als eten. Niets in de sprite zegt "gestolen".

### Hoe schattige of kleine Dark-soorten hun type tonen (vel 2, rij Dark)
| soort | waarom toch onmiskenbaar Dark |
|---|---|
| **Purrloin** (dief) | Een paarse vacht, **groene ogen met halfgesloten leden** en een zelfvoldane grijns. Hij zit "onschuldig" netjes, maar het gezicht verraadt hem. |
| **Nickit / Thievul** (dief) | **Roodbruin mag dus wél**, maar dan met **zwarte sokken**, een zwart snorpluimpje dat als een **inbrekerssnor** leest, **sluwe spleetogen** en een lage sluiphouding. Thievul is de gentleman-dief (Lupin). Dit is de belangrijkste referentie voor onze kleur. |
| **Sneasel** (dief) | Zwartgroen, een **rode veer als accent**, **lange witte klauwen** en een scherpe grijns. Een grillig silhouet. |
| **Murkrow** (dief) | Een kuif als **heksenhoed**, zwart-blauw, met geel als accent. |
| **Sableye** (dief; in deze repo Rock/Ghost) | **Edelsteenogen** en een brede grijns. Ogen als buit. |
| **Zorua** | Donkergrijs en zwart met **rode** accenten aan de manenpunt en rond de ogen, en een ondeugende blik. |
| **Impidimp** | **Roze en paars kan ook Dark zijn**, dankzij een kwaadaardige grijns, schuine ogen en duivelsoortjes. |
| **Poochyena** | Grijs en zwart, **gele oogwitten met rode irissen** en ontblote tanden. |
| **Scraggy** | Afgestroopte huid als een **slobberbroek** en een kuif als **capuchon**: een straatschoffie in kleding uit het eigen lijf. |
| **Pawniard / Maschiff** | Zwart-rood met messen, en roest-zwart met **gele "wenkbrauwen"** en een chagrijnige snuit. |
| **Galar-Zigzagoon** | **Hetzelfde dier als Zigzagoon**, maar zwart-wit gestreept, met **rode ogen**, een **tong uit** (spot) en punkstekels. Het bewijs dat palet en gezicht het type maken. |
| **Inkay / Umbreon / Houndour** | Een donkere basis met **gloeiende tekeningen**: de gele ringen van Umbreon en de botachtige banden van Houndour. Rode ogen. |

**Hieruit volgen de middelen** voor de olinguito:
1. **Palet:** een donkere basis. Een warme donkere tint (kastanje of roest) kan, mits **met zwart** (Nickit, Maschiff), anders wordt het Normal. Desatureer de basis en houd het felle voor het accent.
2. **Eén gloeiend accent, op de ogen:** goud, geel of rood. Bij Dark zit het felste van de sprite bijna altijd in de **ogen**.
3. **Ogen:** halfgesloten leden, schuin, een blik opzij. Geen ronde onschuldige stip-ogen.
4. **Mond:** een scheve grijns met één hoektand, of een tong uit (Galar-Zigzagoon).
5. **Tekeningen:** een **masker of vlek over de ogen**, **zwarte sokken of "handschoenen"** (inbrekershandschoenen) en duidelijke staartringen.
6. **Silhouet:** scherpere punten (een plukje op de kop, puntige oortoppen, een getande staartpunt) en lange haakklauwen die uitsteken (Sneasel).
7. **Houding en voorwerp van de dief:** de sluiphouding (die heeft hij al) en buit die als **buit** leest: een munt of iets glimmends (Meowth, Sableye), niet een snack.

### Herontwerprichtingen

**A. "Zakkenroller" (favoriet)**
- **Silhouet:** zijn huidige pose en lijf, met drie wijzigingen. De **klauwen worden 6–8 px lang** (zo lang als de hand), gekromd als haken, drie per poot, en steken duidelijk buiten de omtrek. De staart krijgt een **getande punt**. Op de kop komt een klein **plukje** dat het ronde hoofd breekt.
- **Typekenmerk:** **zwarte "inbrekershandschoenen"**: de voorpoten zijn tot de elleboog zwart, de achterpoten hebben zwarte sokken (Nickit). Daarbij komt een **donkere vlek over de ogen**, een vaag masker dat in de coati een band wordt en in de wasbeer het Robin Hood-masker. De staart krijgt **4–5 duidelijke donkere ringen** (het zaadje van de coatistaart).
- **Kleuren (donkerder, zoals Jordi vroeg):** vacht kastanje `#A65A34` / `#7A3E2A` / `#4E2621` / selout `#2A1720`; donker (masker, handschoenen, ringen) `#46384A` / `#2B2232`; snuit en buik gedempt crème `#E2C79A` / `#B2906A`; accent goud: iris `#F5C842`, klauwen ivoor-goud `#F3E6B8` / `#BFA06A`. Het budget telt op tot 15 (zie het recept hieronder).
- **Gezicht:** grote ogen met **halfgesloten leden**, een gouden iris en een glans. Eén mondhoek omhoog met **een hoektand**, en mag één wenkbrauw opgetrokken. Sluw maar charmant: een zakkenroller, geen monster.
- **Buit:** in plaats van de rode bes een **gouden munt** (of een glimmend steentje) in de klauwen, in dezelfde goudramp als de klauwen en iris. Zo kost het geen extra kleuren en leest het meteen als "gestolen".
- **Pose:** in frame 1 de huidige sluippose. In frame 2 de "hehe" met **wijd gespreide lange klauwen** en de munt in de lucht (opgegooid).
- **Vooruitwijzing:** de oogvlek wordt het masker, de staartringen de coatistaart, de klauwen blijven (een vast kenmerk van de lijn) en de munt wordt "geven aan de armen". Optioneel kan er een **groene halsdoek** bij (`#3F8F4E` / `#24603A`, de bandietendoek). Die wordt in fase 3 de groene kap of cape van Robin Hood. Dat kost 2 kleuren: laat dan de lichtste crème of één vachttint vallen.
- **Recept:** `{'vacht': [1,2,3,4], 'donker': [5,6], 'creme': [7,8], 'klauw': [9,10], 'oog': [11], 'halsdoek': [12,13]}`, met wit op 14 en de omlijning op 15.

**B. "Nachtdief"**
- Basis indigo-zwart `#2E2A48` / `#1C1A2C` met roestrode accenten `#C2492E` (staartringen, binnenkant van de oren, rand van het masker) en gele ogen `#F5D040`. De lange witte klauwen van Sneasel.
- Het sterkst Dark, maar het minst olinguito, en het botst met een paarsige nachtaap. Alleen kiezen als A te braaf blijft.

**C. "Graaiklauwen"**
- Extra nadruk op de klauwen: **overdreven grote voorpoten** (Grafaiai, Aipom) met zwarte handschoenen en lange ivoren haken. Die worden het iconische kenmerk, zoals de staart bij Treecko. Het lijf blijft klein en de kleur zoals in A.
- Het risico is dat hij een "klauwmonster" wordt in plaats van een charmante dief. Beter is om de handschoenen van C in A te verwerken (dat heb ik gedaan) en de lengte van A te houden.

**Mijn keuze: A.** Jordi's pose blijft. Het type komt uit de Nickit-methode: warm-donker met zwart, sluwe ogen en een gouden accent. De klauwen worden echt lang, en de buit leest eindelijk als buit.

---

## 3. Nachtaap (Psychic): "een tarsier uit een natuurboek"

### Wat werkt
- **De ogen** (Jordi: "geinig"): groot en starend, en het idee van een maansikkel in de iris. Die blijven het hart van het ontwerp.
- **De krulstaart** (Jordi: "geinig"): de Nazca-spiraal moet blijven en groter worden.
- Het contrast "eng maar lief" tussen frame 1 en frame 2 is een goed idee.

### Wat niet werkt
- **De anatomie is letterlijk een tarsier**: kikkerdijen met **grote knieën** (Jordi) en een realistische bouw.
- **Grijsbruin met oranje** is de kleur van het echte dier. Er is geen enkele Psychic-kleur.
- **Oranje uilenogen** lezen als Hoothoot/Noctowl, en Noctowl is in deze repo **Flying/Dark**. Nacht + uil + oranje ogen trekt dus naar **Dark**. Dat geldt ook voor Umbreon: de nacht is in Pokémon het domein van Dark (Espeon is de dag/Psychic, Umbreon de nacht/Dark). Een nachtelijke Psychic moet dus extra duidelijke Psychic-signalen krijgen.
- Er is **geen symbool**: de tekening op het voorhoofd is realistisch (een donkere streep) in plaats van een symmetrisch teken.

### De lat: Abra, Espurr en Oranguru (en de andere Psychics op vel 2)
**Waarom je bij die drie "Psychic" denkt:**
- **Abra:** de **ogen zijn dicht**: de kracht zit achter gesloten ogen. Hij zit in **kleermakerszit of meditatiehouding** met verstopte handen en is volkomen stil. Een **egaal fel goudgeel** dat voor een vos onnatuurlijk is, plus **geometrische bruine "schouderstukken"**.
- **Espurr:** een **lege, wijde blik** zonder emotie. Zijn **oren zijn omgevouwen** over organen met een **oogpatroon** (bij Meowstic open). Een kleine stijve, **frontale en symmetrische** houding met hangende armen en een grote kop. Lavendelgrijs met een wit gezicht. Weinig kleur, maar alles is "onnatuurlijk kalm".
- **Oranguru:** het archetype van de **wijze**: een witte manen als **capuchon of cape**, een paarse vacht, **halfgesloten wijze ogen** en een **voorwerp** (een bladwaaier). Hij zit. Het is een **aap**, net als onze lijn, en dat bewijst dat een aap Psychic kan lezen.

**Wat de rest van de rij bevestigt:**
- **De ogen doen iets onnatuurlijks:** dicht (Abra), leeg starend (Espurr, Natu en Xatu, die nooit knipperen en de toekomst zien), verstopt (Ralts), dromerig of halfdicht (Munna, Musharna, Drowzee), met een **oogpatroon** (Meowstic) of **één gloeiend oog** (Lunatone).
- **Kop en voorhoofd krijgen nadruk:** de grote buitenaardse kop van Elgyem met een hersenpatroon, de "muts" van Hatenna, de parel van Spoink, de horens en het voorhoofd van Indeedee, de tulbandkop van Meditite en de **edelsteen op het voorhoofd** van Espeon.
- **Symmetrie en frontaliteit:** Xatu (totempaal), Baltoy (dogu), Natu, Espurr, Munna. Psychic-soorten staan vaker recht naar je toe dan andere soorten.
- **Zweven of mediteren:** Munna, Solosis, Hatenna, Chingling, Baltoy en Flittle zweven. Abra, Meditite en Oranguru mediteren. Ze rennen of stampen niet.
- **Kleur:** **violet, lavendel, roze/magenta, goud en pastelblauw**, vaak onnatuurlijk voor het dier (een roze tapir, een lavendelkleurige kat, een goudgele vos, een blauw-zwarte kat). De typekleur is magenta-roze, `#F95587`.
- **Symbolen en voorwerpen:** sterren, manen (Lunatone, Cresselia), spiralen en **geometrische ornamenten** (de totemtekening van Xatu, de Nazca-patronen van **Sigilyph**, al een Nazca-Pokémon in de regio), lepels, een slinger (Drowzee/Hypno), een parel, een belletje.
- **Nachtelijk en mysterieus zonder Dark te worden:** Natu/Xatu, Espurr/Meowstic, Elgyem, Hatenna en Lunatone zijn mysterieus door **de ogen en de stilte**, niet door zwart, tanden of een grijns. Woobat (een nachtdier) blijft Psychic dankzij het **hartvormige neusje** en de pluizige ronde vorm.

**Hieruit volgen de middelen** voor de nachtaap: (1) de ogen als typesignaal, mysterieus doordat je niet ziet waar hij kijkt; (2) een **symmetrisch voorhoofds- of maanteken**; (3) een **frontale, kalme en mediterende houding** met de voeten weggestopt (dat lost ook de grote knieën op); (4) **lavendel, zilver en magenta** in plaats van grijsbruin en oranje; (5) de spiraalstaart als **geometrisch symbool** van 2 px dik, met een gloeiende punt; (6) **geen** zwart met geel en geen tandengrijns, want dat leest als Umbreon of Noctowl (Dark).

### Herontwerprichtingen

**A. "Maanogen" (favoriet)**
- **Silhouet:** een grote ronde kop (zo breed als het lijf) met kleine ronde oortjes, en een klein peervormig lijf. Hij zit in **meditatiehouding**, met de benen onder het lijf gevouwen (Abra), dus **geen grote knieën**. Alleen twee lange voeten met de tenen naar buiten piepen eronder uit. Zijn lange vingers liggen met de **toppen tegen elkaar** voor de borst: het gebaar van een ziener of genezer. Achter het lijf staat de **spiraalstaart rechtop**, groot, als een symbool of een halo naast de kop: 1¾ slag en 2 px dik.
- **Typekenmerk: de ogen.** In frame 1 zijn de **oogleden halfdicht**, zodat alleen de onderste helft van de gloeiende iris zichtbaar is: twee **maansikkels als ogen**. Er is geen pupil te zien, dus je weet niet waar hij kijkt. Mysterieus, en het maanmotief zit letterlijk in de blik. In frame 2 gaan de **ogen wijd open**: twee volle gloeiende manen met een kleine pupil. Dat schrikmoment is de "eng"-kant. Tegelijk heft hij één hand met gespreide vingers als een zegen, de "lief"-kant.
- **Voorhoofdteken:** de witte vlekken boven de ogen van de echte nachtaap worden gestileerd tot **twee symmetrische zilveren sikkels**, met in het midden een kleine donkere ruit of spiraal: een Nazca-teken op het voorhoofd, zoals de ster van Kadabra of de edelsteen van Espeon.
- **Kleuren:** vacht lavendelgrijs `#D6CCEB` / `#A193C8` / `#6E5F9A` / selout `#3F3363`; gezicht en sikkels zilverwit `#EEF0FA` / `#B9BCD6`; ogen gloeiend maan-cyaan `#E8FFF8` / `#8FF0E6` / `#3BA8B0`; accent magenta (neusje, handkussentjes, binnenkant van de oren, gloeiende punt van de spiraal) `#F06BA8` / `#B23A7A`. Wit (glans) en de omlijning apart.
- **Gezicht:** volkomen kalm, geen mond in frame 1 (of een klein streepje, zoals Espurr). Frontaal en symmetrisch.
- **Vooruitwijzing:** de sikkelogen en het zilver worden het maanmotief van de genezer (Mama Killa, subtiel). De gevouwen vingertoppen worden de handen van de healer. De spiraal groeit per fase (een krul, dan een spiraal, dan de volle Nazca-spiraal). Het magenta wordt de kleur van zijn helende moves.

**B. "Kleine kallawaya"**
- Oranguru-logica: een **zilveren manen als een capuchon of poncho** om kop en schouders (het begin van de genezersoutfit), en een **bundeltje kruiden of cocablad** in de handen als voorwerp. Frame 1: de **ogen dicht** (Abra). Frame 2: de ogen open en gloeiend.
- Kleuren: vacht diepviolet `#4B3D7A` / `#2E2550`; manen `#D9DCEB`; blad `#5CB85C`; goud `#F2C14E`.
- Een zeer duidelijk Psychic-archetype (de wijze), maar het risico is een mini-Oranguru, en de outfit komt al in fase 1. Bewaar dit liever voor fase 2 of 3.

**C. "Zwevend nachtgeestje"**
- Geen benen: een druppelvormig lijf dat **zweeft** (Ralts, Hatenna, Munna), met enorme ogen en de spiraalstaart als een **slinger** eronder. Pastellavendel en roze.
- Het meest Psychic en het minst aap. Het verliest de "eng"-kant en de band met de nachtaap. Alleen als A te aards blijft.

**Mijn keuze: A.** Het bouwt verder op wat Jordi goed vond (de ogen worden **mysterieuzer** door de sikkels en de verborgen pupil, de **krulstaart** wordt het symbool), lost de **knieën** op met de meditatiehouding, en verschuift de kleur van "natuurboek" naar Psychic zonder naar Dark te trekken.

---

## Volgende stap
Per starter eerst **2–3 silhouetten** (zwart, 64×64) volgens A, plus één alternatief (B), naast Torchic, Litten, Sprigatito en de typereferenties van vel 2 op 1×. Jordi kiest. Daarna pas het palet en het pixelwerk. Toets elke sprite aan de checklist "Pokémon-design" in `SPRITE_PLAN.md`.
