# Vormstudie: wat maakt een sprite herkenbaar Pokémon? (23 okt)

Aanleiding: onze fakemon-sprites zijn goed in shading en kleur, maar zwak in **vorm, pose, plaats van ledematen en kenmerk**. Daar gingen 15+ rondes per sprite aan op. Deze studie zoekt de **verbanden** die over honderden echte sprites terugkomen ("als X, dan doen Pokémon vrijwel altijd Y"), zodat een sprite-agent ze op een nieuwe fakemon kan toepassen. De toetsbare versie staat in `docs/lessen/FAKEMON_CHECKLIST.md`.

Jordi: "de sprites hoeven niet altijd precies zoals de eerste 386 te zijn, maar het moet wel duidelijk een Pokémon zijn." Daarom is alles getoetst op **Gen 1–3 (Emerald-originelen, `anim_front_gba.png`)** én **Gen 4–9 (de expansion-sprites in Gen 3-stijl)**. Wat in beide groepen geldt, is een Pokémon-principe; wat verschilt, is speelruimte.

## Materiaal en meetmethode
- Bron: alle 1024 front-sprites in `graphics/pokemon/` (386 Gen 3-originelen + 638 Gen 4–9; frame 1, transparant = paletindex 0). Niets uit git nodig: vrijwel alles staat nog in de repo.
- `metingen.csv`: per soort bounding box, oppervlak (px), vulling van de box, **soliditeit** (oppervlak / convex omhulsel; laag = veel negatieve ruimte), **symmetrie** (beste overlap van het silhouet met zijn spiegelbeeld; hoog = frontaal), ingesloten gaten, evolutiefase (uit `species_info`).
- `vellen/`: contactvellen per bouwtype op 1× en 2× (`01_…`–`16_…`, getal = oppervlak), uitvergrotingen (`z_*.png`) en onze sprites naast vergelijkbare echte (`c_*.png`, `z_ons.png`).
- `tools/`: `lib.py` (laden/meten), `sheet.py` (vellen), `zoom.py` (uitvergroting, ook met eigen sprites via `paths`), `shape.py`, `metrics_all.py`. Draai ze vanuit een scratchpad-map (ze schrijven naar `sheets/` en `metrics*.json` in de huidige map).

## Kerncijfers

| Groep | n | oppervlak (mediaan) | box b×h | soliditeit | symmetrie |
|---|---|---|---|---|---|
| Gen 1–3 alle | 386 | 1201 | 48×47 | 0,75 | 0,64 |
| Gen 4–9 alle | 638 | 1340 | 50×52 | 0,73 | 0,62 |
| Fase 1 van een lijn (Gen 1–3 / 4–9) | 131 / 160 | **805 / 807** | 39×37 / 38×40 | 0,76 | 0,65 |
| Fase 2 van een lijn | 136 / 166 | 1394 / 1552 | 52×51 / 53×54 | 0,74 | 0,63 |
| Fase 3 | 44 / 56 | 1906 / 1802 | 58×56 / 62×61 | 0,72 | 0,62 |
| Starters fase 1 / 2 / 3 (alle gens) | 24 elk | **798 / 1226 / 2082** | 36×40 / 47×51 / 62×63 | 0,75 / 0,69 / 0,68 | 0,65 / 0,54 / 0,60 |
| Baby's (Pichu, Cleffa, Happiny…) | – | 450–700 | ±30×32 | – | – |

Per bouwtype (vellen 01–16, mediaan): kleine viervoeter 893 px, soliditeit 0,79; grote viervoeter 1554, 0,66; kleine tweevoeter 824, 0,75; grote tweevoeter 1601, 0,66; vogels 949, 0,69; slang/vis 1236, 0,76; **bol/blob 884, 0,83, symmetrie 0,78**; insecten 1154, 0,72; apen 1375, 0,72; Psychic/Dark/Ghost 1069, symmetrie 0,67.

