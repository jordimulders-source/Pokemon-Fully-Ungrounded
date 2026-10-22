# Spriteplan: fakemon en regional forms in Hoenn-stijl

Studie van de Hoenn-sprites (22 okt) en het plan voor hoe wij nieuwe Pokémon-sprites maken.
Alle getallen hieronder zijn gemeten over de 202 soorten van de Hoenn-dex (`HOENN_DEX_TREECKO`..`HOENN_DEX_DEOXYS`)
met de scripts in `tools/concept/sprites/` (zie §7). "p10..p90" = 80% van de Hoenn-sprites valt daartussen.
Illustraties: `docs/concept/sprite_studie/` (1 t/m 6).

---

## Pokémon-design (niet alleen pixeltechniek)

*Toegevoegd na kritiekronde 1 (22 okt, zie `sprites/KRITIEK_RONDE1.md`). Jordi: "Het zijn gewoon dieren en geen Pokémon."* De rest van dit plan gaat over **hoe** je pixelt. Deze sectie gaat over **wat** je tekent, en komt dus eerst: een technisch perfecte sprite van een gewoon dier is nog geen Pokémon.

### Een Pokémon is dier × idee × type
- **Dier:** het echte dier (alpaca, olinguito, nachtaap).
- **Idee:** een rol, een archetype, een voorwerp of een mythe (bokser, dief, ziener; kampioen, Robin Hood, genezer).
- **Type:** het element of de energie, zichtbaar zonder uitleg.

Een sprite die alleen het dier toont, faalt. Toets bij elk ontwerp of je alle drie in één oogopslag ziet. De maatstaf (Jordi): "als je een Oranguru ziet, weet je vrijwel zeker dat het Psychic is, zelfde met een Abra of een Espurr."

### De facetten die een dier tot een Pokémon maken
1. **Stilering: eerst een vorm, dan een dier.** Een basisvorm draagt het ontwerp: een bal (Wooloo, Jigglypuff, Voltorb, Rowlet), een ei of peer (Torchic, Mudkip), een wolk (Mareep, Swablu, Altaria), een druppel (Ralts, Hatenna) of een cilinder (Snorlax, Wynaut). Anatomie wordt vereenvoudigd: poten als stompjes, gewrichten verdwijnen in het lijf.
2. **Overdreven proporties.** In fase 1 is de kop 40–60% van de hoogte, met grote ogen. Precies **één** lichaamsdeel is uitvergroot: de oren van Pikachu, de staart van Treecko, de handen van Makuhita, de kop van Elgyem, de klauwen van Sneasel.
3. **Eén onrealistisch kenmerk** (de "twist"), ook bij gewone dieren: de bol aan de staart van Mareep, de buikcirkel van Sentret, de ringen van Furret, de hand aan de staart van Aipom, de sjaalstaart van Minccino, de schedel van Cubone, de prei van Farfetch'd, de lokstaart van Slowpoke, de bladmanen van Skiddo, de bloem van Deerling, de modderlaarzen van Mudbray.
4. **Element-onderdelen:** lichaamsdelen van het element. Vuur: de staartvlam van Charmander, de rugvlammen van Cyndaquil, de kuif van Torchic, de vlam op het achterwerk van Chimchar. Water: de vin van Mudkip, de schuimsjaal van Froakie, de neusballon van Popplio. Gras: de bol van Bulbasaur, het blad van Chikorita, het spruitje van Turtwig, de bloemvorm in het patroon van Sprigatito. Elektrisch: de wangen van Pichu. Steen: de kristallen van Roggenrola.
5. **Ogen en gezicht met karakter:** grote ogen met een grote glans, plus een ooglid of wenkbrauw die een houding uitdrukt. Grookey is ondeugend, Litten afstandelijk, Pancham dwars, Fuecoco goofy, Riolu alert, Purrloin zelfvoldaan en Espurr leeg. Gekleurde oogwitten (Poochyena), dichte ogen (Abra) en een oogpatroon (Meowstic) zijn al een typesignaal.
6. **Kleur:** 2–3 **grote, egale hoofdkleuren** plus één accent, gekozen op het type en vaak **onnatuurlijk** voor het dier: een blauwe Mudkip en Totodile, een groene Snivy, een goudgele Abra, een roze Munna, een lavendelkleurige Espurr. Natuurlijke vachtkleuren (beige, bruin, grijs) lezen als Normal of als "gewoon dier", tenzij een type-accent of een sterk contrast het overneemt (Nickit: roodbruin, maar met zwarte sokken en sluwe ogen).
7. **Geometrische tekeningen**, die op afstand leesbaar zijn: ringen, strepen, cirkels en symmetrie. Denk aan de buikcirkel van Sentret, de ringen van Furret en Umbreon, de strepen van Galar-Zigzagoon, de spiraal van Stufful, de schouderstukken van Abra, de totemtekening van Xatu en de Nazca-patronen van Sigilyph.
8. **"Kleding" uit het eigen lijf:** de cape van Piplup, het strikje van Rowlet en de capuchon van Decidueye, de riem van Incineroar, het masker van Hawlucha, de mouwen van Mienfoo, de slobberbroek van Scraggy, de hoed van Murkrow, de cape van Meowscarada en de manen van Oranguru. Een **voorwerp** kan ook: de balk van Timburr, de prei van Farfetch'd, de lepels van Alakazam, de waaier van Oranguru, de munt van Meowth.
9. **Persoonlijkheid in pose en frame 2:** de houding vertelt de rol. Riolu staat klaar, Abra mediteert, Purrloin zit "onschuldig" en Nickit sluipt. Frame 2 is een karaktermoment, niet alleen "bek open".
10. **Een uniek silhouet:** het element-onderdeel of de twist breekt de omtrek (de kuif van Torchic, de vin van Mudkip, de staart van Treecko, de oren van Fennekin). Zwart op 1× moet de soort herkenbaar blijven en niet verwisselbaar zijn met een bestaande.
11. **Fase 1 belooft de eindvorm:** Litten wordt Incineroar, Froakie wordt Greninja, Rowlet wordt Decidueye, Fennekin wordt Delphox, Sprigatito wordt Meowscarada. Het zaadje van het kostuum of het idee zit er al in.
12. **Gespriet als Pokémon, niet geïllustreerd:** grote egale vlakken met een paar duidelijke schaduwvormen, en geen textuurruis. Fluffy maak je met een **geschulpte buitenrand** (Wooloo, Mareep), niet met vlekken binnenin.

