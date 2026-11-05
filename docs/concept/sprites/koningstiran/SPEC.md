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