Wat dit zegt:
- **Fase 1 is in alle generaties even groot (±805 px)**: dat is een vaste Pokémon-maat, geen Gen 3-eigenaardigheid. Fase 2 ≈ 1,7×, fase 3 ≈ 2,3–2,6× (starters 1 : 1,5 : 2,6).
- **Ongeveer een kwart van het omhulsel is lucht** (soliditeit ±0,75) en hoe groter/later de vorm, hoe meer lucht (0,76 → 0,72): grote vormen spreiden ledematen, staart en vleugels uit.
- **Bijna geen sprite is symmetrisch** (mediaan 0,63; alleen blobs komen rond 0,8). Ook frontale soorten zijn scheef gezet.
- Wat tussen generaties verschuift (speelruimte): Gen 4–9 heeft een donkerdere omlijning (aandeel zeer donkere pixels mediaan 0,20 tegen 0,13), losse soorten zijn iets groter (1544 tegen 1427), en schattige soorten (Gen 7–9-starters, baby's) hebben vaker een frontaal gezicht. De vormwetten hieronder gelden in beide groepen.

## De verbanden (als X, dan Y)
H = geldt voor vrijwel alle Pokémon (harde eis); R = richtlijn (meestal, met bekende uitzonderingen).

### Kop en gezicht
1. **(H) De kop draait meer naar de kijker dan het lijf.** Lijf 3/4 tot bijna profiel, kop 3/4 tot bijna frontaal. Zie Growlithe, Eevee, Vulpix, Meowth, Shinx, Lillipup, Lycanroc, Liepard, Pikachu, Chimchar. Waarom: het gezicht maakt contact met de speler, het lijf geeft richting en ruimte. Onze fout: kop én lijf in hetzelfde vlak (olinguito: beide profiel; nachtaap: beide frontaal).
2. **(H) Snuitlengte bepaalt het aantal ogen.**
   - Lange snuit (steekt duidelijk voorbij het oog, ±⅓ van de koplengte of meer) → kop meer profiel-3/4, **één oog** in beeld, neus is het meest linkse punt van de kop, de snuit wijst schuin naar links-onder. Zie Poochyena, Mightyena, Houndour, Electrike, Rhyhorn, Ponyta, Mudbray, Nickit, Cyndaquil, Charmander, Squirtle, Treecko, Torchic (snavel).
   - Korte of platte snuit → **twee ogen**, de neus **tussen en net onder de ogen**, iets links van het kopmidden. Zie Growlithe, Eevee, Shinx, Lillipup, Rockruff, Fennekin, Skitty, Meowth, Teddiursa, Mudkip, Bulbasaur, Chikorita.
   - Nooit allebei: twee ogen naast elkaar op een lange profielsnuit leest als "profiel met bril" (onze olinguito ronde 18).
   - Op vel 01 (28 kleine viervoeters): ±9 met één oog, allemaal met lange snuit; ±18 met twee ogen, allemaal met korte snuit.
3. **(H) Bij twee ogen is het verre oog kleiner/smaller en zit het dichter tegen de kopomtrek; de middellijn van het gezicht (neus, mond) ligt links van het kopmidden.** Zelfs bollen doen dit: Jigglypuff, Voltorb, Clefairy, Whismur en Togepi hebben hun gezicht links van het midden. Gelijke ogen op gelijke hoogte rond het midden = frontaal (onze nachtaap, Cuyby met symmetrie 0,94; blobs hebben 0,78).
4. **(R) De oren volgen de kopdraai:** het verre oor staat hoger/achter en is deels bedekt, of steekt anders uit dan het nabije (Poochyena, Eevee, Teddiursa, Lillipup). Twee identieke oren op gelijke hoogte = frontaal.
5. **(H) De kop overlapt het lijf.** Bij kleine soorten valt de nek weg en zit de kop vóór de borst/schouder (Eevee, Growlithe, Vulpix, Poochyena). Bij langnekken (Girafarig, Farigiraf, Ponyta) loopt de nek schuin naar voren en taps toe, de kop zit er schuin op. Een kop die los boven een verticale nekzuil zweeft leest als speelgoed (alpaca).

### Compositie en kenmerk
6. **(H) Diagonale compositie: kop linksboven, de massa loopt naar rechtsonder, een staart/kenmerk geeft tegenwicht rechts(boven).** Zie Growlithe, Vulpix, Cyndaquil (vlam), Skitty, Meowth, Luxray, Absol, Liepard, Pachirisu, Sentret, Furret, Charmander. Vrijwel elke sprite kijkt naar links(-voor); rechtskijkers bestaan (Houndour), maar wij houden links aan.
7. **(H) Eén dominant kenmerk steekt uit het silhouet**, meestal aan de achter- of bovenkant (vlam van Cyndaquil, staart van Vulpix/Sentret/Aipom/Skitty, blad van Chikorita, vin van Mudkip, kraag en oren van Eevee, schild van Squirtle). Het kenmerk zit niet ín de romp maar breekt de omtrek, en is op 1× als vorm te lezen. Accessoires (handschoenen, sjaals) zijn hooguit het tweede kenmerk.
8. **(H) Negatieve ruimte:** lucht tussen de poten, tussen staart en lijf, tussen arm en romp. Soliditeit ±0,75 (kleine viervoeter 0,79, grote 0,66). Alleen bollen/blobs mogen massief zijn (0,83).
9. **(H) Asymmetrie in alles:** geen gespiegelde ledematen, oren of ogen. Nabije arm doet iets anders dan de verre (Pikachu, Elekid, Treecko, Chimchar, Meowth, Squirtle: één arm geheven of naar voren).

### Pose en ledematen
10. **(H) Viervoeters: vier poten zichtbaar, elk een eigen kolom met lucht ertussen, voeten op 3–4 verschillende hoogtes.** Nabije voorpoot het laagst en het meest links; verre voorpoot iets rechts erachter en 1–3 px hoger, donkerder; nabije achterpoot rechts; verre achterpoot tussen de twee nabije in, hoger en donker. Zie Mightyena, Poochyena, Mudbray, Growlithe, Luxray.
11. **(H) Poten hebben gewrichten.** Achterpoot met hak naar achteren (Mightyena, Ponyta, Mudbray, Liepard), voorpoot licht gebogen. Twee rechte, parallelle stokken = meubel (onze alpaca-achterpoten).
12. **(R) Hoefdieren en herten heffen vaak één voorpoot** (gebogen knie) en worden daardoor levend: Ponyta, Rapidash, Girafarig, Stantler, Sawsbuck, Deerling.
13. **(H) Ledematen groeien uit de romp-curve.** Schouder en heup zijn bollingen in de omtrek; poten beginnen binnen de romp (overlap), nooit met een T-aansluiting onder een rechte buik. Verre ledematen: korter, hoger, in schaduwtint, deels achter de nabije.
14. **(H) Eén consistente houding**: het gewicht rust op de poten die op de grond staan. Twee poten die tegelijk vooruit grijpen terwijl de rest stilstaat (olinguito: klauwen horizontaal vooruit) is geen pose maar twee halve.
15. **(R) Staart sluit aan op de achterkant/bovenkant van de heup en loopt in een boog of S**, vaak omhoog boven de rug (Growlithe, Luxray, Meowth, Skitty, Pachirisu, Aipom). Rechte staarten zijn zeldzaam en dan bewust (Poochyena-stompje).

### Verhoudingen per fase
16. **(H) Fase 1 = grote kop, compacte romp, stompe ledematen.** Kop ±40–55% van de hoogte (Torchic, Mudkip, Teddiursa, Shinx, Eevee ≈ 50%; Charmander, Pikachu, Poochyena ≈ 40%), romp peer- of boonvormig en grotendeels achter/onder de kop, poten kort. Box ±36–40 px, oppervlak 700–950.
17. **(R) Fase 2 = puber in actie:** kop ±30–35%, langere ledematen, de pose zit vaak midden in een beweging (Grovyle, Combusken, Monferno, Frogadier, Torracat, Quilava). Oppervlak 1100–1500.
18. **(R) Fase 3 = vult het kader:** kop ±20–30%, brede stand, 60+ px hoog, vaak frontaler en imposant (Blaziken, Swampert, Typhlosion, Incineroar, Rillaboom). Oppervlak 1700–2600.
19. **(R) Hoe schattiger/jonger, hoe ronder en frontaler het gezicht mag** (Gen 7–9-starters, baby's), maar het lijf staat dan nog steeds schuin (Popplio, Sobble, Quaxly, Rowlet).

### Karakter → pose (zie ook de catalogus)
20. **(R) Fighting:** brede A-stand, knieën gebogen, vuisten omhoog en de nabije vuist groter/voorop, zwaartepunt laag en naar voren (Machamp, Hitmonchan, Primeape, Makuhita, Pancham, Infernape, Incineroar, Conkeldurr, Urshifu).
21. **(R) Psychic:** rechtop, verticaal, kalm, slank, vaak zwevend of op de tenen, één hand met voorwerp of gebaar; iets symmetrischer dan andere tweevoeters (vel 15: 0,67 tegen 0,58) (Alakazam, Hypno, Gardevoir, Gallade, Gothitelle, Hatterene, Espeon, Xatu, Medicham).
22. **(R) Dark en sluipers:** laag, voorovergebogen, kop vooruit en op of onder schouderhoogte, klauwen of puntige oren, één poot naar achteren (Sneasel, Weavile, Zoroark, Absol, Liepard, Houndoom, Mightyena, Nickit, Thievul, Purrloin).
23. **(R) Ghost en zwevers:** geen grondlijn, onderkant taps of franje, scheve stand (Shuppet, Duskull, Gastly, Drifloon, Banette, Mimikyu).
24. **(R) Zwaar/tank (Normal, Ground, Rock, grote Water):** frontaler, massa laag, poten kort en wijd, kop laag tussen de schouders (Snorlax, Ursaring, Pangoro, Kangaskhan, Slaking, Swampert, Rhyhorn met de kop omlaag).
25. **(R) Electric/kleine knaagdieren:** energiek, één arm of poot omhoog, staart scherp omhoog (Pikachu, Elekid, Shinx, Pachirisu, Dedenne, Emolga).

## Pose-catalogus
Per pose: voorbeelden (alle generaties), ledematen, gewicht, staart/kop, en welk karakter het draagt.

| # | Pose | Voorbeelden | Ledematen nabij/ver | Gewicht | Staart en kop | Karakter/type |
|---|---|---|---|---|---|---|
| P1 | **Staande viervoeter 3/4 (alert)** | Mightyena, Poochyena, Growlithe, Mudbray, Luxray, Lycanroc | 4 poten in 4 kolommen; nabij-voor laagst links, ver-voor 1–3 px hoger rechts erachter, ver-achter tussen de nabije in; hak achter | gelijk over 4 poten, borst iets naar voren | kop hoger dan de rug, staart omhoog of horizontaal als tegenwicht | Normal, Fire, Electric, honden, trouw/waakzaam |
| P2 | **Steigerend/stappend hoefdier** | Ponyta, Rapidash, Girafarig, Stantler, Sawsbuck, Zebstrika | één voorpoot geheven en gebogen, drie op de grond op verschillende hoogte | naar achteren, borst open | nek schuin naar voren, kop hoog, staart wapperend | sierlijk, trots, Fire/Normal/Grass |
| P3 | **Sluipend/laag** | Liepard, Nickit, Thievul, Purrloin, Zigzagoon, Yungoos, Absol | voorpoten gebogen, één vooruit; achterpoten opgetrokken | laag, naar voren | kop op of onder schouderhoogte, gestrekt; staart laag of in een boog | Dark, dieven, jagers, marters |
| P4 | **Zittende viervoeter** | Vulpix, Eevee, Skitty, Umbreon, Espeon, Lillipup | voorpoten recht en dicht bij elkaar (niet identiek, verre hoger/donker), achterpoot als dij-bolling | op de billen achteraan | kop gedraaid naar de kijker, staart om het lijf of omhoog | schattig, rustig, Normal/Fairy/Psychic |
| P5 | **Zitten op de billen (tweevoeter)** | Teddiursa, Munchlax, Bidoof, Sentret (op staart), Grookey | korte beentjes vooruit, één arm naar de mond/omhoog | laag en rond, romp schuin achter de kop | kop iets gekanteld, één oor hoger | knuffelig, Normal, beren, knaagdieren |
| P6 | **Staande kleine tweevoeter (starterhouding)** | Charmander, Squirtle, Torchic, Piplup, Chimchar, Riolu, Pikachu, Scorbunny | voetjes wijd en verschillend gedraaid, nabije arm voor de romp, verre arm deels achter; vaak één arm omhoog | op beide voetjes, romp licht naar achteren | staart rechtsachter als tegenwicht, kop 40–55% | starters, vriendelijk, alle types |
| P7 | **Vechthouding** | Hitmonchan, Machamp, Primeape, Makuhita, Pancham, Lucario, Combusken, Incineroar | A-stand, knieën gebogen, nabije vuist groot en voorop, verre vuist hoog | laag en naar voren | kop tussen de schouders, blik naar links | Fighting, bokser-lama |
| P8 | **Elegant rechtop/zwevend** | Gardevoir, Kirlia, Alakazam, Gothitelle, Hatterene, Meditite, Medicham | slank, armen asymmetrisch (één gebaar of voorwerp), voeten dicht bij elkaar of verborgen | verticaal, licht | kop rechtop, rok of staart als zoom | Psychic, Fairy, genezers (maangenezer-nachtaap) |
| P9 | **Klimmer/aap (dynamisch)** | Aipom, Ambipom, Mankey, Monferno, Infernape, Simisage, Passimian | armen in verschillende richting, staart als vijfde ledemaat, vaak één voet van de grond | uit balans, beweging | kop gedraaid naar de kijker, staart in een krul | speels, Normal/Fighting/Fire |
| P10 | **Zwevend/vliegend** | Butterfree, Beautifly, Pidgeot, Swablu, Drifloon, Gastly, Ninjask | nabije vleugel groot en open, verre kleiner en hoger/achter | geen grondlijn | kop 3/4, staart/onderkant taps | Bug, Flying, Ghost |
| P11 | **Zittende/staande vogel** | Starly, Murkrow, Taillow, Hoothoot, Rowlet, Fletchling | pootjes klein en verschillend, vleugels gevouwen langs het lijf | op de pootjes, borst vooruit | snavel in profiel = één oog; uil = twee ogen frontaal | Flying, Normal, Dark |
| P12 | **Opgerold / S-bocht** | Ekans, Arbok, Seviper, Dratini, Milotic, Serperior, Dragonair | geen ledematen; lussen achter elkaar met overlap | lussen laag rechts | kop hoog links, nek als S | Poison, Dragon, Water |
| P13 | **Liggend/kruipend** | Slakoth, Zigzagoon, Caterpie, Wurmple, Snom, Spheal | pootjes nauwelijks zichtbaar, onderkant op de grond | horizontaal, laag | kop links iets opgeheven | lui, Bug, Ice |
| P14 | **Bol met gezicht** | Jigglypuff, Voltorb, Clefairy, Whismur, Togepi, Wooloo, Mareep, Cuyby | stompjes of geen; als ze er zijn: verschillend van hoogte | op een smalle voet of zwevend | gezicht links van het midden, één kenmerk (kuif, oren, staart) breekt de bol | schattig, Normal/Fairy |
| P15 | **Massief/tank** | Snorlax, Ursaring, Pangoro, Swampert, Rhyhorn, Mudsdale | korte wijde poten, armen hangend of uitgespreid | laag, breed | kop laag tussen de schouders of naar beneden (charge) | Normal, Ground, Rock, Fighting |

Pose kiezen voor een nieuwe fakemon: **type + karakter → pose (P#) → skelet-sprite uit die rij met vergelijkbaar formaat**. Voorbeelden voor onze lijnen: alpaca (bokser) fase 1 = P1/P2 met een vleugje P7 in de voorpoten, eindvorm P7; olinguito (dief, Dark) = P3 of P1-laag op Poochyena/Nickit; nachtaap (maangenezer, Psychic) = P5 → P8; Cuyby = P14, Cuychu = P13/P14.

## Onze sprites naast echte sprites
Vellen `c_alpaca.png`, `c_olinguito.png`, `c_nachtaap.png`, `c_cuy.png`, uitvergroot `z_ons.png`.

| Sprite | Meting | Wat echte sprites doen | Wat wij doen |
|---|---|---|---|
| **Alpaca r15** (vs Ponyta, Mudbray, Deerling, Girafarig) | 937 px, 34×51, soliditeit 0,66 | romp is de grootste massa; nek schuin naar voren en taps; kop overlapt de nek; achterpoten met hak; één poot geheven | nek als verticale zuil met evenwijdige randen; romp klein en blokvormig; achterpoten twee rechte stokken; handschoenen zijn het grootste kenmerk (accessoire, niet het dier) |
| **Olinguito r18** (vs Poochyena, Nickit, Sentret, Skwovet) | 1118 px, **54×37** (fase-1-box is ±38–40 breed) | korte snuit → twee ogen met neus ertussen, óf lange snuit → één oog; romp compact; vier poten dragen | lange profielsnuit met twee ogen naast elkaar in een maskerband (bril); romp lang en horizontaal (volwassen marter, geen fase 1); klauwen horizontaal vooruit zonder dat ze iets dragen; te breed en te groot |
| **Nachtaap r10** (vs Teddiursa, Aipom, Chimchar, Grookey) | 1033 px (fase 1 ±805), 49×36 | kop gedraaid, één oor hoger, gezicht links van het midden, romp schuin achter de kop, één arm doet iets | kop en gezicht symmetrisch en gecentreerd, ogen even groot op gelijke hoogte, romp recht onder de kop, armen gespiegeld naast het lijf; alleen de staart is asymmetrisch |
| **Cuyby r3** (vs Mareep, Wooloo, Jigglypuff) | 789 px, symmetrie **0,94**, soliditeit 0,87 | bollen hebben symmetrie ±0,78: gezicht naar links, één kenmerk breekt de bol | werkt als bol (goedgekeurd), maar het gezicht staat gecentreerd; dat is de grens van "frontaal" |
| **Cuychu r4** (vs Wooloo, Linoone, Zigzagoon) | 1416 px, soliditeit 0,84 | grote vachtdieren laten poten of een snuit uit de massa steken (Wooloo-pootjes, Zigzagoon-snuit) | massa met gezicht links (goed), maar vrijwel geen negatieve ruimte: een vachtkoepel |

De gemeenschappelijke fout: **wij bouwen een vorm in één vlak** (alles profiel of alles frontaal), uit losse blokken (zuil, doos, stokken) die elkaar niet overlappen. Echte sprites draaien de kop meer dan het lijf, laten delen elkaar overlappen en zetten elk ledemaat anders.
