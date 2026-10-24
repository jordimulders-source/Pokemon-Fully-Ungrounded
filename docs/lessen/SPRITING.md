# Spriting: regels uit de Dragonfly Cave-gidsen

Bronnen (van Jordi, 23 okt): `docs/lessen/bronnen/dragonflycave_spriting_guide.pdf` (*Spriting Guide*, The Cave of Dragonflies) en `make_fakemon_guide.pdf` (*Making Fake Pokémon*). Lees dit samen met `FAKEMON_DESIGN.md` **vóór elke spriteronde**, en lees voor details de gids zelf: de volledige tekst (OCR) staat in `docs/lessen/bronnen/*.txt`, de plaatjes in de PDF's (Jordi: de gidsen zeggen meer dan deze samenvatting). Hieronder de regels, en per regel wat wij fout deden.

## 0. Verplichte checklist vóór oplevering (elke sprite, elke ronde)
Deze punten gingen herhaaldelijk mis; loop ze **expliciet** na en noteer in NOTITIES.md per punt "ok" of wat je deed:
1. **Lichaam én blik diagonaal (3/4 naar links-voor):** niet alleen de ogen, ook het lijf staat schuin (verre kant korter en in schaduw), zoals vrijwel elke Gen 3-front-sprite. Zuiver profiel of zuiver frontaal = fout (Jordi, olinguito ronde 8, Cuyby-evolutie ronde 2). Bijna frontaal mag, zolang er perspectief in zit: blik en verre kant 3/4, verre arm kleiner dan de nabije, en het dier zit niet recht op zijn billen vooruit te kijken (Jordi, nachtaap ronde 10: "we zitten er niet frontaal op").
2. **Alle ledematen, oren en ogen geteld en verbonden** (geen geamputeerde verre kant, geen losse voet of staart).
3. **Geen rechte lijnen** in de omtrek waar het dier rond is; curven zonder hoeken.
4. **Ogen geïntegreerd** (bovenlid, gekleurde iris, glans + reflectie), niet opgeplakt; verre oog geen kopie. **Bij een dier met een snuit is vaak maar één oog in beeld** (Poochyena, Cyndaquil, Typhlosion, Rhyhorn, Dragonair, Kabutops): het verre oog verdwijnt achter de neusbrug; twee ogen naast een snuit geeft al snel een profiel-met-bril of een te grote kop (Jordi, olinguito ronde 18).
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

## 20. Lessen uit olinguito ronde 13 (3/4-constructie van een viervoeter)
- **Verre poten staan links van én hoger dan de dichtbije** bij een 3/4 naar links-voor (de verre kant draait naar achteren; zie Mightyena, Poochyena). Een verre poot rechts van de dichtbije, of een dichtbije poot midden onder de buik ver van de heup, geeft een Escher-pose: dan klopt de overlap niet met de diepte. Check: hangt elke poot onder zijn eigen schouder of heup?
- **Eerst een constructieschets over de vorige ronde** (twee ovalen voor borst en heup, middellijn de diepte in, schouder-/heupas dwars erop, poten als lijnen; `docs/concept/sprites/olinguito/ronde13/bron/constructie.py`), dan pas pixels. Vaak hoeft er weinig opnieuw: hier ging de bestaande dichtbije achterpoot ongewijzigd 9 px naar rechts en alleen de onderkant van de romp en de verre poot werden nieuw getekend.

## 21. Lessen uit alpaca ronde 12
- **Witte/crème vacht: hue-shift, niet "donkerder beige".** Gemeten Gen 3: Altaria/Swablu wit→lavendel (200,200,224)→152,152,192→paarsblauwe rand; Zangoose wit→lichtblauw→grijze rand; Mareep/Ponyta crème→oker→bruin (warm, verzadigder). Kies koel óf warm en houd ±40–50 luma per stap; de referentietabel staat in `docs/concept/sprites/alpaca/ronde12/NOTITIES.md`.
- **Palet wisselen kost niets als de letters vast liggen** (W w v u V): eerst vormen tekenen, daarna de kleuren in `palet.txt` stellen tot de stappen op 1× uit elkaar liggen.
- **Een pompon/kuif in dezelfde vachtkleur leest pas als bol** met een eigen omlijning en een donkere onderrand (u) op de kruin; zonder die rand smelt hij met de kop.
- **Een vuist op een horizontale onderarm leest als een stok met een bal** (rammelaar); zet de vuist dicht op de borst met een wolpluim als overgang, dan groeit hij uit het lijf.
- **Wol is mat:** een witte glanspixel maakt een wolbal plastic; gebruik alleen de hooglichtkleur van de groep en één vouwlijn voor textuur.
- **Een snuit van 1 px naar voren** (3 rijen op x−1, nabije rijen erboven/onder op de oude rand) maakt van een vlakke koprand een muil zonder het oppervlak op te blazen.
- **Heredoc-Python in een worktree-agent kan geweigerd worden;** zet bewerkscripts als bestand in de scratchpad en draai ze met het pad als argument.

