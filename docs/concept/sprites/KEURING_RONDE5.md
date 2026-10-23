# Keuring ronde 5 (onafhankelijk): waarom het fakemon blijven

Gekeurd (frame 1 en 2, 64×64): alpaca ronde 4 + 5, olinguito ronde 4 + 5, nachtaap ronde 2–5, Cuyby ronde 1 (A en B), DJ Rotom ronde 1.
Vergeleken met de echte Gen 3-sprites (`graphics/pokemon/*/anim_front_gba.png`): de 9 starters van Gen 1–3, en Mareep, Ponyta, Growlithe, Eevee, Electrike, Skitty, Zigzagoon, Sentret, Poochyena, Teddiursa, Sneasel, Aipom, Abra, Natu, Spoink, Smoochum, Rattata en Whismur. Daarnaast de DS-sprites van Chimchar, Espurr, Pachirisu en Bidoof, en Rotom met al zijn vormen.

Vellen in `keuring_ronde5/` (3× en 1×):
- `v_blinde_rij.png`: de vier dieren tussen twaalf echte Gen 3-sprites, zonder namen. **Begin hiermee.** De kandidaten zijn 1, 2, 6 en 9, en die haal je er binnen een seconde uit.
- `v_overzicht.png`: de vier ronde-5-sprites boven de Gen 1–3-starters.
- `v_alpaca.png`, `v_olinguito.png`, `v_nachtaap.png`, `v_cuyby.png`, `v_rotom.png`: per soort naast de buren met dezelfde bouw.
- `v_rotom_inspiratie.png`: het DJ Rotom-ontwerp (referentie) naast ronde 1 en Heat, Frost en Wash.
- `v_silhouet.png`: de silhouetten, zwart op 2× en 1×.
- `z_r4r5.png`: alpaca en olinguito, ronde 4 naast ronde 5 op 6×.
- `scripts/`: de vellen en de metingen (`metrics.py`, `colour.py`, `straight.py`). Draaien vanuit de repo-root met `python3 docs/concept/sprites/keuring_ronde5/scripts/<script>.py`.

---

## 1. De kern, voor alle vijf tegelijk

Vijf rondes 'details verbeteren' werkten niet, omdat de fout niet in de details zit. De sprites hebben drie gemeenschappelijke problemen. Het eerste is het belangrijkste.

### Kern 1: het type zit in **spullen** in plaats van in het **lijf**. Dat is hét kenmerk van een fakemon.

Zet op een rij wat elk ontwerp 'Pokémon' moet maken:

| sprite | wat het type/de rol draagt | waar het zit |
|---|---|---|
| alpaca | bokshandschoenen met gouden manchet, wit hoedje met rode band | aangetrokken spullen |
| olinguito | groene sjaal, munt, zwarte handschoen/armband, bril-masker | aangetrokken spullen |
| nachtaap | edelsteen op de borst (r2–r3: ook vier sieraden) | opgeplakt sieraad, verder lijf (ogen, spiraal) |
| Cuyby B | gebreide chullo-muts | aangetrokken spullen |
| Cuyby A | niets: een cavia met een kuifje en een spiraal-sticker | geen idee |
| DJ Rotom | een generieke boombox (handvat, cassettedeck, sleuven, display) met een klein Rotom-koepeltje erop, in plaats van het DJ Rotom-ontwerp (speaker – Rotom-kop – speaker) | afwijking van een bestaand ontwerp; zie §2 |

Bij Game Freak komt het idee uit de anatomie. Makuhita's handen **zijn** de handschoenen. Sneasels klauwen en oorveer zijn lijf. Bij Meowth zit de munt **ín het voorhoofd**. Sentrets buikcirkel en Furrets ringen zijn vachttekening. Rotom-Frost **is** de koelkast: zijn kuif groeit uit de bovenkant en de deurspleet is zijn mond. Fase-1-starters dragen bijna nooit iets. Het 'kostuum' groeit pas in de eindvorm uit het lijf (Decidueye, Incineroar, Meowscarada). SPRITE_PLAN.md zegt dit ook al (facet 8, "kleding uit het eigen lijf"), maar geen enkele sprite doet het.

Het bewijs zit in Jordi's eigen rangorde. Hoe minder spullen, hoe hoger de sprite eindigt. De nachtaap heeft één sieraad en verder alleen lijf (ogen, spiraalstaart): **die zit het dichtst bij**. De olinguito heeft er drie, de alpaca twee. Bij DJ Rotom ligt het anders (zie §2): daar bestaat het ontwerp al, en de fout is dat het niet is nagebouwd.

