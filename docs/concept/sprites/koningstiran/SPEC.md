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

## Afgekeurd
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