## 22. Lessen uit olinguito ronde 14
- **Een romp leest rechthoekig als de buiklijn vlak loopt en de achterkant verticaal valt.** Laat de onderrand vanaf de diepe borst met toenemende stappen per rij (4,3,2,1) naar een hoog ingetrokken lies stijgen en rond de heup af met stappen 2,2,1,1,0,1; zet de achterpoot zó dat de dij de achterkant van die boog vormt (Mightyena).

## 23. Lessen uit alpaca ronde 13 (combineren)
- **Wat Jordi goedkeurt, blijft letterlijk staan:** "meer Pokémon" uitvoeren in palet/shading/details, nooit door goedgekeurde verhoudingen (kop, nek, pose) te veranderen; ronde 12 werd daardoor "Chernobyl" (Jordi).
- **Een pose-wijziging die niemand vroeg eerst als variant opleveren,** niet als enige versie.
- **Kop van ronde X op lijf van ronde Y:** neem de neklengte mee met de kop en laat het lijf beginnen waar de rug start.
- **Glans hoort binnen het zwart:** een glanspixel op de rand van een klein oog laat het oog grijs lezen; een 2 px breed verre oog helemaal zwart.
- **Twee vuisten naast elkaar:** één kolom lucht ertussen, anders één klomp op 1×.

## 24. Lessen uit de Cuyby-evolutie ronde 4
- **Lees de randmelding van `bouw9` echt na vóór je "geen open randen" noteert:** ronde 3 meldde 19 open pixels (lichte spriettoppen, d/q op de schaduwkant) terwijl de notities "ok" zeiden. Lichte toppen krijgen r erboven, schaduwkant K eronder; controleer frame 2 apart, want een deel dat opzij wuift legt de voet eronder bloot (r op de rij erboven in het stilstaande deel).
- **Na een knip de bron terugschrijven naar eindcoördinaten** (`cuyby_evo/ronde4/bron/omzet.py`: het geknipte `delen.txt` terug naar run-length-rijen, gecontroleerd met `cmp` op het raster): dan zijn keuring, raster en bron gelijk en is elke reparatie één getal in plaats van omrekenen.
- **Een gezicht "meer in de vacht" = de lokken van de pony onderaan laten ombuigen naar omlaag over de bovenkant van de snuit, en een wangetje haar tussen snuit en vlek;** de snuit hoeft dan maar 1–2 px smaller voor de helft minder wit. Proef zulke blokken eerst als overlay op het raster (`cuyby_evo/ronde4/bron/proef.py`: legt `proef_blok.txt` over `raster_f1.txt` en rendert 12×/3×/1×), daarna pas in de delen.

## 25. Lessen uit olinguito ronde 15 (lijf op een echt skelet)
- **Een eigen constructie (ovalen, boon) blijft geometrisch lezen, hoe glad de pixels ook zijn;** het lijf van een echte sprite als onderlaag (`onderlaag.py`, niet geschaald) geeft in één ronde een natuurlijke romp en een consequente, staande pootstand.
- **Kies het skelet op houding én verhouding, niet op soort:** Poochyena (stil, laag, kleine romp, korte poten) past beter bij een kleine marter dan Mightyena (te hoog) of Persian (loopt).
- **Neem van de onderlaag de anatomie, niet de vacht:** staartpluim en nekkraag weglaten in het masker, anders tekent de overtrek vachtpieken als rugvorm.
- **Run-lengtes vooraf uitschrijven per curve** (bijv. rug 4,3,2,2,1; buik 4,4,3,2; kont 2,4,3) en daarna de rijen tekenen: zo zie je knikken vóór het bouwen en blijft bouw9 schoon.
- **Een romp die onder een bewegende arm doorloopt, krijgt op de verborgen randpixel al de omlijning** (hier (26,47) = 0), anders verschijnt in frame 2 een open rand.

