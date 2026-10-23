# Spriting: regels uit de Dragonfly Cave-gidsen

Bronnen (van Jordi, 23 okt): `docs/lessen/bronnen/dragonflycave_spriting_guide.pdf` (*Spriting Guide*, The Cave of Dragonflies) en `make_fakemon_guide.pdf` (*Making Fake Pokémon*). Lees dit samen met `FAKEMON_DESIGN.md` **vóór elke spriteronde**, en lees voor details de gids zelf: de volledige tekst (OCR) staat in `docs/lessen/bronnen/*.txt`, de plaatjes in de PDF's (Jordi: de gidsen zeggen meer dan deze samenvatting). Hieronder de regels, en per regel wat wij fout deden.

## 0. Verplichte checklist vóór oplevering (elke sprite, elke ronde)
Deze punten gingen herhaaldelijk mis; loop ze **expliciet** na en noteer in NOTITIES.md per punt "ok" of wat je deed:
1. **Lichaam én blik diagonaal (3/4 naar links-voor):** niet alleen de ogen, ook het lijf staat schuin (verre kant korter en in schaduw), zoals vrijwel elke Gen 3-front-sprite. Zuiver profiel of zuiver frontaal = fout (Jordi, olinguito ronde 8, Cuyby-evolutie ronde 2). Bijna frontaal mag, zolang er perspectief in zit: blik en verre kant 3/4, verre arm kleiner dan de nabije, en het dier zit niet recht op zijn billen vooruit te kijken (Jordi, nachtaap ronde 10: "we zitten er niet frontaal op").
2. **Alle ledematen, oren en ogen geteld en verbonden** (geen geamputeerde verre kant, geen losse voet of staart).
3. **Geen rechte lijnen** in de omtrek waar het dier rond is; curven zonder hoeken.
4. **Ogen geïntegreerd** (bovenlid, gekleurde iris, glans + reflectie), niet opgeplakt; verre oog geen kopie.
5. **Silhouet op 1× leest als de soort** (knijp-je-ogen-test naast de referentiefoto en echte sprites).
6. **Formaat** vergeleken met echte sprites van dezelfde evolutiefase.
7. **Pose niet stijf:** gewichtsverschuiving, poten niet kaarsrecht naast elkaar.

## 1. Gereedschap: alles met de hand, nooit met vormfuncties
- **Gouden regel van omlijnen: gebruik geen vormgereedschap** (cirkel/ellips-tool). De computer tekent de wiskundig dichtste benadering van een cirkel, maar die is niet de mooiste: een met de hand getekende 'cirkel' is gladder voor het oog.
- Alleen een 1-pixel-potlood, emmer zonder anti-aliasing, geen verkleinen/vergroten van de sprite zelf.
- **Wat wij deden:** vormen met PIL-ellipsen en -polygonen, schaduw en omlijning met scripts. Dat is precies de 'wiskundige cirkel'. Daarom oogden onze sprites als plastic speelgoed.

## 2. Werkwijze: grof tekenen, dan per onderdeel gladstrijken
- Teken de grote lichaamsdelen eerst **grof met de hand** (als een krabbel), en strijk elk deel daarna **pixel voor pixel** glad tot een nette 1-pixel-omlijning. **Eén lichaamsdeel tegelijk**, nooit de hele sprite in één keer.
- Kleine details (klauwen, vingers) pas als de grote vormen staan; dunne ledematen pixel voor pixel.
- Riskante delen op een aparte laag of kopie.
- **Pixel-over** is een erkende methode: verklein een tekening (Sugimori-art of een eigen modeltekening) tot spriteformaat en trek hem met de hand over, met de regels van het omlijnen. **Dit is de logische stap na onze modeltekeningen**: de goedgekeurde tekening verkleinen tot ±64 px en met de hand overtrekken, in plaats van een bestaande sprite als skelet te nemen.
- Hoe groter de sprite, hoe exponentieel moeilijker: blijf bij het Gen 3-formaat (max. 64×64, de figuur meestal kleiner).