### Type zichtbaar maken: vaste middelen per type
Typekleur = de kleur van het type-icoon in de games. "Typisch palet" = wat de Pokémon zelf meestal gebruiken (dat wijkt soms af: Dark-Pokémon zijn zelden bruin zoals hun icoon).

| type | typisch palet | vormtaal en motieven | voorbeelden |
|---|---|---|---|
| Normal | beige, bruin, crème, roze, wit | rond en zacht, natuurlijke vachtkleuren, één schattige twist | Sentret, Zigzagoon, Wooloo, Lillipup, Bidoof, Skwovet |
| Fire | rood, oranje, geel + donkere basis | vlammen als kuif, staart of kraag, gloeiende vlekken, rook | Charmander, Cyndaquil, Torchic, Litten, Fuecoco, Houndour |
| Water | blauw, cyaan, wit, crème | vinnen, kieuwen, schelpen, schuim en bubbels, gladde rondingen | Mudkip, Froakie, Popplio, Sobble, Quaxly, Wooper |
| Grass | groen + crème, roze of geel bloem-accent | bladeren, knoppen, bloemen, spruiten, zaden | Bulbasaur, Chikorita, Treecko, Snivy, Sprigatito, Skiddo |
| Electric | geel + zwart of blauw | bliksemvormen, staartbollen, wangvlekken, gekartelde punten | Pichu, Mareep, Shinx, Emolga, Yamper |
| Ice | lichtblauw, wit, lila | kristallen, ijspegels, sneeuwkragen, zesvoudige symmetrie | Snorunt, Spheal, Snom, Vanillite, Cubchoo |
| Fighting | rood, roodbruin, huidtinten, blauw-grijs, zwart-wit contrast | vuisten, handschoenen, tape, gordels, maskers, knotjes, wenkbrauwen, een klaarstaande houding | Riolu, Makuhita, Pancham, Hawlucha, Kubfu, Clobbopus, Stufful |
| Poison | paars, magenta, giftig groen | vlekken, druppels, stekels, gasbellen, bulten | Grimer, Ekans, Skrelp, Toxel, Shroodle |
| Ground | zandbruin, oker, aarde | schubben, graafklauwen, modder, botten | Sandshrew, Cubone, Mudbray, Hippopotas, Diglett |
| Flying | wit, hemelblauw + een vogelkleur | vleugels, veren, kuiven, staartwaaiers | Swablu, Pidgey, Rookidee, Wingull |
| Psychic | roze/magenta, violet, lavendel, goud, pastelblauw | ogen die iets onnatuurlijks doen, nadruk op het voorhoofd, symmetrie, frontaliteit, zweven of mediteren, sterren/manen/spiralen, edelstenen, lepels, parels | Abra, Espurr, Oranguru, Natu, Munna, Elgyem, Hatenna, Espeon |
| Bug | geelgroen, rood, oranje + zwart | segmenten, antennes, voelers, schildpatronen | Caterpie, Wurmple, Grubbin, Nymble |
| Rock | grijs, bruin, zandsteen | hoekige vormen, scheuren, kristallen, platen | Geodude, Roggenrola, Rockruff, Nacli |
| Ghost | paars, donkerblauw, grijs-wit | zweven, transparantie, rafelranden, één oog, kaarsen, dekens | Gastly, Shuppet, Litwick, Sinistea, Greavard |
| Dragon | blauw, groen, rood + crème buik | hoorns, vinnen, schubben, oervormen, wiggenkoppen | Dratini, Bagon, Gible, Axew, Jangmo-o |
| Dark | zwart, antraciet, indigo, diep paars; warm-donker (roest, kastanje) alleen met zwart | **één gloeiend accent** (rood, geel, goud, magenta), meestal **op de ogen**; spleet- of halfgesloten ogen, gekleurde oogwitten, een scheve grijns of hoektand, maskers, sokken, puntige plukken, klauwen; kleding van een schurk (hoed, capuchon, cape) | Poochyena, Sneasel, Zorua, Nickit, Purrloin, Murkrow, Umbreon, Galar-Zigzagoon |
| Steel | zilvergrijs, blauwgrijs + een accent | platen, bouten, magneten, scherpe randen | Aron, Klink, Pawniard, Tinkatink |
| Fairy | roze, wit, pastel | strikjes, linten, harten, sterren, bloemen, zachte krullen | Flabébé, Swirlix, Hatenna, Impidimp (Dark/Fairy) |

**Nadruk voor de starters:**
- **Fighting** (Stufful/Bewear, Makuhita, Pancham, Riolu, Kubfu, Clobbopus): het type zit in **wat het lijf doet en draagt**. Handschoenen, tape of wanten uit het eigen lijf, kleurblokken als een uniform (gordel, mawashi, masker, mouwen), een knot of hoofdband, een **wenkbrauw in een V** en een **houding die klaarstaat**. Schattigheid blijft kan: een zacht lijf met één of twee harde signalen.
- **Dark** (Nickit/Thievul, Purrloin, Sneasel, Murkrow, Galar-Zigzagoon): het type zit in **palet + ogen + grijns**. Een donkere of zwart-gecontrasteerde basis, één gloeiend accent op de ogen, halfgesloten of schuine ogen, een scheve grijns, maskers, sokken en klauwen. Dieven sluipen en houden **buit** vast. Bewijs: Galar-Zigzagoon is hetzelfde dier als Zigzagoon, maar zwart-wit met rode ogen en een tong uit, en meteen Dark.
- **Psychic** (Abra, Espurr, Oranguru, Natu/Xatu, Elgyem, Hatenna): het type zit in **ogen + kop + stilte**. Dichte, lege, verborgen, patroon- of gloeiende ogen, een groot hoofd met een teken op het voorhoofd, een symmetrische en frontale houding die zweeft of mediteert, violet/roze/goud, en symbolen (manen, sterren, spiralen). Let op: de **nacht** is in Pokémon het terrein van Dark (Umbreon; Noctowl is in deze repo Flying/Dark). Een nachtelijke Psychic heeft dus extra Psychic-signalen nodig en mag geen zwart met geel of rood gebruiken, en geen tanden.

