# Koningstiran (eindvorm "Sapa Inca") – SPEC

Werkwijze: `docs/lessen/SPRITE_WERKWIJZE.md`. Lijn en inspiratie: `docs/concept/POKEMON.md` (Koningstiran-lijn), brainstorm in `IDEEEN.md`, richtingsschetsen in `docs/concept/ontwerp/koningstiran/`.

## Jordi letterlijk
- (5 nov) "daar moeten we zeker een pokemon van maken, die daar op lijkt met zon inca hoofdtooi"
- (5 nov) "belangrijk is dan wel dat we de sprites van zeker de derde vorm zo maken dat je de kop toch redelijk van de voorkant kan zien, of grotendeels, mogelijk van de tweede ook"
- (5 nov) "en de kroon moet lekker imposant groot zijn"
- (5 nov) "ik ben het eens met de a opties" (pose A: rustig staand, kop driekwart naar voren)
- (5 nov) "dit is een klein vogeltje, maar misschien kunnen we de vogel zelf wat groter maken [...] dat we een hybride vorm maken" → Claude stelde de bergcaracara voor; Jordi stuurde een foto van een bergcaracara (akkoord).
- (5 nov) "sapa inca moet dus niet helemaal frontaal staan, want dat is geen enkele sprite. Laten we nadenken over een pose, doe sprite onderzoek. We beginnen met deze pokemon maken en dan gaan we terugwerken"

## Volgorde
Eindvorm eerst (FAKEMON_DESIGN principe 1), daarna terugwerken naar awki en hatun runa.

## Onderdelen (status)
| Onderdeel | Bron/referentie | Status |
|---|---|---|
| Silhouet | `silhouet_v1_vel.png`, `silhouet_v1_1x.png` (1560 px; Gen 3-ref. 1033–1825), direct uit het poppetje B3 | v1: wacht op Jordi |
| Pose | groep A uit `referenties/pose_onderzoek.png` (Noctowl, Empoleon, Squawkabilly, Rufflet) | **gekozen: A** |
| Bouw | **hybride met de bergcaracara** (*coraquenque*, de kroonveervogel): groot, rechtop, lange poten, haaksnavel; `referenties/bergcaracara_foto.webp` | gekozen; details open |
| Kroon (waaier) | echte koningstiran: rood, staalblauwe punten, zwarte band; imposant | open |
| Franje (mascaypacha), oorschijf, tocapu-borst | schets v2 | open (uit de veren laten groeien, geen hoed) |
| Lijf, staart, kleuren | echte koningstiran: bruin, okergele borst, rossige staart | open |

## Pose-onderzoek (Claude, 5 nov)
- Gen 3-vogels met kop van opzij (Swellow, Staraptor) tonen een dwarse waaier als een streep: dus **kop driekwart** (beide ogen, snavel naar linksonder), het lijf meer opzij dan de kop (olinguito-les).
- Grote kronen in echte sprites: Noctowl, Empoleon, Pyroar, Kingambit, Slowking. De kroon staat breed op de kop, de verre helft iets korter; bij Kingambit/Pyroar is de kroon het grootste vlak en loopt hij tot de rand van het vak.
- Voorstel: **A+B**: rechtop zittend als Noctowl/Empoleon, borst vooruit, vleugels gevouwen als een mantel, staart schuin naar rechtsonder; kop ±30° van frontaal, iets omhoog; waaier ±40–45% van de spritehoogte.
- Frame 2 (later): kop een fractie zwaaien en snavel open (oranje keel), zoals de echte balts.

- (5 nov) "dit is gewoon weer een t-pose" / "hij mag wat swagger tonen, het is een koning" / "we hadden afgesproken dat de pose zou lijken op bijv empoleon" / "het model is verder prima, dus niet opnieuw bouwen, gewoon aanpassen" / "de vleugels gaan we ook niet statisch t-pose doen"
- Pose-ronde 2 (pop3d.py): Empoleon-houding: borst vooruit, iets achterover, verre vleugel geheven met gespreide slagpennen (gebaar), nabije vleugel als mantel naar achteren-omlaag, brede stand.

- (5 nov) "horen de handen zo gevederd te zijn? dat lijkt meer op een danser dan echt een koning toch" → pose-ronde 3: vleugels gesloten en massief (Empoleon-flippers), verre vleugel gebiedend schuin naar voren-omlaag, nabije als gesloten mantel.