## 3. Lijnen, hoeken en curven
- Een schuine lijn = segmenten die telkens 1 pixel verspringen; een regelmatig patroon (bijv. 1-2-1-2) leest als recht. Liever een eenvoudiger helling dan een 'bobbel'.
- **Hoeken** (corner) wijzen schuin, **punten** (point) recht; samen 8 richtingen. Gebruik ze alleen voor echte scherpe punten (klauwen).
- **Curven:**
  - tussen een horizontaal en een verticaal segment langer dan 1 moet minstens één 'neutraal' segment van 1 pixel zitten;
  - **nooit een hoek of punt in een curve** (geeft een zichtbaar 'spijkertje');
  - geen 'besluiteloosheid': de segmentlengtes moeten geleidelijk oplopen of aflopen (bijv. 1-1-2-3), niet heen en weer (3-1-2-2-1 leest als wiebelig);
  - een lange rechte lijn die abrupt in een andere overgaat, breekt de curve; laat de helling geleidelijk veranderen.
- **Symmetrie en identieke delen verraden een nep-sprite**: nooit een lichaamsdeel kopiëren en spiegelen voor de andere kant. *(Onze nachtaap: frontaal en symmetrisch.)*

## 4. Kleuren en palet
- Per kleur **3 tinten** (hooglicht, basis, schaduw) plus een donkere omlijningstint; de relatieve helderheid tussen de tinten blijft altijd gelijk.
- Alle tinten van een kleurgroep in dezelfde tint; schaduwen eventueel een beetje richting blauw.
- **'Overshaden'** (meer tinten, verlopen) ziet er nep uit. Werken met een beperkt palet is juist de kunst.
- Neem kleuren liefst over van een bestaande sprite met ongeveer die kleur (geen te felle eigen kleuren).

## 5. Licht en schaduw
- **Licht komt van linksboven** bij een sprite die naar links kijkt (rechtsboven als hij naar rechts kijkt). Denk aan een spuitbus vanuit die hoek: wat de verf raakt is licht, de rest schaduw.
- De grens basis/schaduw ligt op de **'evenaar'**: de grens tussen de delen die naar het licht en van het licht af gekeerd zijn. Volg de ronding van het lijf; delen achter het lijf (staart) krijgen veel schaduw.
- Hooglicht klein en precies waar het licht loodrecht valt; **slagschaduw** van een ander lichaamsdeel altijd volledig in de schaduwkleur; de extra donkere tint alleen waar zowel direct als teruggekaatst licht ontbreekt.
- **R/S-stijl gebruikt veel van de hooglichtkleur** (de Yellow-Scyther met witte glimlichtjes oogde donkerder dan de R/S-Scyther met veel lichte groentint). Te weinig hooglicht maakt een sprite te donker.

## 6. Glans en ogen
- Glans (*shine*) = een klein rond, bijna wit vlekje waar het licht naar de kijker weerkaatst; niet op elk hooglicht, alleen waar het oppervlak glanst.
- **Ogen:** kraalogen (zoals Pikachu en Eevee) hebben **altijd een witte glansvlek én een gekleurde reflectie aan de tegenoverliggende kant** (teruggekaatst licht). Dat geeft diepte. *(Onze ogen: grote ronde 'brillenglazen', egaal gloeiend of poppenogen met te veel glans: Jordi: "de ogen zijn vaak niet echt Pokémon-achtig".)* Bij zeer glanzende delen een beetje teruggekaatst licht in de schaduw, eventueel gedithered (Voltorb).

## 7. Texturen
- **Vacht:** maak de grens tussen basis en schaduw **gekarteld, zoals de vacht zelf**, eventueel met wat dithering en korte streepjes in de haarrichting. Niet overdrijven. Ook voor veren. *(Alpaca: 'klonterige wolschaduw'.)*
- **Schubben:** meestal weglaten, of groot genoeg om met omlijning te tekenen (Magikarp).
- **Rots/staal:** opdelen in vlakke vlakken, die elk één tint krijgen; elke lijn moet echt twee vlakken scheiden.
- De meeste Pokémon: gewoon zoals de bol hierboven; het zijn tekenfilmwezens.