### Kleurstrategie
- Kies **2–3 hoofdkleuren** als grote egale vlakken en **één accent**. Het accent zit op het type-onderdeel (de vlam, de handschoen, de ogen), niet ergens willekeurig.
- Gebruik **of** een verzadigde typekleur als basis (gemeten: fase 1 van de starters heeft gemiddeld 0,54 verzadiging), **of** een neutrale basis (wit, grijs) met één fel accent in de typekleur (Scorbunny, Oshawott, Rowlet).
- Contrast in **helderheid** maakt het silhouet: een lichte basis met een donker accent, of omgekeerd. Ton-sur-ton (beige op crème) wordt een vlek.
- Een starterstrio vormt samen een **driehoek**: duidelijk verschillende tinten én helderheden, zodat ze naast elkaar in het keuzescherm niet op elkaar lijken.
- Een natuurlijke dierkleur mag, maar dan moet een ander middel het type dragen (het patroon, de ogen, kleding uit het eigen lijf).

### Checklist Pokémon-design (vóór stap 2 "Silhouet" van §3, en opnieuw bij de keuring in §6)
- [ ] **Dier × idee × type:** kan iemand zonder uitleg het dier, de rol én het type noemen? Test het op iemand die de tekst niet kent.
- [ ] **Type herkenbaar** volgens de tabel hierboven: minstens drie middelen van het type tegelijk (kleur + onderdeel + ogen/houding).
- [ ] **Een basisvorm** draagt het ontwerp; de anatomie is vereenvoudigd (geen realistische gewrichten, knieën of snuit).
- [ ] **Precies één iconisch, onrealistisch kenmerk** dat op 1× leesbaar is en het silhouet breekt.
- [ ] **Silhouettest:** zwart op 1× naast vergelijkbare Pokémon (`sprites/kritiek/grid.py`, groep "Silhouet"): niet te verwarren met een bestaande soort of een gewoon dier.
- [ ] **Kleur:** 2–3 hoofdkleuren + één accent; de basis is ofwel de typekleur, ofwel neutraal met een type-accent; voldoende helderheidscontrast.
- [ ] **Gezicht:** grote ogen met een glans plus een ooglid of wenkbrauw die de persoonlijkheid geeft; frame 2 is een karaktermoment.
- [ ] **Vooruitwijzing:** het zaadje van de eindvorm (kostuum, motief, kenmerk) zit al in fase 1, en elke fase heeft hetzelfde vaste kenmerk (zoals de klauwen of de spiraal).
- [ ] **Starters:** naast alle 27 starters van fase 1 (vel `sprites/kritiek/1_starters_gen1-9.png`) valt hij niet weg als "het dier zonder thema"; het trio vormt een kleurendriehoek.
- [ ] **Andere Pokémon van hetzelfde dier** (bijv. Wooloo/Mareep, Sentret/Zigzagoon, Oranguru) bekeken: wat doen die om Pokémon te worden, en wat doet de onze anders?
- [ ] **Gespriet, niet geïllustreerd:** egale vlakken, duidelijke schaduwvormen, geen textuurruis. Fluffy zit in de buitenrand.

---

## 0. Eerst weten: welke sprites zie je eigenlijk in de game?

Elke soort heeft twee sets in `graphics/pokemon/<soort>/`:

| bestand | wat het is | in de game? |
|---|---|---|
| `anim_front_gba.png`, `back_gba.png`, `normal_gba.pal`, `icon_gba.png` | de **originele GBA-sprites** (Ruby/Sapphire/Emerald, voor Kanto/Johto de FRLG/RSE-versies); alleen soort 1–386 | **nee**: alleen met `P_GBA_STYLE_SPECIES_GFX = TRUE` (`include/config/pokemon.h`) |
| `anim_front.png`, `back.png`, `normal.pal`, `icon.png` | wat expansion standaard toont: voor Gen 1–4 de **DPPt/HGSS-sprites**, voor Gen 5 de BW-sprites, Gen 6+ community-sprites in DS-stijl, allemaal teruggebracht naar 64×64 en 16 kleuren | **ja** |

Gevolgen:
- De **echte Gen 3-leidraad** zijn de `_gba`-bestanden. Die zijn het meest consistent en het best (zie §1).
- Wat de speler naast onze fakemon ziet, zijn de **in-game (DPPt-)sprites**: iets kleiner in het vak, donkerder (gemiddelde helderheid V 0,61 tegen 0,67), met meer zwarte omlijning (55% van de randpixels zwart tegen 43%) en bijna geen lichte rand aan de lichtkant (4% tegen 17%). Zie `1_starters_gba_vs_ingame.png` en `5_generaties.png`.
- Het ingebedde palet in `back.png` (huidige set) is vaak de **shiny**; lees altijd `normal.pal` / `normal_gba.pal`.
- De kleurvarianten (`variants.pal`) zijn gemaakt op de huidige set (`normal.pal`), niet op de GBA-set. Overschakelen naar de GBA-sprites zou alle Gen 1–3-recepten breken (andere indexvolgorde). Dat doen we dus niet.

**Voorstel (designkeuze voor Jordi):** we tekenen met de **constructie van de GBA-Hoenn-sprites** (pose, ramps, selective outlining, belichting), maar met het **contrast van de in-game sprites**: de rechter-/onderrand zwart, en de lichte rand aan de lichtkant iets zuiniger dan in Hoenn. Zo valt een fakemon niet op als "zachter" of "lichter" naast een Poochyena of Swablu in hetzelfde gras. De controle (`check.py`) meet beide; we kijken altijd met `compare.py` naast allebei.

---

## 1. De Hoenn-sprites: regels en kenmerken

### 1.1 Formaat, schaal en plaatsing
- Front: `anim_front.png` = **64×128**, twee frames van 64×64 onder elkaar. Back: 64×64. Icoon: 32×64 (twee frames van 32×32). Geïndexeerde PNG, **16 kleuren**, index 0 = transparant.
- **Grootte groeit met de evolutiefase** (bounding box van frame 1, mediaan [p10..p90]):

