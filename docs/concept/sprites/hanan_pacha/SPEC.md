# Hanan Pacha – condor-legendary (Fire/Flying)

Trio van de drie Inca-werelden (zie `docs/concept/POKEMON.md` → Legendaries). Wezen, geen godenbeeld (Jordi: "net als dat groudon een behemoth is en kyogre een leviathan"). Moet ogen als een box legendary.

## Jordi (27 nov, letterlijk)
- "condor fire/flying klinkt goed"
- "hij moet echt machtig zijn, vleugels gespreid, maar wel passend in een sprite, dus hij kan niet te horizontaal worden, mogelijk kunnen we de vleugels zo spreiden dat het bijna een soort zon vorm is, duidelijk condor hoofd, maar wel heroisch, kraag mee eens, zwart/wit/goud/vuur ook, maar hij moet wel echt shinen. Inca geometrie patroon op de vleugels gaat niet vertalen denk ik, geen vlammen"

## Voorstellen van Claude die Jordi aannam
- Witte halskraag van de condor als stralenkrans ("kraag mee eens").
- Kleuren zwart/wit/goud/vuur ("ook").

## Geschrapt
- Inca-geometrie op de vleugels, vlammen aan de slagpennen.

## Antwoorden (Jordi, 27 nov, letterlijk)
- Shinen: "b qua felheid en kleurgebruik, a is denk ik niet goed te spriten" (b = straalt uit als geheel, felste/opvallendste van het kwartet; geen metallic glans).
- Hoek: "driekwart naar links ja, maar wel dat je de hele vorm ziet".
- Vuur: "Vuur hoeft niet zichtbaar te zijn, vuur is ook niet in ho oh zichtbaar, of in arcanine".

## Rondes
- **r1** (`gemini/r1.png`, prompt v1). Jordi: "hij is te zwart wit, die kring klopt niet, de vleugels moeten de kring vormen, lijkt geen legendary, ook niet genoeg condor, bijna kalkoen achtig". (Gemini tekende een losse zwarte ring achter het lijf; blauwgrijze kop met lel = kalkoen.)
- Na r1 (meerkeuze, Jordi): kleur = "meer goud als hoofdkleur en warme vuurtinten erbij"; legendary = "alle drie" (sierlijke sierveren, massiever en groter, heroïsche houding).
- **r2** (`gemini/r2.png`, prompt v2). Jordi: "ik vind hem nog niet heel mooi, ondanks dat die nu wel doet wat we vragen".
  Daarna: "ja het is een combinatie van dingen, het is teveel ho oh, misschien toch teveel zwart nog (dat duidt in pokemon vaak op evil) de kop is klein en hangend, de kraag is teveel kalkoen denk ik en hij is niet trots en heroisch, misschien moet de staart wel niet alleen naar rechts maar ook naar links en tussen de klauwen"
- **r3** (`gemini/r3.png`, prompt v3). Jordi: "de kop heeft geen mooie kleur en wijkt teveel af, ik vind hem wel beter worden, behalve dat de veren in elkaar plakken en hij toch nog iets teveel ho oh is, misschien andere pose, maar dan komt het zon idee er nog niet goed uit, doe eens wat suggesties"
- Na r3 gekozen (Jordi): "ik neig ernaar nog wat wit/zwart in de vleugels te verwerken ook, niet dominant"; "K1, V1, H1, P1 klinkt goed" = K1 kop diep karmijnrood (warm rood uit de vleugels, rode kop van een mannetjescondor), V1 per vleugel 6–7 losse vingerpennen met ruimte ertussen, H1 witte vleugelband + donkere vingerpunten (goud blijft hoofdkleur), P1 vleugels schuin omhoog in een brede V, vingerpennen waaieren uit als zonnestralen (geen gesloten ring).
- **r4** (`gemini/r4.png`, prompt v4). Jordi: "beter, maar hij is nog net niet majestueus genoeg. ik denk dat hem dat in versiering zit nog, misschien de staart of iets anders, doe suggesties"
- Na r4 (Jordi): "ik weet het al. Dit plaatje de staartveren, zoiets moeten we ook doen" (`referentie/staart_hanan_pacha_art.png`: frontale condor-illustratie; staart = waaier van ±9 lange, smalle, puntige losse veren die recht omlaag hangen onder het lijf, tussen en achter de klauwen, elk met een duidelijke schacht). Jordi daarna: "de vorm en waar ze heen gaan he" (alleen vorm en richting van de veren overnemen, geen binnentekening). Daarna: "k-a mag je ook proberen" (kroonkam). Mantel en gelaagde dekveren niet gekozen.
- **r5** (`gemini/r5.png`, prompt v6). Jordi: "nu is die goed, maar nu is de pose te horizontaal". Volgende stap: bijsturen in hetzelfde gesprek, alleen de vleugels steiler (`gemini/BIJSTUUR_r5.md`).
- **r6_bijstuur** (`gemini/r6_bijstuur.png`): bijsturen "vleugels steiler" veranderde bijna niets (6 % pixels anders). Jordi: "niet beter he"; "misschien nog 1 laatste prompt met de juiste vleugel pose?" → prompt v7 (v6 + steile V + vierkant formaat; r1/r2/r5 waren 1408×768, r3/r4 1024×1024). Daarna: "iets meer weer de zon vorm?" → in v7 stralen pennen en staart samen rond uit.
- **r7** (`gemini/r7.png`, prompt v7, 1024×1024). Jordi: "pose is goed, maar de kleuren zijn minder mooi dan de vorige versie, maar dat kan je wel fixen toch?" → model = pose r7 + kleuren r5.
- Na r7 (Jordi, meerkeuze): kleuren van r5 = "1, 2 en 3" (goudtint r5 op lijf en vleugels; vingerpennen als r5: wit → oranje → karmijnrood → donkere punt; kop- en kamkleur r5). Staart: "ze zijn wat te dun de veren, dus staart van r5 maar kleuren van r7" (r7-staart: goud met zwarte punten).
- **Model vorm v1** (`model/model_vorm_v1.png`): r7 met alles onder y=705 vervangen door r5 vanaf y=505 (poten + staart, dx −225, geplakt, niets hertekend). Kleuren nog r7 (staart nog r5-kleuren); kleurwerk volgt.
  Jordi: "slecht knip en plak werk" (harde horizontale naad, stukjes r5-lijf, kleine r5-poten onder het r7-lijf, ander goud). Volgende stap: staart bijsturen in het r7-gesprek (`gemini/BIJSTUUR_r7_staart.md`).