- (5 nov) "hoort die zo dik te zijn? En nu zijn we gewoon poses van vleugels aan het gokken ook. Het is ook weer te recht. Zou die niet meer een nonchalante koningspose kunnen aanhouden?" → gokken gestopt (werkwijze: na 2 mislukte poserondes een echte bron); kandidaten in `referenties/nonchalant.png`, Jordi kiest het skelet.

- (5 nov) Jordi stuurt het Pachacútec-beeld (Cuzco, `referenties/pachacutec_beeld_cuzco.webp`): "doe deze pose qua vleugels, dus eentje wijst half de lucht in, de ander gewoon zoals decidueye bijv" → pose-ronde 4: nabije vleugel gesloten en half omhoog naar buiten (rechts in beeld, voor de kroon langs), verre vleugel gesloten hangend (Decidueye), contrapposto (standbeen + verre poot naar voren en hoger), slanker lijf.

- (5 nov) "dat die zijn eigen staart vasthoudt als scepter is wel komisch, b3 lijkt wel ok. Wederom is wel de vleugel weer een rechte lijn, daar mag iets meer dynamiek in zitten, evenals dat de benen in een v-pose staan" → **hoek B3 gekozen** (lijf 44°, kop 76°); pose-ronde 5: knik in de pols van de opgeheven vleugel (arm naar buiten, pennen omhoog, bolle achterrand), 3 buigingen; standbeen recht, vrije poot met gebogen knie. Staart-als-scepter: nog open.

- (5 nov) "de vleugel mag ietsje korter, 1 is wel het beste. De poten zijn nu wel wat te lang voor het lichaam denk ik, misschien het lichaam iets verder naar beneden en de poten iets korter" → **buiging 1 gekozen**; vleugel ±20% korter, poten ±10 korter (lijf zakt), staart mee omhoog.

- (5 nov) Staart als scepter: **ja** (Jordi; Claude had het eerst ten onrechte weggelaten). Eerste opzet: lange middelste staartveer onder het lijf door naar voren, rechtop naast de verre vleugel, pluim bovenaan.

- (5 nov) Krabbel van Jordi (`referenties/krabbel_jordi_staart_arm.png`): "een beetje zoals de oranje streep, klein stukje achter de poot door en dan voorbij de poot komt die weer naar boven, en rode streep is vanaf rechts een stukje van de bovenarm wat korter mag" → staart en bovenarm zo aangepast. "en spiegelbeeld mag".

- (5 nov) "de benen staan voor de staart, de staart gaat achter de benen door langs het lichaam de hand in" / "op die manier ja, maar nu ziet het er niet mooi uit" / "het moet staart en scepter zijn en als dat niet lukt dan doen we het niet" → in deze pose leest het niet als scepter (balk op heuphoogte, of een lange sliert): **scepter vervalt**. Gewone roestbruine staart, rechts achter het lijf, achter de poten. Vleugels niet gespiegeld ("mag" = toestemming).

- (5 nov) "de linkerbovenarm is veel groter dan de rechter [...] de poten onnatuurlijk [...] 1 is een stuk langer dan de ander, klopt dat met het bronmateriaal?" → nee: op het beeld zijn de benen even lang (dij onder het lijf, voorste been gebogen en hoger). Benen nu even lang (±21) onder het lijf; linkervleugel smaller (bovenarm even dik als rechts).

- (5 nov) "maak maar een silhouet" → v1 direct uit het poppetje verkleind (massa heilig), geen reparaties. Eigen keuring: twee plekken waar delen tegen elkaar plakken op 1x (opgeheven vleugel tegen de kroonrand; standbeen tegen de staart); rechter kwastje valt achter de vleugel. Varianten (vleugel verder naar buiten) losten het plakken niet op en verborgen de staart: niet doorgestuurd.

- (6 nov) Kleur ronde 1 (maker) → eigen keuring: gezicht klein/boos, vleugel knots, borst plat ei, staart weg → ronde 2 (alleen kleur, silhouet bevroren, kroon bevroren). Ronde 2: gezicht rustiger, vleugel met penscheidingen, borst met volume, staart gescheiden. Resterend (zit in het silhouet): kop 11×9 px (ogen 2–3 px), vleugel leest als opgeheven arm, staart 2–3 px breed. Voorgelegd aan Jordi.

- (6 nov) Jordi over ronde 2: "Ik vind dit al heel netjes. Laten we hier morgen verder aan werken". Aanvulling: "Nog niet perfect hoor, maar heel ver al". Open voor morgen: de drie silhouetvoorstellen (kop groter, vleugelpunt, staart).