### Kern 2: de pijplijn maakt plastic speelgoed, geen gespriete tekening

De sprites ontstaan uit vormen in een script, een automatische schaduw ('masker min verschoven kopie'), een automatische selout-pass en daarna handwerk. Dat geeft meetbare, consequente afwijkingen ten opzichte van Gen 3:

| meting (frame 1) | Gen 3 (gemiddeld) | kandidaten |
|---|---|---|
| oppervlak in pixels, fase-1-starters | **808** (Treecko 967 als grootste) | alpaca 1300, nachtaap 1230, Cuyby 1171, olinguito 1052 |
| losse 'accentpixels' (pixel zonder gelijke buur) per pixel oppervlak | **0,17** | 0,065–0,098 (de helft) |
| kleurwissels per pixel ('detail') | 1,84 | alpaca 1,36, Cuyby 1,39–1,45 |
| verzadiging van de gekleurde pixels | starters ±0,66 | nachtaap 0,42 |
| randpixels in rechte runs ≥5 px (hoekigheid) | 0,19 (0,04–0,35) | olinguito r5 **0,39**, DJ Rotom **0,59** |

Te groot, te glad, te weinig enkele pixels: grote egale vlakken met overal dezelfde sikkelschaduw. Dat is het 'vinylfiguurtje'-effect uit de keuring van ronde 3. Gen 3-sprites zijn op 1× juist kleiner en drukker. Ze hebben veel losse pixels: een glans, een klauwpuntje, een plukje, een onderbroken lijn. De tekenaars zien dit zelf ook ('nog wat groot', 'schaduw deels uit een script'), maar elke ronde blijven de getallen hetzelfde, omdat de pijplijn dezelfde blijft.

### Kern 3: er is geen vast ontwerp, dus het ontwerp verandert bij elke pixelronde

Er is geen modeltekening. Het ontwerp wordt in 64×64 bedacht en tegelijk gepixeld. Elke 'handwerkronde' beslist het ontwerp daardoor opnieuw. **Daarom is ronde 5 slechter dan ronde 4.** De opdracht was 'lijf en poten met de hand afwerken', maar de kop van de alpaca en die van de olinguito zijn in de praktijk opnieuw ontworpen (zie `z_r4r5.png`). `check.py` keurt alleen statistiek (formaat, selout, lichtrichting) en laat dus een fakemon zonder FOUT door.

---

## 2. Per sprite

### Alpaca (ronde 4 → 5)

**Wat er in ronde 5 slechter werd** (`z_r4r5.png`):
- **Doosvormige kop:** een rechthoek met een loodrechte voorkant. De rechte runs in de contour stegen van 0,19 naar 0,26.
- **Wollen capuchon rond een bruin gezichtsmasker:** het leest als een hoofddoek of bivakmuts, niet als een alpacakop.
- **Oren als twee hoge, puntige hoorns:** het wordt een geit of lama.
- **Vier dunne, rechte stokpoten:** dat zijn volwassen verhoudingen. Jordi vroeg 'fluffier', en dit is het tegendeel.
- **Rode 'schoen' aan de voet:** de handschoen van de verre voorpoot staat op de grond en leest als een rood laarsje.

Ronde 4 was rommeliger, maar ronder en wolliger, met kortere poten.

**Waarom het een fakemon blijft:**
- **Een realistische kameelachtige snuit** die naar links uitsteekt. Echte Pokémon-viervoeters in fase 1 (Growlithe, Eevee, Mareep, Skitty) hebben een korte snuit en grote ogen laag in de kop. Bij de alpaca zitten de ogen hoog en ver naar achteren, zoals bij een paard.
- **Een lijf in puur zijaanzicht** (wolkenblok met vier poten), terwijl de kop in driekwart staat.
- **64% van de pixels is neutraal** (wit, grijslavendel, zwart). Bij Mareep is dat 19%: zijn 'witte' wol is crème met een warme gele schaduw (255,238,131 → 230,197,98 → 197,148,41). De grijslavendelen schaduw van onze wol is de 'generieke kleur' waar Jordi in ronde 1 al over begon.
- **Het silhouet** (`v_silhouet.png`) is een verzameling uitsteeksels (oren, hoed, twee handschoenen, vier poten) zonder één vorm die je herkent.

