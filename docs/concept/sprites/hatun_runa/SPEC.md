# Hatun runa (koningstiran fase 1) – SPEC

Lijn: hatun runa (Normal/Flying) → awki (Fire/Flying) → Sapa Inca (Fire/Psychic, af: `../koningstiran/af/sapa_inca.png`). Zie `docs/concept/POKEMON.md` (Koningstiran-lijn). Werkwijze: **Gemini-model namaken** (`docs/lessen/SPRITE_WERKWIJZE.md`, poedelmot/poedellarve) + `docs/lessen/GEMINI.md` + `docs/lessen/SPRITE_KERN.md`.

## Model (bevroren)
`referenties/model_gekozen.png` = Gemini-ronde 4 (`../koningstiran/gemini/ronde4_startprompt_v3.png`). Kijkt al naar links: niet spiegelen.
Inhoud: grote kiskadie die afzet naar een insect: lijf schuin naar voren, nabije vleugel hoog in de opslag (goudgele onderkant, bruine slagpennen), verre vleugel links achter de kop, opgezette roestbruine staart rechts, snavel wijd open (roze/rode bek), zwarte kruin met gouden vlekje, brede witte wenkbrauwstreep, zwart masker, witte keel, gele buik, donkere pootjes hangend.

## Jordi letterlijk
- (7 nov) "ik vind dit wel iets, hij maakt nu consistent hetzelfde ontwerp, dat betekent dat je prompt goed klopt met welke soort we maken"
- (7 nov) "nee de volgende versie is veel slechter. commit deze maar en hier bouwen we morgen een sprite van"
- (7 nov) "brand maar los met het bouwen van de sprite" / "volg ook de lessen van de poedelmot bouwer, dat ging uitstekend"
- Eerder over de lijn: "ik wil eigenlijk ook een actievere pose [...] ik wil iets anders dan een vogel die weer vooruit poseert zoals zoveel sprites"

## Formaat
Eerste vorm, kleine vroege vogel: model op 48 px breed verkleind = **971 px** (Taillow 838, Starly 767, Wingull 647 bij 58 breed). Silhouet `silhouet/silhouet.png` (`sil.py 48`), bevroren.

## Aandachtspunten (alleen uitvoering, geen ontwerp)
- Kop en oog op 1×: het oog zit in het zwarte masker; volg het model (oog met lichte iris/glans zoals in het model), opbouw van een echt Gen 3-vogeloog.
- Staart rechts: zoals het model (opgezet). Niet veranderen; als hij op 1× als derde vleugel leest: "ter info voor Jordi", niet repareren.
- Herhaalde slagpennen: geen zebra/raster; minder, grotere vormen op de modelplekken (poedelmot-les).