## 26. Lessen uit de keuring van olinguito ronde 15
- **Toon/helderheid vergelijken met soorten van hetzelfde type** (Jordi): een donker Dark-type mag donkerder zijn dan Normal-referenties (Sentret, Ursaring). Blijf de lumameting wel doen, maar beoordeel tegen Dark-types (Umbreon, Houndour, Sneasel, Poochyena, Murkrow, Absol).
- **Doos-kop, band-masker en brilogen lezen als fakemon:** kop met vlakke top/rechte achterkant/rechte kin, een rechte maskerrand en rechthoekige ogen in een zwarte lijst. Gen 3: ronde kop, maskerrand met een curve, bovenlid donkerst.
- **Een kenmerk moet op 1× leesbaar blijven:** een staart als buis met een haakje van 3 px verliest het kenmerk; laat hem taps toelopen met een duidelijke haak.
- **Bewaak het gekozen concept tijdens reparatierondes:** de olinguito dreef in 15 rondes weg van concept B naar het silhouet van de eigen fase-2-schets.

## 27. Lessen uit olinguito ronde 16 (kop, masker, staart)
- **Schedel als lijst van (y, links, rechts) met regels voor de vulling, details als overlay-segmenten** (`bron/kop16.py`): de omtrek valt in één oogopslag te controleren op runs, en masker/ogen/snuit liggen er los bovenop. Sneller en foutlozer dan hele rijen tellen.
- **Een staart met de hand per rij (links, rechts) uitschrijven**, niet met een formule: afronden gaf telkens rechte stukken van 5–6 px.
- **Een donker masker op een donkere kop wordt leesbaar door wat eromheen ligt:** basis/hooglicht rond de vleugel (schaduw naar de uiterste 2 px van de achterkant), crème wang die onder het oog omhoogkomt en wenkbrauwboogjes. Het lijf hoeft niet lichter.
- **Een haak leest op 1× pas met lucht in de bocht** (≥ 2 px) en een punt die terug omlaag wijst; een haakje van 3 px zonder gat leest niet.
- **Oorvoet aan de schaduwkant:** de onderste rij van een oor dat over de schedelomtrek steekt, eindigt ook met de omlijningskleur, anders ontstaat een open rand waar oor en schedel samenkomen.

## 28. Lessen uit olinguito ronde 17 (staart, neus tussen de ogen)
- **Een neus in de donkere maskerband verdwijnt:** zwart (16,12,18) naast masker (44,28,28) heeft te weinig contrast. Een inham van 1 rij crème boven de neus scheidt ze, en de maskerrand houdt zijn golf.
- **3/4-kop: controleer de neus tegen de oogmiddens**, niet alleen tegen het kopsilhouet. Als de neuspunt buiten de twee oogmiddens valt, leest de kop als profiel, hoe goed de ogen ook in 3/4 staan. Meet het met lijnen op 6× (compare.png, onderste rij).
- **Geen ogen in 3/4 op een profielsnuit:** oog-as en snuit-as moeten dezelfde richting hebben. Bij een korte snuit (kinkajoe, olinguito) ligt de neus 1–3 rijen onder de ogen, tussen de ogen.
- **Een hangende staart naast een lijf: houd de punt ook in het tweede frame los** van de dij. Een staart die in frame 2 omhoogveert (−1), zou hier de dij raken (punt y45 x52 naast de dij op x51). Een staart die omlaagzakt (+1) blijft vrij en geeft een natuurlijke tegenbeweging.
- **Zak en haakgat samen geven de lucht:** de ruimte tussen romp en staart die doorloopt in het gat van de haak, leest op 1× als één bocht. Elke binnenrand van dat gat moet omlijningskleur hebben (bouw9 vangt het).
- **Staart als rijen van 16 tekens (x48–63) met de hand uitgeschreven**, gecontroleerd met `assert len == 16`: sneller en foutlozer dan segmenten tellen.