**Prioriteiten:**
1. **[ontwerp] Het kostuum moet eruit en de handschoenen moeten uit het lijf komen.** Haal het hoedje weg: de bombín is de belofte voor fase 3. In fase 1 is hooguit het zaadje te zien, bijvoorbeeld een kuif die al iets van een koepel heeft. Maak de 'handschoenen' van de voorpoten tot **wolbollen**: dezelfde geschulpte wolrand, naadloos vast aan de poot, zonder manchet of band. Ze mogen een eigen, verzadigde wolkleur hebben (rozerood) en zijn groter dan de achtervoeten (één uitvergroot lichaamsdeel, zoals de handen van Makuhita). Zo blijft Jordi's grap staan, maar wordt het anatomie.
2. **[ontwerp] Een andere kop.** Het kenmerk van een alpaca is niet de snuit, maar de **wollen kuif** (de 'topknot' over de ogen) en het korte, platte gezicht. Maak die kuif tot de grootste vorm van de kop, met de oren erdoorheen en de ogen er groot en laag onder. Optioneel en Jordi's keuze: een kuif in de vorm van een **hoofdbeschermer van een bokser**. Dan zit Fighting in de anatomie.
3. **[ontwerp/uitvoering] Babyverhoudingen:** een compacte wolbal als lijf (Mareep, Wooloo), korte stompe poten in plaats van stokjes, een korte en dikke hals. De kop is minstens 45% van de hoogte en het oppervlak ±850–950.
4. **[uitvoering] Kleur:** een warme wolramp met kleur (crème, geel of perzik in de schaduw, zoals Mareep) en geen grijslavendel. De bruine gezichtsvacht mag blijven. Het accent is het rood van de wolbollen.
5. **[uitvoering] Pose:** het lijf ook in driekwart naar de kijker (Growlithe, Mareep). Eén wolbol opgeheven in dekking, en in frame 2 een stoot.

### Olinguito (ronde 4 → 5)

**Wat er in ronde 5 slechter werd:**
- **De kop werd een afgeplatte rechthoek** met een platte bovenkant. De ronde teddybeerkop met ronde oren, het kenmerk van de echte olinguito, is weg. De rechte runs in de contour gingen van 0,19 naar **0,39**: boven het maximum van Gen 3.
- **De ogen staan nu in volle zwarte kaders:** het leest als een **skibril of vliegbril**, precies de klacht van ronde 2.
- **Het lijf is samengeperst.** Ook op 88% van de opzet zitten alle details er nog in, dus het wordt drukker.
- **De klauwen zijn een witte waaier of kam** die schuin naar beneden wijst. Het leest niet als een hand.

**Waarom het een fakemon blijft:**
- **Drie spullen voor één rol** (sjaal, munt, handschoen) plus een bril-masker. Een dief wordt bij Pokémon verteld met lichaamstaal: Nickit sluipt en Purrloin zit 'onschuldig'. Een rekwisietentafel doet dat niet.
- **Te donker en te zwart.** De gemiddelde helderheid is **0,32**, de donkerste van alle bekeken sprites (Sneasel 0,40, Poochyena 0,46, het Gen 3-gemiddelde ±0,52). 90–95% van de buitenrand is zwart (Gen 3: 48%) en 15% van de binnenpixels is zwart (Gen 3: 5%). Op 1× is het een bruine vlek (`v_blinde_rij.png`, nr. 6). Jordi vroeg 'wat donkerder', niet 'alles donker'. Dark zit bij Pokémon in **contrast + één gloeiend accent**, niet in een donkere sprite.