| | hoogte | breedte | oppervlak (pixels) | bovenrand y |
|---|---|---|---|---|
| fase 1 (en losse soorten) | 40 [30..58] | 42 [29..61] | ±910 [530..1670] | 11 |
| fase 2 | 52 [42..61] | 52 [37..62] | ±1440 [1020..2040] | 6 |
| fase 3 | 60 [46..63] | 62 [49..64] | ±1920 [1370..2500] | 2 |

  Een eindvorm is dus ±2× zo groot (in pixels) als zijn basisvorm. Starters: Treecko 48 hoog → Grovyle 56 → Sceptile 64 (raakt het hele vak), Torchic → Blaziken, Mudkip → Swampert idem.
  Kleinste Hoenn-sprites: Natu (358 px), Magnemite, Aron, Surskit, Luvdisc (±420); grootste: Tropius, Swampert, Walrein, Exploud, Hariyama (2400–2700).
- **Horizontaal gecentreerd** op x ≈ 31,5 (zwaartepunt 29..34). Voeten/onderkant meestal op y 47–62.
- De verticale plek in het vak maakt in de game niet uit: `frontPicYOffset` = **63 − onderste rij van frame 1** (voor alle 131 gecontroleerde soorten exact), en `backPicYOffset` = 63 − onderste rij van de back. Zwevende soorten krijgen daarnaast `enemyMonElevation` (Masquerain 10, Lunatone 13, Castform 16). `check.py` rekent deze waarden uit.
- Grote eindvormen en legendaries mogen het vak vullen en tegen de rand aan lopen (Sceptile, Groudon, Rayquaza); basisvormen nooit.