- Jordi: "je kan ook gewoon de sprite gaan bouwen en dan in de sprite gaan kijken naar de staart ipv half knippen en plakken"; "eerst kijken of het laatste model werkt en anders kan je daarna r5 gebruiken voor de staart". → Sprite r1 = r7 overgenomen (staart r7), kleuren uit r5 (punten 1–3); staart pas daarna beoordelen.
- **Sprite r1** (`sprite_r1/`, maker): r7 verkleind (natief 160 px, ×2,44 → 56×64), kleuren r5; pennen en staartveren 1–2 px breed → streperig. Nog niet gekeurd; naar Jordi voor de staartvraag ("eerst kijken of het laatste model werkt").
- Jordi na r1: "eens met dat de staart niet werkt"; "de kop is aan de kleine kant ook" "waardoor het oog maar 2 pixels is". → r2: staart van r5 in r7-kleuren, kop uit het model geschaald (×1,2/×1,35/×1,5 ter keuze), oog 1-op-1 van een Gen 3-vogel; pennen: banden r5 langs de lengte (voorstel Claude).
- Jordi: "de vleugels vind ik wel goed gelukt, alleen moeten nog meer kleurtinten en schaduw krijgen" → pennen-voorstel van Claude vervalt; vleugels vorm/kleurvolgorde bevroren, meer tinten + Gen 3-schaduw.
- Jordi: "ja het is niet erg dat de kop dan meer vleugel overlapt".
- Jordi: "en schaal de halsband mee" (kop + kraag samen schalen).
- **Sprite r2** (`sprite_r2/`): staart r5 (donkere punten), vleugels meer tinten (silhouet = r1), kop+kraag ×1,2/×1,35/×1,5 met oog Spearow/Pidgeot/Pidgeot. Snavel leest slecht (over de witte band), staart leest als massa.
- Jordi over r1/r2: "het is pixelblur" ("allebei"); "het hoofd leest amper nog als een condor hoofdd en de staart is wel prima, maar de binnenkant is blurry en de poten zijn niet meer herkenbaar"; "kijk anders naar hoe de legendary birds en ho oh het doen". → r3 (verse maker): natief raster, exacte 2× met regels, schrappen naar 64 met kop/kraag beschermd (Gengas/Krassault), staart r5-vorm scherp, studie Articuno/Zapdos/Moltres/Ho-Oh.
- Jordi: "ja de vormen zijn belangrijker dan welke kleur dominant is" (reductie: vormgrenzen gaan voor de dominante kleur).
- Jordi: "en overlappen is niet erg, zolang de voorste vorm maar goed gedefinieerd is".
- **Sprite r3** (`sprite_r3/`, verse maker): natief → 2× met regels → schrappen (kop/kraag beschermd), r5-staart, studie Ho-Oh/Moltres. Scherp; kop ±11×12 px, poten en staart nog zwak.