**Prioriteiten:**
1. **[ontwerp] Sjaal, munt en armband eruit.** Het enige uitvergrote kenmerk zijn de **lange klauwen**: Jordi's eis, en het vaste kenmerk van de hele lijn. Laat de dief zien met de pose (op de tenen, gebogen, één klauw geheven) en het gezicht (sluwe halfdichte ogen, een scheve grijns met een hoektand). Buit kan hooguit in frame 2 kort in de klauw: dat is een karaktermoment, geen onderdeel van het ontwerp.
2. **[ontwerp] De ronde teddybeerkop terug** (ronde 4 zat dichterbij), met ronde oren en een korte snuit. Het masker wordt **één band dwars over de ogen** zoals bij Zigzagoon: de ogen liggen ín de band, zonder ring per oog. Dan is het een vachttekening en geen bril.
3. **[uitvoering] Lichter en warmer basispalet.** Echte olinguito's zijn oranjebruin: neem dat als hoofdkleur. Het donker komt alleen op het masker, de sokken en de staartringen, met goudgele ogen als het enige gloeiende accent. Selout aan de lichtkant in de donkerste vachttint, en zwarte binnenlijnen alleen waar delen overlappen. Doel: gemiddelde helderheid ≥0,42, zwart aan de buitenrand ≤0,6.
4. **[uitvoering] Rondere vormen:** contouren in getrapte runs (1-2-3) in plaats van rechte balken. De rechte runs moeten weer naar ±0,2.
5. **[uitvoering] De klauwen als hand:** drie gebogen haken die uit één poot komen, met verschillende lengtes. Het oppervlak mag ±900.

### Nachtaap (ronde 2–5): bijna, en wat het laatste stukje is

**Wat goed is en waarom hij het dichtst bij zit:** hij is het enige ontwerp waarvan het idee in het **lijf** zit: ogen die te groot zijn (tarsier), het nachtaapmasker (sinds ronde 4) en de spiraalstaart. Het silhouet (kop als bol + spiraal) is op 1× meteen herkenbaar (`v_silhouet.png`). Van de kandidaten is dat het beste silhouet.

**Het laatste stukje (in volgorde van belang):**
1. **[ontwerp/kleur] Hij is eenkleurig pastel.** 77% van de pixels valt in één lavendeltint, met een verzadiging van 0,42 (Aipom 0,58, Abra 0,88, de starters ±0,66). Echte Psychic-apen en -katten hebben twee zones: Aipom paars met een crème gezicht, Chimchar oranje met crème, Espurr grijs met wit en paars. Een nachtaap heeft van nature precies zo'n patroon: **een licht gezicht (witte 'wenkbrauwen' en snuit) in een donkere vacht**. Bij ons is het omgekeerd: een licht lijf met donkere strepen. Dat is de hoofdreden dat hij 'knuffel' leest in plaats van 'mysterieus'. Advies: een **dieper, verzadigder violet/indigo lijf**, met een **bleke gezichtsschijf** waarin de ogen staan. Paars blijft het, dus Jordi's goedkeuring van de kleur blijft gelden, maar dit is wel een keuze die hij moet maken.
2. **[uitvoering] De ogen zijn glazen poppenogen** (marineblauw, cyaan reflectie, twee witte glanzen). De **vorm** van ronde 2/3 mag blijven (die vond Jordi geinig). De **weergave** moet anders: een iris die egaal gloeit (lichtcyaan, of magenta/roze in het palet; geen geel op zwart, want dat is Dark-terrein, zie SPRITE_PLAN), een kleine pupil en **één** glanspixel. Glans betekent onschuld. Een egale gloed betekent 'ziet iets wat jij niet ziet' (Espurr, Natu). Dan zijn de ogen zelf het psychische orgaan.
3. **[ontwerp] Haal de borststeen weg.** Het is het laatste opgeplakte sieraad. Met de gloeiende ogen + spiraalstaart zijn er genoeg Psychic-signalen.
4. **[uitvoering] De pose leest als Fighting.** Ronde 4/5 staat in een brede sumohurk met dijen zo groot als de kop: precies Jordi's oude klacht ('knieën wat groot'). Tarsierverhoudingen zijn juist **dunne, lange ledematen met grote handen en voeten (vingerkussentjes)**. Kies een zittende of zich vastklampende houding, met de handen dicht bij het gezicht of één hand geheven (frame 2), en een kleiner lijf (oppervlak ±850–950, nu 1230).
5. **[uitvoering] De middelste streep van het masker** loopt over de hele schedel en leest op 1× als een naad in een helm of bowlingbal. Maak er een korte, donkere wig tussen de wenkbrauwen van. De twee zijstrepen worden dunner, langs de rand van de gezichtsschijf.

### Cuyby (ronde 1, A en B)

**Waarom 'zo overduidelijk een fakemon':** het is een **kawaii-sticker van een echte cavia**. De signalen:
- **Een plat liggend 'broodje'** in zijaanzicht, zonder zichtbare poten.
- **Stipoogjes** met één glans, en **roze blosovaaltjes**. In frame 2 dichte ^^-ogen.
- **Een spiraal als sticker** op de flank. Die verandert het silhouet niet.
- **B: een gebreide muts**, een kledingstuk.