### 1.2 Palet en ramps
- **13 van de 15 kleuren gebruikt** (mediaan; p10..p90 11..15). Eindvormen gebruiken er vaker 14–15. Weinig kleuren (7–10) alleen bij simpele, eenkleurige soorten: Geodude, Baltoy, Abra, Muk, Regice.
- **Omlijning = één (bijna) zwarte kleur**: #101010 (83×) of #000000 (78×), soms #181818. Nooit een gekleurde donkere tint als "zwart". In de GBA-paletten staat ze bijna altijd op **index 15** (123 van 202; anders 14).
- **Paletvolgorde (GBA):** per ramp opeenvolgende indexen, **van licht naar donker** (Treecko: 1–3 oranje oog, 5–7 rode buik, 11–14 groen lijf licht→donker, 15 zwart). 80% van de buren in de palettabel hoort bij dezelfde ramp. Zie `3_paletten_starters.png`.
- **±3 ramps per sprite** (2..4), elk meestal **4 tinten** (3..7), plus één los **wit** (146 van 202 sprites hebben precies één wit, vrijwel altijd als oog-hooglicht). Sommige lichtste tinten worden gedeeld (wit lijf + oogglans).
- Gemeten ramp van 4 tinten, donker → licht (HSV):
  - **helderheid V: 0,48 → 0,71 → 0,87 → 1,00** (stappen van ±0,15);
  - **verzadiging S: 0,58 → 0,60 → 0,54 → 0,39** (de lichtste tint is bleker: pastel-hooglicht, nooit feller);
  - **tint:** gemiddeld ±3–9° per ramp richting geel aan de lichte kant (61% van de ramps), dus *subtiele* hue-shift. Duidelijkst bij blauw/groen: Mudkips schaduw #4a4a83 is violet tegen een lijf van #5aace6, Ralts' groen loopt van #317b4a (blauwgroen) naar #cdffac (geelgroen).
  - De **meest gebruikte tint is de op één na lichtste** (Treecko #9cd54a, Mudkip #5aace6); de lichtste is het hooglicht.
- **97% van de Hoenn-sprites heeft een tint met V = 1** (één kanaal op 255). Gemiddelde helderheid per pixel V ≈ 0,67. Dat is de GBA-look: het scherm van de GBA was donker, dus alles is licht en helder. (De in-game DPPt-set: V ≈ 0,61, maar 32% heeft een V = 1-tint.)
- Grijzen zijn neutraal of licht warm (Aggron: #6a6a6a/#8b8b8b/#acacac naast #bdacac/#decdcd), bruinen worden in de schaduw grijzer (Zigzagoon).
- Alle kleuren zijn 15-bit GBA-kleuren (waarde = `round(v/255·31)·255//31`, bijv. 255/213/197/180/164…).

### 1.3 Belichting
- **Licht van linksboven**, op front én back (regressie van tintrang tegen positie: dx −0,13, dy −0,17 mediaan; zie `2_omlijning_en_licht.png`). Schaduw rechtsonder en aan de onderkant van bollingen.
- ±40% van de vlakpixels zit in de donkere helft van zijn ramp, ±5% is echt hooglicht (de lichtste tint). Hooglichten zijn kleine vlekjes linksboven op bollingen (koppen, buiken), geen randlicht rondom.
- ±12% van de sprites wijkt in de meting af (licht meer van rechts of onder: Torchic, Swampert, Regirock); bij nadere blik zijn dat sprites met lichte vlakken rechts (vinnen, buik), niet ander licht. Regel: altijd linksboven.

### 1.4 Omlijning en lijnwerk (het belangrijkste verschil met andere generaties)
- **Selective outlining (selout):** de buitenlijn is aan de lichtkant gekleurd, aan de schaduwkant zwart.

  | rand | zwart | donker (zwart óf donkerste rampkleur) |
  |---|---|---|
  | boven | 21% | 39% |
  | links | 20% | 43% |
  | onder | 66% | 81% |
  | rechts | 63% | 79% |

  Aan de bovenkant/links is de lijn dus meestal de **donkerste of een middentint van de ramp eronder** (Torchic: bruinrood; Mudkip: donkerblauw-violet; Gardevoir: lichtgrijs op de jurk). Rechtsonder zwart. Over de hele rand: 43% zwart, 58% donker, 17% lichter dan V 0,45.
- Uitersten binnen Hoenn: bijna overal zwart (Treecko, Sceptile, Poochyena, Mightyena, Metagross, Baltoy: > 60%) tegenover bijna nergens zwart (Mudkip, Wurmple, Beautifly, Wingull, Swablu/Altaria, Milotic, Salamence, Wailord, Lunatone/Solrock: < 25%). Zachte, ronde, lichte of "luchtige" soorten krijgen de lichtste lijnen.
- **Lijndikte 1 px.** Een dubbele zwarte rand komt maar op 4% van de randpixels voor (onder voeten, onder de buik).
- **Binnenlijnen** zijn grotendeels niet zwart: maar ±4% van de binnenpixels is zwart (mond, diepe plooien, pupillen, scheiding van overlappende ledematen). Plooien, spieren en vachtlijnen zijn de donkerste rampkleur (Shroomish' gezicht, Zigzagoons strepen).
- **Anti-aliasing** spaarzaam: weinig losse pixels (±9 per sprite). Selout doet het werk van anti-aliasing; trappetjes in schuine lijnen zijn gelijkmatig (1-1-1 of 2-2-2), niet rommelig.

### 1.5 Dithering en textuur
- Schaakbord-dithering komt **sparzaam** voor: ±4,5% van de pixels (p10..p90 1,4..8,5%). Typisch als **overgangsband van één tot twee pixels** tussen twee tinten op een grote ronde vorm (Torchics kop, Mudkips staartvin, Treeckos staart) of als **textuur** op grote egale lijven (Wailord 14%, Magikarp 16%, Silcoon, Wailmer, Lunatone, Regirock, Sandshrew 10–12%).
- Geen dithering op kleine sprites als vervanging van een ramp; nooit over de omlijning.
- Vacht: getande silhouetranden en V-vormige plukken in twee tinten (Zigzagoon, Poochyena, Vigoroth), niet per haar getekend.

### 1.6 Ogen, mond en kleine details
- **Ogen:** zwart (of donkere iris) met **1 witte pixel glans** (kleine soorten: Mudkip 2×3 zwart + 1 wit; Torchic ±3×4 + 2×2 wit). Grotere/serieuzere soorten: gekleurde iris (geel/oranje/rood) met een zwarte pupil en zwarte rand (Treecko, Poochyena, Grovyle). Ogen zijn de plek waar zwart wél overal zit.
- Mond open in frame 2 komt veel voor; de binnenkant van de mond is een donkere eigen kleur (rood/roze ramp), tanden 1 px wit.
- Klauwen/tenen: 1–2 px, licht (wit/beige) met zwarte buitenrand (Combusken, Absol). Pootjes van kleine soorten zijn 2–3 px brede stompjes met één schaduwpixel.
- Zie `heads`-crops in de scratchmap of zoom zelf met `contact.py --zoom 6`.

### 1.7 Pose en perspectief
- **Driekwartaanzicht, kijkt naar links** (naar de speler linksonder). Lijf iets gedraaid, verste ledematen donkerder en kleiner. Een minderheid staat recht van voren (Whismur, Loudred, Makuhita, Abra, Shroomish): ronde of "frontale" ontwerpen.
- Houding met energie: armen uit (Treecko), gebogen knieën, staart of vleugel als tegengewicht. Lange lichamen diagonaal door het vak (Linoone, Seviper, Gyarados, Rayquaza).
- **Frame 2 (Emerald-animatie) is een actiepose**, geen verschoven kopie: in 163 van 200 sprites verschilt na de beste verschuiving nog > 40% van de pixels. Typisch: bek open (Poochyena, Mightyena, Lombre, Taillow), armen omhoog (Treecko, Nuzleaf, Hariyama), vleugels omhoog (Taillow, Pelipper), sprongetje omhoog (Mudkip), ogen dicht/blij (Whismur), andere kopstand (Geodude). Alleen vormloze soorten bewegen bijna niet (Slakoth, Silcoon, Cascoon, Shelgon). Het silhouet blijft ongeveer even groot (hoogte en breedte mediaan gelijk, ±5 px); de voeten blijven meestal op dezelfde rij. Zie `4_frames_en_back.png`.
- In `species_info` wisselen de frames via `.frontAnimFrames` (`ANIMCMD_FRAME(0, n)`/`(1, n)`) plus een `.frontAnimId` (bijv. `ANIM_V_SQUISH_AND_BOUNCE`).

### 1.8 De achterkant (back)
- Van achteren-linksboven gezien, het lijf naar rechtsboven gericht; de kop is vaak in profiel gedraaid zodat **één oog zichtbaar** blijft (Treecko, Ralts, Zigzagoon, Aron, Linoone).
- **Groter dan de front:** ±1,14× zo breed en ongeveer even hoog, want de onderkant is **recht afgesneden**: bij 82% van de backs is de onderste rij voor meer dan de helft gevuld (de rest valt achter het tekstvak). Die snijlijn heeft **geen** zwarte omlijning.
- Zelfde licht (linksboven) en dezelfde selout als de front. Bovenrug en kop krijgen de meeste details; de afgesneden onderkant is egaal.

### 1.9 Iconen
- 32×32, twee frames; de figuur is ±20×20 px (16..26) met de onderkant op **y = 29**.
- Frame 2 = **1 px lager/ingedrukt** met kleine wijzigingen aan poten/kop (90 van 202: precies 1 px verschoven plus wijziging; verder ±1 px opzij).
- Max. ±8 kleuren uit **één van de 6 gedeelde icoonpaletten** (`graphics/pokemon/icon_palettes/pal0-5.pal`, `.iconPalIndex`); omlijning in het donkergrijs van dat palet. Grote kop, vereenvoudigd tot 2 tinten per kleur, zelfde kijkrichting als de front. Zie `6_iconen.png`.

### 1.10 Evolutielijnen
- Wat blijft van fase 1 naar 3: **kleurschema en de verdeling ervan** (Treecko-groen met rode buik → Sceptile met rode buikband en gele zaden in een nieuwe kleur), **de ogen** (vorm en kleur), één **signatuurvorm** die groeit (Mudkips kopvin → Marshtomps → Swamperts twee vinnen; Torchics kuif → Blazikens kuif), en het palet loopt grotendeels door (zelfde ramps, één extra ramp voor een nieuw onderdeel).
- Wat verandert: proporties (kop van ±40% van de hoogte naar ±25%), houding (van gedrongen en rond naar hoekig en dynamisch), meer kleuren en meer binnenlijnen.

### 1.11 Waar Hoenn zelf niet consistent is
- Omlijning: zwarte lijnen rondom (Treecko, Poochyena, Metagross) naast bijna lijnloze sprites (Mudkip, Swablu, Wailord) zonder duidelijke regel per type.
- Kleuraantal: 7 (Geodude, Baltoy) tot 15.
- Dithering: van 0 (Ralts) tot 16% (Magikarp).
- Transparante kleur verschilt per sprite (paars bij Treecko/Sceptile, groen bij de rest): onbelangrijk, maar kies er één vaste.
- Paletvolgorde: meestal licht→donker per ramp, soms door elkaar (Treecko's staart).
- Zwart is #000000 óf #101010.
- Enkele sprites zijn recht van voren of plat van opzij (Linoone, Wailord) in plaats van driekwart.
Voor ons: kies binnen deze spreiding bewust per soort, maar houd een lijn binnen één evolutielijn gelijk.

### 1.12 Doen / nooit
Doen:
- 1 px omlijning, rechtsonder zwart, linksboven gekleurd (selout).
- Licht linksboven, ramps van 3–5 (meestal 4) tinten, de lichtste met V ≈ 1 en lagere verzadiging.
- Eén vaste near-black (#101010) op index 15; ramps licht→donker op opeenvolgende indexen.
- Driekwart, naar links, met energie in de pose; frame 2 als duidelijke actiepose.
- Grootte volgens fase (§1.1); 1 px marge rondom bij basisvormen.
- Ogen met 1 px witte glans.

Nooit:
- Zwarte binnenlijnen voor elke plooi ("kleurboek"-look); pillow shading (licht in het midden, donker rondom); hooglichten aan de rechterkant.
- Gradients met 8 tinten of dithering als hoofdschaduw; dithering over de omlijning of op kleine vormen.
- Een tweede donker-zwart naast index 15; gekleurde "bijna-zwarten" als omlijning.
- Een basisvorm die het vak vult, of een eindvorm van 40 px hoog.
- Frame 2 = frame 1 een pixel verschoven (alleen bij vormloze soorten).
- Kleuren die op de GBA wegvallen: hooglicht onder V 0,9 bij een licht lijf, of een schaduw boven V 0,6 (geen contrast).

---

## 2. Andere generaties: wat ze anders doen en wanneer afwijken mag

Gemeten op de in-game set (`anim_front.png`/`front.png`), mediaan per generatie:

| | zwart aan de rand | donkere rand | lichte rand (selout) | licht dx/dy | dithering |
|---|---|---|---|---|---|
| Hoenn GBA | 43% | 58% | 17% | −0,13/−0,17 | 4,5% |
| Gen 1 (in-game) | 47% | 74% | 6% | −0,09/−0,10 | 4,2% |
| Gen 3 (in-game) | 58% | 75% | 4% | −0,13/−0,21 | 3,8% |
| Gen 4 | 50% | 83% | 2% | −0,07/−0,22 | 4,0% |
| Gen 5 | 49% | 86% | 0,5% | −0,05/−0,11 | 3,5% |
| Gen 6–8 | 51–54% | 78–86% | 0% | ±0/−0,09..−0,19 | 3,6–4,1% |
| Gen 9 (1 frame) | 51% | 78% | 0,5% | −0,03/−0,16 | 4,3% |

- **Gen 4/5:** donkere omlijning bijna rondom, licht meer van boven dan van links, iets donkerder en verzadigder. Gen 5 staat vaker stijf recht van voren.
- **Gen 6–9 (community-sprites in DS-stijl):** geen lichte selout meer, licht vrijwel recht van boven, poses frontaler; Gen 8+ heeft vaak ruizige schaduw zonder nette ramps (dat merkten we al bij de kleurvarianten). Gen 9 heeft maar één frame.
- **FRLG/RSE-Kanto (`_gba` van Gen 1–2)** volgt dezelfde regels als Hoenn: bruikbaar als extra Gen 3-referentie (Bulbasaur, Charmander, Growlithe, Dratini).

Wanneer afwijken mag:
- **Donkerdere/zwartere omlijning** (richting Gen 4): mag, en is zelfs aan te raden voor donkere, hoekige of "gevaarlijke" soorten, en overal aan de rechter-/onderkant (in-game-contrast, zie §0).
- **Frontaal aanzicht** (Gen 5): alleen voor ronde, symmetrische of totemachtige ontwerpen (zoals Hoenn ook doet bij Whismur/Baltoy).
- **Meer textuur/dithering**: voor steen, wol, nevel en grote egale lijven.
- **Niet** afwijken in: lichtrichting, 1 px lijnen, aantal tinten per ramp, het formaat per fase, twee frames.

---

## 3. Werkwijze: een fakemon maken

Elke stap levert iets op dat we kunnen tonen; Jordi keurt op stap 2 (silhouet) en stap 9 (eindresultaat), niet tussendoor op elke pixel.

1. **Idee en referenties** (`POKEMON.md`): inspiratie, type(s), fase, grootte in de wereld, 2–3 echte foto's en 3 Hoenn-sprites van vergelijkbare bouw als "stijlbuur" (bijv. een lama → Mightyena voor de poten/vacht, Absol voor de kop, Camerupt voor de massa).
2. **Silhouet** (zwart op transparant, 64×64): de vorm moet op 1x herkenbaar zijn. Grootte volgens §1.1 (fase 1 ±40 hoog, fase 2 ±52, fase 3 ±60). Driekwart, naar links, voeten op één rij, zwaartepunt x ≈ 32. Maak 2–3 varianten en vergelijk ze met `compare.py` op 1x naast de buren; voor een lijn alle fases naast elkaar. → *Jordi kiest.*
3. **Kleurgroepen en palet** (zie ook §5): bepaal de onderdelen (lijf, buik, vacht, accent, ogen, …), elk een eigen ramp. Maak het palet met `ramp.py` (basis = de meest voorkomende tint; 4 tinten; index 15 = #101010; wit los). Budget: 14 kleuren + omlijning. Typisch: lijf 4, tweede kleur 4, accent 3, oog/mond 2, wit 1.
4. **Vlakken inkleuren** met de basistint per onderdeel (nog geen schaduw). Kijk of de kleurverdeling klopt (wat is groot, wat accent).
5. **Lijnwerk:** 1 px buitenlijn zwart; daarna selout: aan boven- en linkerkant de zwarte pixels vervangen door de donkerste (of op heel lichte delen de op één na donkerste) tint van het vlak eronder. Binnenlijnen alleen waar delen overlappen; plooien in de donkerste rampkleur.
6. **Belichting:** licht linksboven. Schaduw (tint 2 en 1 van onder) rechtsonder en onder elke bolling; ±40% van het vlak in schaduw, hooglicht klein (±5%) linksboven op kop/buik. Verste ledematen een tint donkerder. Dithering alleen als 1–2 px overgang op grote ronde vlakken of als textuur.
7. **Details:** ogen (zwart + 1 witte glans, of iris + pupil bij grotere soorten), tanden/klauwen 1–2 px, vacht als getande rand in twee tinten. Op 1x controleren: valt een detail weg, dan vergroten of schrappen.
8. **Frame 2:** een actiepose in hetzelfde silhouetformaat (bek open, kop omhoog, poot geheven, oren/staart omhoog). Zelfde palet, voeten op dezelfde rij tenzij hij springt.
9. **Back:** kop/rug van linksachter, kop in profiel met één oog, ±1,15× de breedte van de front, onderkant recht afgesneden (geen lijn aan de snede), zelfde licht. → **Icoon:** vereenvoudigde front (kop groot), ±20×20, onderkant y 29, tweede frame 1 px lager, kleuren uit het best passende icoonpalet (0–5).
10. **Controle en keuring:** `check.py <map> --stage N` (moet zonder FOUT; elke LET OP bewust), `compare.py` (naast Hoenn-GBA en in-game buren), dan pas naar Jordi (zie §6). Na akkoord: in de game zetten (`species_info`-waarden staan in de uitvoer van `check.py`; zie de les "Nieuwe vorm" in CLAUDE.md voor de rest) en een gevecht-screenshot maken.

**Eén lijn tegelijk tekenen**, niet één sprite: eerst alle silhouetten van de lijn, dan de paletten samen (doorlopende ramps), dan alles uitwerken.

### Hulpscripts
Al gemaakt (`tools/concept/sprites/`):
- `spritelib.py` – laden (GBA- en in-game-set, juiste `normal*.pal`), Hoenn-soortenlijst, randmaskers.
- `contact.py` – contactvel op schaal (kolommen GBA/in-game front f1/f2, back, icoon; `soort=pad.png` voor eigen sprites; `--grid` 8×8-raster).
- `measure.py` + `summary.py` – alle metingen uit dit document per soort naar CSV en samenvatting (`--hoenn`, `--all`, `--set gba|new`).
- `ramp.py` – palet-/rampgenerator, gekalibreerd op de Hoenn-ramps (getest op Treecko en Mudkip: de midden- en lichte tinten komen op 1–2 GBA-stappen na overeen; de donkerste tint is in Hoenn vaak sterker naar violet/grijs verschoven en moet je met de hand bijstellen, bijv. `--hue 8`), schrijft JASC-`.pal` + stalenvel.
- `check.py` – regelcontrole (formaat, 16 kleuren, palet front=back, zwarte omlijning op 15, 15-bit-kleuren, randen, V=1-hooglicht, icoonpalet) en vergelijking met de Hoenn-spreiding per fase (grootte, selout per kant, lichtrichting, schaduw, dithering, losse pixels, framewissel); geeft `frontPicYOffset`, `backPicYOffset` en `*PicSize`.
- `compare.py` – vel met de nieuwe sprite naast de Hoenn-sprites van dezelfde fase en grootte (GBA en in-game), vergroot én op 1x.
Bestaand en bruikbaar: `tools/grounded/variants/ramps.py --grid` (indexkaart: welke index waar staat), `zoom.py`, `sheet.py` (varianten).

Nog te bouwen (wanneer nodig):
- `selout.py`: zet zwarte randpixels boven/links automatisch om naar de donkerste tint van de buur (eerste versie, daarna met de hand bijwerken).
- `back_from_front.py`: hulp voor de back (spiegelen, 1,15× vergroten met Scale2x→verkleinen, afsnijden op y ±56) als ondergrond om overheen te tekenen; nooit als eindresultaat.
- `icon_from_front.py`: verkleinen naar ±20 px + mappen op het dichtstbijzijnde icoonpalet, als ondergrond.
- `battle_mock.py`: front en back op een gevechtsachtergrond in 240×160 (sneller dan een test-ROM voor de eerste blik).

---

## 4. Werkwijze: regional forms

Bekijk eerst hoe de echte regionale vormen en onze eigen Hoenn-Grimer het doen (`contact.py ... --cols nf1,nf2,nb grimer grimer/hoenn vulpix vulpix/alola meowth meowth/galar zigzagoon zigzagoon/galar growlithe growlithe/hisui`):
- **Behouden:** de pose en het skelet (vaak letterlijk dezelfde houding: Galar-Zigzagoon, Hisui-Growlithe, Hoenn-Grimer), de **ogen en het gezicht**, de verhoudingen en de grootte in het vak, het tweede frame (zelfde beweging).
- **Veranderen:** het palet volledig (ander kleurverhaal dat bij het nieuwe type en de plek past), en 1–3 **silhouetonderdelen** die het nieuwe type vertellen (Hisui-Growlithe: rotshelm; Alola-Vulpix: krullen; Galar-Zigzagoon: rechtopstaande punk-kuif; Hoenn-Grimer: draaikolk-punt). Die onderdelen moeten op 1x aan het silhouet te zien zijn.
- **Herkenbaar blijven:** wie de basisvorm kent, moet hem op 1x in het gras herkennen. Toets: zet de vorm naast de basisvorm in `compare.py --with <basisvorm>`; het silhouet moet grotendeels gelijk zijn, alleen de 1–3 nieuwe onderdelen steken eruit.

Stappen:
1. Basis: kopieer de **in-game** sprite (`anim_front.png`, `back.png`, `normal.pal`) van de basisvorm naar een eigen map (`graphics/pokemon/<soort>/<regio>/`). De in-game set, omdat de speler de basisvorm zo kent en de varianten daarop aansluiten. De GBA-versie ernaast leggen als stijlreferentie.
2. Indexkaart maken (`ramps.py --grid`) en vaststellen welke indexen welk onderdeel zijn; onderdelen die een index delen eerst splitsen (zie §5).
3. Nieuwe onderdelen tekenen met de regels uit §1 (selout, licht linksboven), in de bestaande indexen van het lijf waar ze erin opgaan (les "Pokémon-sprites aanpassen" in CLAUDE.md: geen omlijning tegen het lijf, dezelfde breedte als het hoofd).
4. Nieuw palet met `ramp.py`, frame 2 en back meenemen (elke wijziging op alle drie), icoon aanpassen.
5. `check.py` + `compare.py --with <basisvorm>`; keuring.
Het Venomoth-ontwerp dat al bestaat (`POKEMON.md`) volgt dezelfde controle zodra de bestanden in de repo staan.

---

## 5. De 8 paletten: indexen indelen voor de varianten

Elke soort krijgt uiteindelijk normaal + 6 varianten + shiny. Varianten zijn **paletwissels per kleurgroep** (`tools/grounded/variants/`: een recept zegt per onderdeel welke indexen erbij horen en welke doelkleur de meest gebruikte index krijgt). Wat bij de bestaande sprites telkens misging (KEURING.md, AGENT_BRIEF.md), lossen we bij het tekenen al op:

1. **Eén onderdeel = een eigen, aaneengesloten reeks indexen** (licht→donker). Nooit één index voor twee onderdelen die apart moeten kunnen kleuren (Grovyles bladeren deelden een index met het lijf; Magikarps oogwit met de vinnen; Spinda's spiraalogen met de oren). Dus: oogwit ≠ wit lijf, mondbinnenkant ≠ wangen, klauwen ≠ tanden als het lijf wit kan worden.
2. **Index 15 = alleen de omlijning** (en zwarte pupillen/mondlijnen). Zo blijft ze in elke variant zwart en vallen lijnen nooit weg. Gekleurde omlijning (selout) gebruikt de donkerste tint van het eigen onderdeel, zodat ze automatisch meekleurt.
3. **De meest gebruikte tint van een onderdeel is de basistint** (op één na lichtste), niet de schaduw. Dan werkt de variantgenerator zonder `'_base'`-uitzonderingen en worden albino/witte varianten niet bleek.
4. **Kleine accenten krijgen 2–3 eigen tinten** (oog, neus, snavel, zaden, vlam) in plaats van een lichte tint van een andere ramp te lenen; Jordi wil dat álles meekleurt.
5. **Ogen een eigen groep** (iris/pupil apart van het lijf), zodat een variant gekleurde ogen kan krijgen.
6. **Contrast per ramp ruim** (V-stappen ±0,15): bij een witte of zwarte variant moeten de tinten nog uit elkaar te houden zijn.
7. **Budget:** omlijning 1 + wit 1 + 13 voor ramps, bijv. lijf 4, buik/tweede kleur 3–4, accent 3, oog 2. Liever een ramp van 3 dan een gedeelde index.
8. Schrijf de indexindeling meteen op als een `'species'`-dict in recept-formaat (`{'lijf': [1,2,3,4], 'buik': [5,6,7], ...}`) naast de sprite (bijv. als commentaar in `POKEMON.md` of een `parts.json` in de map); dan is het recept later alleen nog kleuren kiezen.

Voor nu maken we alleen het normale palet; shiny en varianten volgen per lijn als de sprites goedgekeurd zijn.

---

## 6. Keuring vóór Jordi en presentatie

Checklist (alles ja, anders eerst verbeteren):
- [ ] `check.py` zonder FOUT; elke LET OP heeft een reden.
- [ ] Silhouet op 1x herkenbaar; grootte past bij de fase (§1.1) en naast de rest van de lijn.
- [ ] Driekwart naar links (of bewust frontaal), voeten op één rij, 1 px marge bij basisvormen.
- [ ] Licht linksboven op front, frame 2 én back; geen pillow shading.
- [ ] Omlijning 1 px; rechtsonder zwart, linksboven selout; geen zwarte kleurboeklijnen binnenin.
- [ ] Ramps 3–5 tinten, lichtste V ≈ 1 met lagere verzadiging, schaduw iets naar violet/blauw; alles 15-bit.
- [ ] Ogen met glans; kleine details op 1x leesbaar of weggelaten.
- [ ] Dithering alleen als overgang/textuur, ≤ ±8% van het vlak.
- [ ] Frame 2 is een echte actiepose; back volgt §1.8; icoon volgt §1.9.
- [ ] Indexindeling volgens §5 (elk onderdeel eigen indexen, omlijning op 15, basis = op één na lichtste tint); getest met een snelle albino- en zwarte proefvariant (`sheet.py`) dat lijnen blijven staan.
- [ ] Naast de in-game buren niet merkbaar lichter/zachter (§0).

Presentatie aan Jordi (één vel per soort of lijn, niet per stap):
- `compare.py`-vel: de nieuwe sprite (f1, f2, back) op 3× naast 4–6 Hoenn-sprites van dezelfde fase en grootte, de in-game versies eronder, en alles op 1×.
- Ingezoomd (6×) met `contact.py --zoom 6 --grid` voor de details (Jordi wil inzoomen vóór iets in de game gaat).
- Bij een lijn: alle fases naast elkaar op dezelfde schaal.
- Na akkoord: één screenshot uit een testgevecht (front tegenover een bestaande back, en de eigen back tegenover een bestaande front).

---

## 7. Reproduceren

```
python3 tools/concept/sprites/measure.py /tmp/hoenn_gba.csv --set gba --hoenn
python3 tools/concept/sprites/measure.py /tmp/hoenn_new.csv --set new --hoenn
python3 tools/concept/sprites/summary.py /tmp/hoenn_gba.csv /tmp/hoenn_new.csv
python3 tools/concept/sprites/contact.py uit.png --zoom 3 treecko grovyle sceptile
python3 tools/concept/sprites/ramp.py pad/palet --ramp lijf=#9cd54a:4 --ramp buik=#d55239:3 --white
python3 tools/concept/sprites/check.py graphics/pokemon/<nieuw> --stage 1
python3 tools/concept/sprites/compare.py uit.png graphics/pokemon/<nieuw> --stage 1
```
Illustraties in `docs/concept/sprite_studie/`: 1 starters GBA vs in-game, 2 omlijning en licht (rand: zwart/donker/licht; vlak: schaduw/hooglicht), 3 GBA-paletten van de starters in indexvolgorde, 4 frame 1/2/back, 5 generaties naast elkaar, 6 iconen.