- (7 nov) "ik vind de kroon en het gezicht erg mooi, veel mooier als in het model, evenals buik en poten. [...] Het lichaam leest nog niet helemaal goed door positie van de poten. Hij staat in een juiste pose, maar linkeronderkant lichaam plus de linkerpoot zien er een beetje gekkig uit. Hoe het lichaam daar opeens ophoudt. De armen zijn nu een stuk beter en de hoofdtooi is subliem, nu lijkt het patroon misschien wel iets teveel op een watermeloen, is dat true to form? Gezicht mogelijk iets te klein, maar het gezichtsidee is wel goed. Daarnaast wil ik toch nog kijken of we in de linkerarm die nu naar beneden hangt, of die iets hoger kan hangen en daar een staf in kan"
  → Bevroren (kleur): kroon, gezicht(sidee), buik, poten. Open: linkeronderkant lijf + linkerpoot, kroonpatroon minder watermeloen, gezicht iets groter?, linkervleugel hoger met staf.

- (7 nov) Staf B (gouden zonneschijf) + krabbel `referenties/krabbel_jordi_staart_is_staf.png`: "We halen de echte staart weg en geven daar een kleine indicatie waar de staart het lichaam uitkomt en heel licht afbuigt. De staf buigt vervolgens af en heel licht zie je dat die naar het lichaam gaat. En tahdah de staart is de staf geworden." / "hij gaat nergens over de lichaamsdelen heen die we al hebben" → poppetje: gouden staartstukje rechtsonder achter het standbeen; staf buigt onder de hand naar het lijf en verdwijnt erachter; hangende slagpennen korter zodat dat stuk zichtbaar is. Silhouet v2 (`silhouet_v2_vel.png`).

- (7 nov) "bijna, dit sluit niet mooi aan. Allereerst houdt hij de staf niet meer vast, de arm is weg om een of andere reden. De staf mag nog wat hoger achter het lichaam komen. De staart staat juist de verkeerde kant op" / "als in waar de staf staart wordt mag ietsje hoger" → arm zichtbaar (elleboog links naast het lijf, vleugelpunt om de staf), staf verdwijnt hoger achter het lijf, staartstukje uit de stuit omlaag en dan naar links achter het standbeen.

- (7 nov) Krabbel `referenties/krabbel_jordi_staf_krul.png`: rood kruis over het staartstukje rechts (weg); geel: staf krult onderaan af bij de buikrand, en een piepklein krulletje onder het lijf tussen de poten. "verder is de vleugel een beetje in tweeën gesplitst links. Het hoeft maar een hele subtiele link te zijn, het feit dat de staf afkrult is al een hint" → zo gedaan; linkervleugel één doorlopende vorm.

- (7 nov) "nee je volgt mijn instructies niet op. De staf verdwijnt nu nergens heen, die moet afbuigen naar het lichaam toe. De staart is nu ook onderin verbonden met de poot?" → staf buigt onder de hand naar het lijf en verdwijnt achter de DONKERE flank (gemeten: rechts/onder van het zichtbare eind ligt lijf, niet de gele buik); krulletje tussen de poten met 1 px lucht naar beide poten op 1x (rij 57).

- (7 nov) Krabbel `referenties/krabbel_jordi_staf_punt.png`: "Het moet gewoon een puntje zijn, zodat je kan zien dat er een staart hangt, hij moet niet een verbinding maken naar iets wat niet bestaat" / "al kan de staf links goed zijn, zolang we het lichaam fixen, want die is niet goed in vorm nu" / "nee houd de staf links maar zo" / "puur tussen de poten" / "en het lichaam linksonderin moet meer opgevuld" / "maar laten we aub weer naar de sprite gaan want dit is echt zinloos werk" → terug naar de pixels (ronde 3 op ronde 2), poppetje alleen als onderlaag voor de staf (`poppetje_staf_256.png`).

- (7 nov) "en het uiteinde van de staf plus de staf zelf mag ook wat kenmerken van een staart hebben, dus een hybride idee" → aan de maker doorgegeven (ronde 3).

- (7 nov) "het zijn echt kleine aanpassingen van de sprite die we eerder hadden, die moet echt als leidraad" → ronde 2 is de basis; alleen verplaatsen/toevoegen wat nodig is.

- (7 nov) "moeten wel bijv nog het patroon/kleurgebruik in die kroon aanpassen maar dat komt nog" → kroonpatroon/kleur later, aparte ronde.