## 8. Omlijning (de grootste les)
- **Volledig zwarte omlijning oogt 2D en tekenfilmachtig** (de guide laat het zien bij de Scyther-revamp). *(Precies wat Jordi bij de nachtaap zei: "heel cartoony"; onze meting: donkere rand 0,93 tegen 0,35–0,6 bij Gen 3.)*
- Omlijning per kleurgroep:
  - **zwart** (of bijna-zwart) rond de schaduwkant;
  - de **omlijningsbasis** (een donkere tint van die kleur) rond de basiskleur;
  - de **schaduwkleur als omlijnings-hooglicht** op de meest belichte randen;
  - eventueel (Pikachu) de schaduwkleur als extreem hooglicht op de lichtste randen.
  - Overgang langs de omtrek: helemaal zwart → zwart met een pixel omlijningsbasis aan de binnenkant → omlijningsbasis → omlijningsbasis met een pixel hooglicht aan de binnenkant → een paar segmenten hooglichtkleur.
- Omlijning altijd **1 pixel breed**, geen klonten zwart.
- **Anti-aliasing alleen aan de binnenkant** van de omlijning (lichtere pixels naar binnen), **nooit aan de buitenkant**: dat geeft lelijke gekleurde puntjes op een andere achtergrond.
- **Pseudo-omlijning:** dunne delen van 1–2 pixels (bijv. een rand van Scythers sikkels) niet omlijnen, maar alleen met kleur scheiden.

## 9. Overige sprites (voor later)
- Gen 3: voorkant 64×64, 2 frames (Emerald); achterkant 64×64, vergroot en links/onder afgesneden; party-icoon 32×32 in 2 frames (bovenkant bijna-zwarte omlijning, onderkant grijze omlijning om diepte te geven; slechts 3 icoonpaletten); overworld 32×32 (kleine 16 breed), grote 64×64; voetafdruk 16×16 als silhouet.
- Shiny = alleen een ander palet; binnen een lijn meestal dezelfde shinykleuren.