Elk vroeg Normal-type van Game Freak heeft **één overdreven kenmerk dat het silhouet maakt**: Sentrets gestreepte staart, Zigzagoons zigzagvacht, Whismurs oorschelpen, Skitty's staartbol, Rattata's tanden en krulstaart, Bidoofs tanden. Cuyby heeft er geen. Het silhouet (`v_silhouet.png`) is een bobbelige ovaal die elk knaagdier kan zijn. Hij **ligt** ook, terwijl Rattata, Sentret, Skitty en Whismur rechtop staan, alert en naar de speler gericht.

**Prioriteiten:**
1. **[ontwerp] Eén Pokémon-twist kiezen** (keuze voor Jordi). Drie opties:
   - (a) De **rozetten van de Abessijnse cavia** worden geometrische, rechtopstaande kruinen die het silhouet breken, zoals Zigzagoons vacht.
   - (b) De **driekleurige vlekken** van de huiscavia worden strakke geometrische kleurvlakken, zoals de buikcirkel van Sentret.
   - (c) Het **'wheeken'** (fluiten) als kenmerk, zoals Whismurs oren: wangzakken of een snuit die opbolt als hij fluit.
2. **[ontwerp] Rechtop en naar de speler:** zittend in driekwart, met de voorpootjes zichtbaar en de kop naar voren. Frame 2 = fluiten of een popcornsprongetje (cavia's springen van blijdschap), met de mond open.
3. **[uitvoering] Kawaii-signalen eruit:** de blosjes weg. Ogen met een vorm (ooglid, iris, glans zoals bij Skitty en Teddiursa), en een mondlijn.
4. **[ontwerp] B: geen muts.** Wil Jordi het Andesmotief, laat het dan uit het lijf komen: een vachtpatroon in chullo-motief, of oren die als oorflappen hangen.
5. **[uitvoering] Kleiner** (1171 → ±700–850; Rattata 518, Whismur 884) en schaduw in clusters in plaats van een verloop.

### DJ Rotom (ronde 1): niet trouw aan het DJ Rotom-ontwerp

*Bijgesteld na Jordi's correctie: "DJ Rotom is duidelijk een Rotom-vorm, maar niet DJ Rotom; je hebt het niet goed nagebouwd." Als Rotom-vorm leest hij dus wel. De fout is dat het bestaande ontwerp uit Pokémon Pokopia niet is nagebouwd. De tekenaar kreeg 'niet kopiëren, zelf tekenen' mee, en dat was te streng. **Het ontwerp moet trouw zijn aan DJ Rotom; alleen de pixels zijn eigen werk in Gen 3-stijl.***

Vergelijk `v_rotom_inspiratie.png` (links de referentie, daarnaast ronde 1) en de overworld-sheet in `dj_rotom/inspiratie/`, die de opbouw van alle kanten laat zien.

**Wat het echte ontwerp is** (drie delen naast elkaar):
- **Twee staande speakerkasten** links en rechts. Ze zijn hoog en smal (staand formaat), oranje, met een **donkere voorkant** waarin **twee conussen boven elkaar** zitten (klein boven, groot onder). Ze staan iets schuin naar buiten, als 'armen'.
- **Rotoms kop als middenblok**, ongeveer even hoog als de kasten en iets naar voren en lager geplaatst. Het is een afgeronde, oranje vierkante kop met de Rotom-kuif bovenop, **grote schuine, boze Rotom-ogen** (wit met een blauwgroene iris) en een **brede, open mond** die bijna de hele onderste helft van de kop beslaat. In die donkere mond staat een **groene equalizer**, met in de grote versie witte tandjes bovenaan.
- **De noot-bliksem:** een mintgroene zigzagbliksem die achter of naast de kuif omhoog schiet en eindigt in een **vlaggetje of plaatje met een muzieknoot**.
- **Mintgroene gloed** rond het **hele** silhouet: één doorlopende rand van ±2–3 px om de drie delen samen, met een donkerder blauwgroene buitenkant.
- **Silhouet:** breed en laag (lijf zonder de bliksem ±1,7 : 1), licht gekanteld, met drie duidelijke 'blokken' en kleine gleuven ertussen. Er is geen handvat, geen cassettedeck, geen staal en geen display.

**Waar ronde 1 afwijkt** (gemeten op frame 1):
| | DJ Rotom (referentie) | ronde 1 |
|---|---|---|
| opbouw | 3 losse delen: speaker – kop – speaker | 1 doorlopende boombox-kast met een koepeltje erop |
| kop | middenblok op volle hoogte, ogen groot en boos, mond = de halve kop | klein koepeltje boven de kast, ogen ±3 px en rechtop ('braaf') |
| mond | brede open grijns met een equalizer erin | los displaytje onder de ogen, gescheiden van de kop |
| speakers | staand, 2 conussen boven elkaar op een donkere voorkant | 2 ronde speakers naast elkaar op een oranje frontje |
| extra's | geen | handvat, cassettedeck met spoeltjes, ventilatiesleuven, zijpaneel in perspectief |
| verhouding lijf b:h | ±1,7 : 1, breed en laag | ±1,07 : 1 (47×44), bijna vierkant, met het handvat erbovenop |
| staal/grijs | ±0% | 24% van de pixels |
| donkere vlakken (speakervoorkant, mond) | 21–38% | 15% |
| contour | afgerond, gekanteld | 0,59 rechte runs: een orthografisch blok |
| bliksem | mint, uit de kop omhoog, met een notenvlag | apart rechtsboven, los van de kuif, noot als losse vorm |
| gloed | mint met een donkere buitenrand, sluit de drie blokken samen | lichtmint, valt weg tegen een lichte achtergrond |

Kort gezegd: de tekenaar heeft een **generieke boombox** getekend en daar een kleine Rotom op gezet. Het eigen DJ Rotom-ontwerp is juist dat Rotom zelf het middendeel van de installatie **is**, met de speakers naast zich.

**Prioriteiten (de volgende ronde neemt het ontwerp letterlijk over):**
1. **[ontwerp] De opbouw van de referentie overnemen:** speaker – Rotom-kop – speaker, als drie afgeronde oranje blokken met smalle gleuven ertussen. De kop is het middenblok op volle hoogte, iets naar voren. Handvat, cassettedeck, sleuven, zijpaneel en display gaan eruit.
2. **[ontwerp] Het gezicht van DJ Rotom:** grote, schuine, boze ogen (met de Rotom-ogen van Heat/Frost als pixelvoorbeeld) en een brede open mond over de onderste helft van de kop, met daarin de groene equalizer (staafjes van verschillende hoogte; in frame 2 een ander patroon). Een of twee witte tandjes bovenaan mag.
3. **[ontwerp] Speakers zoals in het origineel:** staand, met een donkere voorkant en twee conussen boven elkaar (klein + groot). Licht schuin naar buiten. In frame 2 'pompen' de conussen (1 px groter): dat idee uit ronde 1 is goed en mag blijven.
4. **[uitvoering] Silhouet en verhouding:** breed en laag (±1,7 : 1 zonder bliksem; bijvoorbeeld 58 breed, ±34 hoog voor het lijf), een paar graden gekanteld, afgeronde hoeken. De kuif staat bovenop de kop, en de mintgroene **bliksem met notenvlag** schiet daar direct naast omhoog.
5. **[uitvoering] Kleur en gloed:** alleen oranje (kasten + kop), donker navy/zwart (speakervoorkant + mond), mint/groen (equalizer, bliksem, gloed) en wit/blauw (ogen). Geen staal. Eén doorlopende gloed van 2–3 px om het hele silhouet, met de **donkerste tint buitenaan** zodat de rand op een lichte achtergrond niet wegvalt.

Werkwijze voor deze sprite: leg de referentie (`dlkf051-….png`, 176 px) verkleind naar het doelformaat als onderlegger, en neem verhoudingen, plaatsing en vormen over. Teken de pixels zelf opnieuw in Gen 3-stijl, met het oranje en de ogen uit het palet van de echte Rotom-vormen. 'Eigen werk' betekent hier: eigen pixels, niet een eigen ontwerp.

---

## 3. Werkwijze voor de volgende ronde

Vijf rondes pixelwerk aan een ontwerp dat geen Pokémon-ontwerp is, leveren een steeds nettere fakemon op. Het advies is: **eerst het ontwerp vastleggen, dan pas pixelen, en elke laag apart laten goedkeuren.**

1. **Ontwerpronde zonder pixels.** Maak per soort **drie duidelijk verschillende concepten** als vlakke tekeningen op 128–256 px (SVG of PNG). Bouw ze op uit geometrische basisvormen (bal, peer, cilinder, druppel), zoals Sugimori dat doet: egale kleurvlakken, geen schaduw. Elk concept krijgt één regel 'dier × idee × type × twist'. Er mogen **nul spullen** in zitten, tenzij dat ene voorwerp de twist is (Meowths munt, Farfetch'ds prei). Jordi kiest een concept, en dat wordt de **modeltekening**: vanaf dan staat die vast en wordt hij in pixelrondes nooit meer veranderd. Dit is de goedkoopste plek om 'Pokémon genoeg?' te beantwoorden. Als Jordi zelf een schets kan maken of laten maken, is dat de beste bron.
2. **Een echte Gen 3-sprite als skelet.** Kies per soort één officiële sprite als onderlegger voor pose, verhoudingen, formaat, clustergrootte en lijnbehandeling, en teken de modeltekening daaroverheen op 1×:
   - nachtaap: Aipom (kop en gezicht) + de zithouding van Chimchar;
   - alpaca: Mareep (wollijf) + Growlithe (driekwartstand);
   - olinguito: Teddiursa (kop) + Zigzagoon (lijf en masker);
   - Cuyby: Skitty of Whismur;
   - **DJ Rotom:** de referentie uit Pokopia zelf is de onderlegger (opbouw, verhoudingen, gezicht). Voor de pixels van de ogen en het oranje kun je Rotom-Heat/Frost gebruiken.

   Het skelet bepaalt alleen de constructie. De pixels worden opnieuw getekend.
3. **Het palet uit de referentie.** Neem de rampopbouw (stappen in helderheid, tintverschuiving, verzadiging) over uit het palet van de skeletsprite (`normal_gba.pal`) en draai alleen de tint. Dan heb je meteen Gen 3-kleuren in plaats van zelf gemengde pasteltinten.
4. **Geen automatische schaduw meer.** De sikkelschaduw uit het script en de selout-pass vervang je door clusters die met de hand per vorm gezet zijn. Doelen ten opzichte van Gen 3: losse accentpixels ±0,15 per pixel oppervlak, rechte runs ≤0,25 en een oppervlak voor fase 1 van ±800–950.
5. **Elke laag apart goedkeuren, en een goedgekeurde laag niet meer aanraken:** silhouet → vlakke kleuren → lijnen en schaduw. Een ronde wijzigt maar één laag. Ronde 5 ging achteruit omdat 'afwerken' ongemerkt ook 'opnieuw ontwerpen' werd.
6. **Blinde test vóór Jordi.** Zet de 1×-sprite op een veld tussen 15 echte Gen 3-sprites (`scripts/lineup.py`). Vraag een frisse agent, zonder context, welke er niet bij hoort en waarom. Wordt hij meteen gekozen, dan gaat hij niet naar Jordi. Deze test vangt precies wat `check.py` mist.
7. **Aanvulling op `check.py`** (alleen als hulpmiddel; een ontwerpfout maakt het niet goed): meet ook de verzadiging van de gekleurde pixels, de rechte runs in de contour, het aandeel losse accentpixels en een bovengrens voor het oppervlak bij starters (zie `scripts/metrics.py`, `colour.py` en `straight.py`).

## 4. Kort oordeel

| sprite | kern | soort probleem |
|---|---|---|
| alpaca | dier in kostuum (hoedje + aangetrokken handschoenen) met een realistische paardensnuit; r5 werd hoekiger met stokpoten | vooral ontwerp |
| olinguito | rekwisieten (sjaal, munt, armband) in plaats van lichaamstaal; r5: doosvormige kop, skibril-ogen, te donker en te zwart | ontwerp + uitvoering |
| nachtaap | goed lijfconcept; laatste stukje: eenkleurig pastel (geen licht gezicht in een donkere vacht), glazen poppenogen, borststeen, sumohurk | vooral uitvoering + één kleurkeuze |
| Cuyby | een kawaii-sticker van een echte cavia; geen twist, ligt plat | ontwerp |
| DJ Rotom | leest als Rotom-vorm, maar is niet DJ Rotom: een generieke boombox met een Rotom-koepeltje in plaats van speaker – Rotom-kop – speaker met de equalizer-mond | ontwerp (trouw aan de referentie) |