- (7 nov) Ronde 3 (maker, op ronde 2): kroon/gezicht/buik/poten/rechtervleugel 0 px gewijzigd; linkervleugelpunt verschoven om een staf (hybride: gouden schacht, roestbruine vaan, zonneschijf 5×5), lijf linksonder opgevuld (+22 px), bruine staart weg, gouden puntje tussen de poten (1 px lucht). Open: zon/staf klein, puntje hangt los, hand leest als vuist. Voorgelegd aan Jordi.

- (7 nov) "dat gefrummel tussen die benen, geen idee wat je daar weer gedaan hebt. Daar moet helemaal aan de bovenkant tussen de benen heen een hele lichte hint van een start van een staart zijn, niks anders." / "het hoeft niet los van de poten" → hangend puntje weg (8 px); 2 px roestbruin/rood bovenaan in de kruising (54,28 t; 55,28 r). Afgekeurde versie: `ronde3/sapa_inca_puntje_afgekeurd.png`.

- (7 nov) "de vleugel om de staf heen mag iets minder recht, iets meer als de vleugelvorm die we hanteren. De staf mag nog iets meer op een staart lijken. Linkerpoot sluit niet lekker aan op het lichaam tov de rechter, gezichtis nog net iets te klein." → ronde 4 (maker).

- (7 nov) "gaat vooral om de ogen die moeten pokemon stijl zijn, mogen klein hoor, maar wel duidelijk pokemon stijl" → maker: oogstudie Gen 3-vogels (Honchkrow, Murkrow, Corviknight, Staraptor, Swellow, Talonflame), ogen volgens die opbouw.

- (7 nov) "hij heeft daar wel iets te lieve ogen" → trots/zelfverzekerd, niet boos en niet lief (maatstaf Staraptor, Honchkrow, Braviary).

- (7 nov) Ronde 4 (maker, op ronde 3): linkervleugel met knik en bolle achterrand om de staf; staf taps (3→5 px) met vaan aan beide kanten; linkerpoot opgebouwd als de rechter; ogen opnieuw (goud, hoog onder een vlak lid, glans; gezicht zelfde maat). Kroon/buik/rechterpoot/rechtervleugel 0 px. Open: ogen klein, staf meer staf dan staart, staf onder de arm deels verborgen.

- (7 nov) "het is nu niet helemaal duidelijk meer dat hij een staf vast heeft, misschien onderin de staf nog iets meer ervan tonen? zodat de vleugel het grotendeels overlapt maar niet volledig" → ronde 5 (maker).

- (7 nov) "verder vind ik op wat design consistencies na het prima, alleen de hoofdtooi moet nog een iets ander design, misschien de zwarte pixels daar geel maken oid, maar misschien kan je wat variaties tonen" → kroonvarianten A–F (alleen hercoloreren, op ronde 4): `kroon_varianten/kroon_varianten.png`.

- (7 nov) Ronde 5 (maker, op ronde 4): staf komt onder de vleugelpunt weer tevoorschijn (rij 47–49, zelfde lijn en dikte), buigt dan naar het lijf; 24 px gewijzigd, rest 0 px. Open: middenstuk 9 rijen verborgen, bocht leest als knik.

- (7 nov) "nu is er een zwart vlak tussen staf, lichaam en vleugel in wat er niet mooi uitziet" → ronde 5b: zone x17–23, rij 44–52 (d + K-streepjes) laten lezen als vleugelpunt + flank.

- (7 nov) Ronde 5b: zwarte klont weg (45 px binnen de zone, 0 erbuiten); vleugelpunt in vleugeltinten, flank in schaduwtint, zwart alleen als onderrand. Open: vleugelpunt iets lichter dan de bovenarm.

- (7 nov) Krabbel `referenties/krabbel_jordi_lijf_staf.png` (rode lijnen = gewenste omtrek, rood puntje = onnodige bruine pixels): "ja nu heb je er een paar bruine pixels neergezet. De staf is een rechte streep die nog steeds achter zijn vleugel lijkt te zitten, omdat die dus niet over de vleugel heen overlapt, dat moet een klein beetje, totdat die hem vast pakt. Daarnaast is het ook weer een rechte lijn als die achter zijn lichaam verdwijnt, ook niet mooi. Het lichaam zelf is ook niet zo goed, is wat teveel uitgedijt en dus niet mooi een ovalerige afwerking. Plus de gele buik is nu een soort van ballonvorm met tuitje geworden. De poten zijn nog niet netjes afgewerkt qua kleur en schaduw. Ik heb een rood puntje gezet op de onnodige bruine pixels" → ronde 6 (maker).