## 10. Uit de fakemon-guide (aanvullend op FAKEMON_DESIGN.md)
- **Taakverdeling (Jordi, 23 okt):** types, evoluties, stats, moves en naamgeving bepaalt Jordi; hij geeft de richting en Claude werkt het daarna in detail uit met de regels hieronder. Niet zelf voorstellen tenzij hij erom vraagt.
- Drie soorten fakemon: origineel, tegenhanger van een bestaande, en (pre-)evolutie. Lijkt een idee te veel op een bestaande Pokémon, overweeg het dan in die lijn op te nemen of maak het juist duidelijk anders.
- Grootte en stadia volgen de game: vroeg = klein eerste stadium (3 stadia als de eindvorm groot is), midden = groter begin, laat = grote losse soort. **Pre-evoluties zijn bijna altijd kleiner, schattiger en eenvoudiger.**
- Type: liever een nieuwe combinatie, of een type dat soortgelijke Pokémon nog niet hebben. Geen idee? Normal.
- Stats: begin bij een vergelijkbare Pokémon en schuif; HP = dik/groot, Defense = pantser, Sp. Def = vacht/vet (isolatie), snel = klein en slank. Krachtige gimmick = lage stats.
- Evolutie: max. 3 stadia per lijn; geen level-evolutie na een steen-, ruil- of vriendschapsevolutie (behalve baby's); steen-evoluties leren daarna nauwelijks nog moves.
- Level-up-moves: 1–2 startmoves (zwak, meestal Normal, ≤ 40–50 kracht), een vast ritme van levels (bijv. om en om 2 en 4), na evolutie ruimer; nooit meer dan 3 statusmoves op rij.
- Sekseverschillen alleen als de soort daar reden voor geeft; bij dieren is het mannetje meestal het opvallendste, geen menselijke stereotypen.
- Naam: meestal een samentrekking van een woord voor het type en een woord voor het basisdier/-voorwerp; niet te obscuur.

## 11. Werkwijze-lessen (olinguito ronde 8)
- Handwerk als tekstraster per lichaamsdeel (`y: x"pixels"`, achterste deel eerst) met een klein opbouwscript (`docs/concept/sprites/olinguito/ronde8/bron/build.py`); een dump met kolomnummers maakt fouten in rijlengtes direct zichtbaar.
- Meet het oppervlak al bij de eerste opzet tegen echte Gen 3-sprites (Teddiursa 652, Torchic 782, Mudkip 852, Treecko 967): de eerste olinguito was 1660 px en moest helemaal opnieuw op ¾ schaal.
- Zwarte kraalogen verdwijnen in een donker masker; een gekleurde iris (goud) met witte glans leest wel op 1×.
- Drie dunne klauwen lezen als een vork of bezem; twee brede haken die overlappen lezen als één gereedschap (Drilbur).

## 11b. Werkwijze-lessen uit de praktijk
- **Rasters met de hand, maar controleerbaar** (nachtaap ronde 8): schrijf rijen als run-length (`3.2V4h`) of als `x:pixels` met absolute x en laat het script de breedte controleren; tellen in lange tekstrijen gaat anders steeds mis. Lagen (staart, lijf, kop) los, achter naar voor.
- **Itereer op het geheel**: render na elke grote stap op 8× en op 1×; de eerste versie van de nachtaap was 1305 px en leek een kist (rechte rug, horizontale armbalk). Kleiner tekenen en de armen in een V zetten loste dat op.
- **Gelijke kleur naast gelijke kleur verdwijnt**: violette armen op een violet lijf lazen niet; een crème borst erachter wel.
- **Een gekleurde ronde punt leest als een oog**: geef staartpunten niet de oogkleur.
- **Ronde 9 (reparatieronde):** één delenformaat voor alle soorten (`## naam x y dy2` + tekenrijen) met `bouw9.py`, dat meteen open randen (randpixel zonder omlijningskleur), rechte randstukken > 4 px en het zwart-aandeel meldt; met de hand geschreven pixelrijen gaan erin via `zet.py` (voorbeeld: `docs/concept/sprites/*/ronde9/bron/`).
- **Oogmaat meten, niet schatten:** Jigglypuff-oog ±25% van de kopbreedte; ronde 8 zat op 38%. Oogomlijning in de gezichtstinten (donkere iriskleur, crèmeschaduw eronder) in plaats van een zwarte ring haalt het "opgeplakte".
- **3/4 zit in de linkerkant van de kop:** laat de verre wang 1–2 px voorbij het verre oog uitsteken, zodat de neusbrug schuin uit het gezicht komt; een snoet die vanaf de schedelrand recht opzij steekt leest als profiel.
- **Verre arm op een donker lijf** verdwijnt; een zwarte rand aan de lichte kant plus één rij basistint maakt hem zichtbaar.
- **Rasters met absolute x** (olinguito ronde 11): `y x pixels` per regel (`bron/delen_abs.txt` → `abs2delen.py` → `bouw9.py`); meerdere regels per y in één deel mogen, zo teken je overlappende klauwen zonder te tellen.
- **Zijwaartse blik = pupil tegen de voorrand van het oog.** Naar de kijker: pupil in het midden-onder met iris aan beide kanten (oog ≥ 4 px breed), en omlijning naast de pupil in de maskerkleur in plaats van zwart, anders smelt de pupil met de rand.
- **Klauw als deel van de hand:** eindig de poot in een vingerrij met een zwarte splitsing en laat elke klauw direct onder een vinger beginnen met dezelfde breedte; een klauw die versmalt moet rechtsonder zwart sluiten (anders open rand).
- **Twee klauwhanden naast elkaar lezen als een hark**; zet de verre poot op een andere hoogte (opgetrokken sluippoot) zodat de klauwgroepen apart lezen.
- **Een rechte arm van schouder tot poot is een plank**: geef hem een elleboog naar achteren en een onderarm naar voren, en houd hem kort (Pokémon-armen zijn stomp).

## 12. Lessen uit Jordi's feedback op ronde 8
- **Geen 'geamputeerde' verre ledematen:** in een 3/4-pose zijn de verre arm en het verre been bij Gen 3 altijd (deels) zichtbaar achter of naast het lijf. Laat ze nooit weg; teken ze kleiner en in de schaduwkleur. Check: tel per sprite de armen, benen en oren.
- **Alles afmaken en verbinden:** elke voet, oor en elk lijfdeel sluit met een doorlopende omlijning aan op het lijf; geen open of half afgemaakte randen. Controleer ingezoomd elke rand van de omtrek.
- **Geen lange rechte lijnen in organische vormen** (staarten, ledematen): elke lijn buigt (vgl. Aipom- en Mew-staart).
- **Gezicht compleet:** ogen, mond (ook als hij klein is) en oren horen erbij; ontbreekt er één, dan oogt het onaf.
- **Ogen niet 'opgeplakt':** de oogkassen en de omlijning van de ogen in de kleur van het gezicht laten overlopen (gekleurde omlijning en schaduw rond het oog), en de oogkleur laten passen bij het type (Psychic: roze/paars/rood/cyaan zoals Espeon, Abra, Ralts, Natu).
- **Kijkrichting:** Gen 3-sprites kijken bijna altijd **diagonaal** (3/4 naar links-voor, beide ogen zichtbaar), niet in zuiver profiel (Jordi, olinguito ronde 8).

## 13. Lessen uit de Cuyby-evolutie ronde 1 (gras/vacht als silhouet)
- **Gras = smalle, rechte halmen** (1–5 px, vaste helling); brede, golvende plukken in geel/oranje lezen als vlam of stekels.
- **Een kenmerkvlak (Cuyby's zwart) moet een vlak blijven:** een smalle diagonale band van oor naar oog las als piratenooglap; compact rond het oog met het oor er direct naast werkt.
- **Belichte punten bovenaan** (sprieten, oren) krijgen de omlijningsbasis in plaats van zwart; dat haalde het zwart-aandeel van 0,63 naar 0,51 zonder de vorm te veranderen.
- **Controleer onder- en bovenranden van het lijf apart:** een verborgen bovenrand of een rechte onderrand van 20+ px valt op 1× direct op; dump het raster met kolomnummers (`frame().text()`) om ze te vinden.

## 14. Lessen uit alpaca ronde 10 (silhouet)
- **Eerst het silhouet tegen een foto van het echte dier** (2–3 ruwe schetsen op 64×64): na negen rondes op details bleek de alpaca een schaap omdat de kop direct op het lijf zat.
- **Een lange nek moet zichtbaar zijn:** een grote babykop dekt de nek af; zet de kop hoger en het lijf lager (7–9 px nek onder de kin), en laat de nekrug als één holle curve van achterhoofd naar rug lopen.
- **Run-length-rijen met absolute x** (`y x0 3V 2W 1. 5w`, `ronde10/bron/bouw10.py`) zijn het snelst om met de hand bij te werken: een deel verschuiven of 3 px korter maken is één getal per rij.
## 15. Lessen uit de Cuyby-evolutie ronde 2 (lange vacht)
- **Lange vacht valt steil omlaag, niet horizontaal:** scheidingen van kop naar staart lazen als een gefrituurde garnaal of een pissebed. Scheidingen die van de rug steil naar achteren-omlaag lopen tot aan lokpunten in de zoom, lezen als hangende vacht of een rieten dak.
- **Een gladde koepel is een brood:** vacht moet de omtrek breken. Laat lokken overlappen aan de achterkant (een lichtere punt met een inham eronder, zoals de staarten van Ninetales) en geef de zoom hangende lokpunten.
- **Een lok in een boog met een gat eronder leest als een hengsel.** Vul de ruimte onder een overhangende lok met de vacht erachter, in de schaduwtint, en laat alleen onder de punt een inham open.
- **Scheidingen in drie tinten langs de lengte:** bovenaan zacht (schaduwtint), in het midden de omlijningsbasis, alleen bij de zoom zwart. Doorlopend zwarte, even ver uit elkaar liggende lijnen lezen als segmenten. Onderbreek ze hier en daar en vul aan met korte streepjes (schaduw, en hooglicht in het licht) in de haarrichting.
- **Run-length-rijen op absolute x met overschrijven** (`y: x: 3h 12s  x: d r h`) maken handwerk per deel snel en controleerbaar. Teken eerst de basistinten per rij, en zet daarna de lijnen als drietallen 'donkerder | scheiding | lichter' erover (`docs/concept/sprites/cuyby_evo/ronde2/bron/`).
- **Te groot? Knip een strook weg** in plaats van opnieuw te tekenen: een kolom of rij zonder kenmerken (geen oog, inham of neus) eruit halen kost op het oog niets. Dat ging hier van 1487 naar 1385 px.
- **Een roze vlekje in een zwart oor leest op 1× als een tweede oog.** Gebruik in een donker oor hooguit één roze pixel.

## 16. Lessen uit nachtaap ronde 10 (reparatie, uitdrukking)
- **Een spiraal van 1¼ slag past in 13×15 px** met een buitenring van 3 px, een binnenkrul van 3 px (O-v-K) die vanaf de onderkant opstijgt en een vrij kopje met ≥ 1 px lucht rondom; zie `docs/concept/sprites/nachtaap/ronde10/bron/delen.txt` (deel `staart`).
- **Lucht tussen delen die in frame 2 tegengesteld bewegen** (oor omlaag, staart omhoog) altijd horizontaal maken: een lege kolom blijft in beide frames leeg.
- **Slagschaduw die met een bewegend deel meeschuift** als eigen mini-deel met dezelfde dy2 als dat deel (`## kinschaduw x y 1`); in frame 1 valt het samen met de bestaande schaduw.
- **Uitdrukking zit in één of twee rijen:** een opgewipte flick aan de buitenhoek leest als verdrietig, een vol zwart lid plus een volle donkere irisrij als halfdicht en slaperig; neutraal en starend = lid K, zwaarst aan de buitenhoek, tweede rij al middentint, kleine pupil met iris rondom.
- **Verzadiging verhogen bij gelijke tint verlaagt de helderheid** (HSV-waarde gelijk houden is niet genoeg): reken de luma na (0,3R+0,59G+0,11B) en til de waarde op tot het niveau van de referentie (Aipom ±137).
- **Een tekenrij met absolute x meteen renderen** (een klein overlay-script dat het blok over het raster legt) is sneller dan via `delen.txt` itereren als een heel deel opnieuw getekend wordt.

## 17. Lessen uit alpaca ronde 11 (herstart from scratch)
- **Verzonnen kleurvlakken mogen, maar alleen als ze werken:** een gezicht, poten of buik in een andere kleur dan het echte dier kan, zolang de soort herkenbaar blijft en het één geheel oogt. Bij de alpaca maakten het crème gezicht en de bruine poten (ronde 9–10) juist de herkenning kapot (Eevee-kop op een schaap); één vachtkleur overal, alleen schaduwtinten, liet hem meteen alpaca lezen. Check altijd tegen een foto of het echte dier dat vlak heeft.
- **Kop als één blok met een vaste x0** (`y 12 ....VwwKK...`, alle rijen even lang) is makkelijker te tekenen en te controleren dan losse run-length-rijen: kolommen staan recht onder elkaar en een oog verschuiven is één teken per rij (`ronde11/bron/bouw11.py` leest beide vormen).
- **Oppervlak sparen zonder de soort te verliezen:** een lange nek kost weinig als hij smal is (9–10 px); de meeste winst zat in een lijf dat 1 kolom korter is, kortere achterpoten (die staan verder weg en dus hoger) en een kop zonder lege wangen (1030 → 869 px).
- **Diepte via voethoogte:** dichtbije voorvoet het laagst, verre voorvoet 3 px hoger, achtervoeten nog 2–4 px hoger; zo staat een viervoeter 3/4 in plaats van in profiel, ook als het lijf zelf nog vrij zijwaarts is.
- **Een fringe-schaduwlijn vlak boven de ogen leest op 1× als boze wenkbrauw:** houd de pixels direct boven een oog licht en zet de franjepunten tussen de ogen.

## 18. Lessen uit olinguito ronde 12 (houding en klauwen)
- **Klauwrichting controleren aan de verschuiving per rij:** een klauw die verticaal begint en aan de punt opzij uitwaaiert (verschuiving 0,0,−1,−1) heeft de holle kant aan de verkeerde kant en oogt gespiegeld. Een haak zoals Sandslash/Zangoose: eerst schuin naar voren, dan recht omlaag (−2,−1,−1,0,0,0); bolle kant voor/boven, holle kant naar achteren/de grond.
- **Bij een verschuiving van 2 px komt de bovenkant bloot:** die pixels krijgen de omlijningstint (8), en wat de volgende rij niet bedekt de zwarte rand (0); anders meldt bouw9 open randen.
- **"Meer voorovergebogen" betekent de kop echt verplaatsen** (5 px omlaag en naar voren) en de heup het hoogste punt van de rug maken; een paar pixels kantelen in het lijf zie je niet.
- **Twee poten verschillend maken = alles tegelijk anders:** hoek (gebogen vs gestrekt), lengte, dikte, tint (dichtbij lichter, ver in 2/1), voetmaat en voethoogte (ver 1 rij hoger).
- **Delen die in frame 2 bewegen:** laat het stilstaande deel eronder (hier het lijf onder de kop) 4–6 px doorlopen, anders komt in frame 2 een rand zonder omlijning bloot.
- **Een mond die direct boven de kaaklijn ligt, smelt ermee samen:** laat één pixel room tussen lip en kaakrand, en een wit tandje onder de lip maakt hem leesbaar op 1×.
- **Sandbox-valkuil:** in een worktree weigert de omgeving samengestelde shell-regels (heredoc + `&&`, `cd ..`); zet bewerkingen in een los script in de scratchpad en roep dat met één `python3`-regel aan.

## 19. Lessen uit de Cuyby-evolutie ronde 3
- **Een laag, lang dier in 3/4:** laat de rug naar achteren dalen en de zoom naar achteren stijgen. Lopen die twee lijnen naar elkaar toe, dan leest de romp kleiner en verder weg. Een schuine rugscheiding met de verre flank als smalle schaduwband erboven maakt het af (Mareep, Linoone).
- **Verre pootjes staan links van en hoger dan de nabije** bij een dier dat naar links-voor kijkt: bij die draaiing schuift de verre kant naar links en naar achteren. Ze staan dus niet rechts ervan en ook niet erachter verstopt.
- **Gezicht in een vachtmassa:** zet het gezicht binnen de vacht, met haar aan de verre kant (gordijn of pony). Tegen de linkerrand leest het als profiel. Houd het wit bij een snuit en een kleine bles; een lange witte diagonale streep leest als snavel.
- **Losse zwarte 1-px-sprietjes in de omtrek lezen als vliegjes.** Maak sprieten aan de rand 2 px breed aan de voet of geef ze de omlijningsbasis (r), en laat ze diagonaal aansluiten.
- **Na het knippen opnieuw controleren:** een geknipte kolom kan net de laatste randpixel van een rij zijn (de rij verliest haar omlijning) of de enige kleurpixel van een voetje. Leg kenmerken van 1 px niet op een knipkolom en lees de randmelding van `bouw9` opnieuw.
- **Letterlijke pixels naast run-length** (`rle3.py`: `rhhsd` naast `3h`, `.` = laat staan) is voor kleine vormen zoals sprieten, ogen en punten sneller dan tellen.

## 20. Lessen uit de Cuyby-evolutie ronde 4
- **Lees de randmelding van `bouw9` echt na vóór je "geen open randen" noteert:** ronde 3 meldde 19 open pixels (lichte spriettoppen, d/q op de schaduwkant) terwijl de notities "ok" zeiden. Lichte toppen krijgen r erboven, schaduwkant K eronder; controleer frame 2 apart, want een deel dat opzij wuift legt de voet eronder bloot (r op de rij erboven in het stilstaande deel).
- **Na een knip de bron terugschrijven naar eindcoördinaten** (`cuyby_evo/ronde4/bron/omzet.py`: het geknipte `delen.txt` terug naar run-length-rijen, gecontroleerd met `cmp` op het raster): dan zijn keuring, raster en bron gelijk en is elke reparatie één getal in plaats van omrekenen.
- **Een gezicht "meer in de vacht" = de lokken van de pony onderaan laten ombuigen naar omlaag over de bovenkant van de snuit, en een wangetje haar tussen snuit en vlek;** de snuit hoeft dan maar 1–2 px smaller voor de helft minder wit. Proef zulke blokken eerst als overlay op het raster (`cuyby_evo/ronde4/bron/proef.py`: legt `proef_blok.txt` over `raster_f1.txt` en rendert 12×/3×/1×), daarna pas in de delen.