## 29. Les: "een klein beetje" is letterlijk (olinguito ronde 17 → 18)
- **Een kleine correctie van Jordi = een paar pixels, nooit een herbouw.** "Neus een heel klein beetje naar rechts" werd 11 px verschuiven plus wang dichtmaken: "Chernobyl". Geef de agent een pixelbudget (bijv. < 10 px gewijzigd), laat hem tellen, en lever 1 px/2 px als varianten.

## 30. Lessen uit olinguito ronde 19 (één oog, kleinere kop)
- **Eén oog bij een snuitdier = de snuit herbouwen, niet het oog weghalen:** de snuitbrug moet schuin naar de neuspunt lopen (1 px per rij) en het verre oog zit achter die brug. Crème brug tussen neus en masker houdt de neus leesbaar.
- **Verkleinen zonder schalen:** een kop opnieuw typen in de gemeten verhouding (kop ±35–40 %) en het lijf inkorten door 1–2 kolommen te knippen waar romp en dij recht doorlopen; daarna alleen de knipnaad repareren (omlijning dij/achterpoot).
- **Frame 2 per pixel afleiden uit de beweging van de vorige ronde** (welke pixels schoven, welke bleven staan) en de verre achterpoot expliciet stil houden; anders ontstaan halve poten op de knipnaad.
- **Studie meten met kopkaders op 3×** (studie.png) geeft in één blik of een kop te groot is: 43 % → 36 %.
- **PNG altijd met transparency=0 opslaan:** ronde 19 werd zonder transparantie opgeslagen, waardoor de groene index-0-achtergrond zichtbaar was.

## 31. Lessen uit olinguito stap 1b + ronde 20
- **Bevroren delen als masker-functie in het bouwscript** (kop per rij tot de achterste omlijning, staart als rechthoeken). Plak ze als laatste laag letterlijk terug en controleer met dezelfde maskers in `check.py`. Zo is pixeldiff 0 per constructie te bewijzen.
- **Een frame-2-animatie per onderdeel:** zoek eerst per onderdeel de verschuiving tussen de frames (hier kop/voorpoten −1, staart +1, lijf 0). Neem bij het letterlijk overnemen het onderdeel uit **hetzelfde frame** van de bron, want de staart van stap 1b is in frame 2 niet exact verschoven (3 px verschil).
- **Bij een verschoven kop in frame 2 gaat de borst eronder mee**, anders ontstaan gaten en open randen onder de kin.
- **Sandslash-klauwen letterlijk overnemen:** knip de hand uit (x4–14, y34–45), laat de gele arm weg en vertaal de 5 klauwtinten. Gebruik een middentint (a) voor crème, anders verdwijnt de scheidingslijn en lezen 2 klauwen als één witte vlek. Van de verre klauwen alleen de punten tonen, met een omlijningsrij erboven.
- **Een uiteinde dat niet kan meeschuiven** (de lobpunt zou op de bevroren kaak vallen): eindig de vorm op de nieuwe plek en maak de oude plek vacht. Een los lijntje dat dan overblijft, wordt ook vacht, anders blijft er een donker stipje over.
- De Read-weergave van grote PNG's is grof. Controleer pixelposities met een tekstraster, niet op het oog.

## 32. Lessen uit olinguito v2 (3D-poppetje → sprite)
- **Pixel-over van het 3D-poppetje** (`docs/concept/ontwerp/olinguito_v2/scripts/sprite.py`) geeft maat en silhouet (±850 px), maar de automatische omzetting zelf is rommelig (binnenlijnen, vlakke kop). Teken daarna met de hand per deel (`teken.py` + `docs/concept/sprites/olinguito_v2/delen.py`: `(y, x, pixels)`, kop als omtrek-dict met vulregels).
- **Keuringslus met één agent** (via SendMessage dezelfde agent, zodat hij zijn eerdere oordeel kent): 3 rondes van afgekeurd naar goedgekeurd. Typische fails: maskerbalk als rechthoek (moet een gebogen band zijn), vlak oog zonder pupil/irisverloop, kop als kegel zonder stop en snoet, klauwen als identieke rechte strepen (vork), verre achtervoet van 1 rij (telt niet op 1×), ingesloten gaatje van 1 px.
- **Bouwscript controleert nu ook ingesloten gaten** (transparant, niet verbonden met de rand); lucht tussen twee poten is wél gewenst, losse 1-px-gaatjes niet.