- (7 nov) Ronde 6 (maker): lijf ovaal volgens de rode lijnen, buik rond (licht druppelvormig), staf vóór de vleugel tot de greep, poten afgewerkt. **Door Claude afgekeurd vóór Jordi:** onder de hand hangt de staf als losse sliert door de lucht → ronde 6b.

- (7 nov) Ronde 6b: geen losse sliert meer; staf 2 rijen zichtbaar onder de vleugelpunt, verdwijnt achter de ronde lijfrand linksonder (die ligt daarvoor 2–4 px buiten de rode boog). 33 px binnen de zone, 0 erbuiten. Voorgelegd aan Jordi.

- (7 nov) "nu is het lichaam links weer net wat teveel weggesneden. en dat maakt gelijk de staf wat gekker, nu kan ik wel zien dat die op de juiste plek naar het lichaam gaat, dus zo slecht is dat niet. Het gele vlak in het midden heeft wel nog steeds een rare vorm, die mag nog wta ronder, aan de rechterkant is het beter, maar mag die nog een klein beetje dunner, we komen dichtbij nu. Poten ook netter afgewerkt" → poten bevroren (goed); ronde 7: lijf links voller, buik ronder en rechts iets dunner.

- (7 nov) "En de bovenkant van de staf moet nog mooier, dat is nu best lelijk afgewerkt, misschien dat we daar een soort van uiteinde van de staart idee van kunnen maken, dat het echt hybride staart en staf is" → ronde 7: stafkop als staartveer-uiteinde/scepterkop.

- (7 nov) Ronde 7: lijf links voller (één bolle boog naar de dij), buik egaal ovaal (breedte per rij 3→12→2) en rechts 1 px dunner, stafkop A = staartveerpunt (5 px smal, naast het kroonkwastje), variant B = zonneschijf uit veerpunt. Poten 0 px. Voorgelegd.

- (7 nov) "nu maak je weer e zelfde fout als eerder, nu is het lichaam aan de linkerkant weer gek uitgebold" → ronde 7b (Claude, 9 px): linkeromtrek linksonder precies tussen 6b en 7 (begin rij 48–53: x16,17,18,20,22,24); rest = ronde 7.

## Afgekeurd
- Staartpoging na de krabbel (5 nov): ging over het been heen, las als een streep, "lijkt niet op een staart, een scepter". "spiegelbeeld mag" ging over de staart, niet over de vleugels ("niet spiegelbeeld"). Wacht op Jordi's antwoord/omtrek.
- Pose-ronde 4: opgeheven vleugel een rechte lijn, benen in een V.
- Pose-ronde 3: te dik, te recht, vleugelpose gegokt.
- Pose-ronde 2: gespreide slagpennen ("danser").
- Pose-ronde 1: stijf rechtop, vleugels langs het lijf, symmetrisch ("t-pose").
- Helemaal frontaal (schets v2 fase 3): "geen enkele sprite" staat zo.

## Foto's van Jordi (5 nov, alleen in de chat binnengekomen; punten overgenomen)
1. Twee video-stills, vogel in de hand, kuif open: waaier halfrond, midden **oranjerood met rijen zwarte stippen**, buitenrand **lavendel-paars met zwarte vlekken**; snavel open, geel-oranje onderkant en oranje keel.
2. Close-up recht van voren: de **zijveren hangen omlaag als kwastjes met zwarte punten**, tot onder ooghoogte (paddenstoel-/parapluvorm, een natuurlijke franje rond het gezicht); snorharen bij de mondhoek, grote donkere ogen.
3. Staande foto (titel "Tropical royal flycatcher"): als 1, van schuin voren.
4. Tekening van een zittende vogel op een tak: **pose A** bijna precies (kop driekwart naar links, waaier dwars op de kop en iets ingekort); olijfbruine rug, okergele borst, lichte stippen op de vleugeldekveren, roestbruine staart.
5. Bergcaracara (wel als bestand): `referenties/bergcaracara_foto.webp`. Zwarte bovenkant en borstband, witte buik en broek, **kaal oranjerood gezicht**, bleekblauwgrijze **haaksnavel**, oranjegele poten met zwarte klauwen; rechtop, kop opzij, eivormig lijf, kleine kop t.o.v. het lijf.

## Nodig
- Kleuren van de hybride (koningstiran-bruin/oker of caracara-zwart/wit): vraag aan Jordi.
