# DJ Rotom – kleur1 (frontsprite frame 1)

Op het bevroren silhouet (`silhouet_af/silhouet.png`), kleuren uit de bron, stijl van de game-Rotoms.
Bestanden: `dj_rotom.png` (64×64, geïndexeerd, transparency=0), `normal.pal`, `vel.png`, `bron/`
(`dj_rotom.txt` = het tekstraster, de bron van waarheid; `hand.py` = de eerste handopzet per onderdeel;
`zet.py` = pixelbewerkingen in het raster; `palet.py`, `render.py`, `vel.py`, `controle.py`;
`quant.py`/`bouw_start.py`/`start.txt` = alleen het startpunt, niet in het eindresultaat).

## Game Freak-studie (Rotom, Heat, Wash, Frost, Fan, Mow op 8×, indexrasters)
| onderdeel | wat GF doet | wat ik overnam |
|---|---|---|
| gloedrand | geen zwarte buitenlijn; 2 px gloed: buitenste px donkere gloedtint (Rotom 28a8b8, Frost b050c8), daarbinnen lichte gloedtint, dan meteen het oranje | buiten `1` donker mint, binnen `2` mint; brede gloedzones (onder de linkerspeaker, boven de rechter) helemaal `2` |
| oranje | 4 tinten, in alle vormen gelijk: f8a880 / e87028 / c04818 / 783820, + 101010 zwart | identiek (bron #e2673c ≈ game #e87028, dus game-oranje) |
| omtrek van het lijf | lichtkant (links/boven) c04818 als omlijning, schaduwkant (rechts/onder) 783820 en zwart; zwart alleen onder/rechts en op naden | links/boven `6`, rechts/onder `7`, de onderste hoek rechts `8` |
| kasten (Frost, Wash, Heat) | voorvlak e87028, zijvlak c04818 met een 783820-rand, hooglicht f8a880 als rij langs de bovenrand, licht linksboven | voorvlak `5`, rechterzijvlak `6`, rand `7`; één rij `4` onder de bovenrand, `4`-rand links die naar onder overgaat in `5` |
| spits | 3–4 px breed aan de voet, lichte streep links (f8a880), schaduw rechts, omringd door gloed | punt `6`, lichte streep `4` links, `5` midden, `6` rechts; voet loopt over in het bovenvlak van de kop |
| ogen | ±4×5: wit langs de rand, gekleurde iris 2 breed die bovenaan de rand raakt, zwarte pixel links/rechts in het midden ("8a9 / 8bb8 / 7bb7 / 8bb9") | iris `c` donker boven, `d` licht onder, wit `f` rondom, zwart `8` links/rechts; verre oog 3 breed (3/4) |
| tanden/mond | Mow/Heat: witte tanden tussen zwart, 1 px | grijns `7fff7` / `777` |
| plasma | Rotom: donkere rand, middentint, lichte kern (b8f0e8) en wit in het hart | bliksem: rand `1`, vulling `2`, kern `3`, witte noot `f` |

## Palet (16, index 0 transparant; alles exact 15-bit)
| idx | groep | kleur |
|---|---|---|
| 0 | transparant | 98d0a0 |
| 1–3 | gloed/plasma: donker, midden, licht | 41a47b, 83d5a4, c5f6d5 |
| 4–7 | oranje (= game-Rotom): hooglicht, basis, schaduw, donker | f6a483, e67329, bd4a18, 7b3920 |
| 8 | zwart (conussen, display, snoer, onderhoek) | 101010 |
| 9–11 | speaker: front navy, conusring/stofkap-rand, glans | 182031, 39415a, a4acbd |
| 12–13 | iris: donker, licht (blauwgroen uit de bron) | 3994a4, 73cdd5 |
| 14 | equalizer groen | 31d594 |
| 15 | wit (noot, tanden, oogwit) | f6f6f6 |

## Onderdelen (plaats volgens onderlaag / bron_vervormd)
- Linkerspeaker x4–19: front x4–13 (navy paneel x6–12, kleine conus boven, grote onder, navy ertussen), zijvlak x14–19 in `6`.
- Kop x21–34: bovenrand met spits (x25–29), voorvlak x21–30 met ogen, grijns, zwart display met groene equalizer; zijvlak x31–34; donkere naad x20 tegen de linkerspeaker.
- Snoer: rij 53 van x19 tot x34, loopt achter het display door naar beide speakers.
- Rechterspeaker x35–59: schuine bovenrand (perspectief), navy paneel x37–53 met twee conussen (9 en 11 breed: ring `a`, zwarte conus, navy stofkap, glans `b` onderaan zoals in de bron), voorrand `5` op x54, zijvlak `6` dat naar onder breder wordt.
- Bliksem: zigzag met een achtste noot (kop 2×2, steel, vlag) in wit; de lichte kern loopt door de stengel naar de spits.

## Checks (script `bron/controle.py`)
- alpha-diff met `silhouet_af/silhouet.png`: **0 px** (1756 px).
- open randen (alles behalve de buitenste gloedtint naast transparant): **geen**.
- losse pixels: **geen**.
- rondreis tekstraster ↔ png: gelijk.
- `tools/concept/sprites/check.py`: draait niet meer (zoekt `HOENN_DEX_TREECKO`, die is weg na de Hoenn-opruiming); niet door mij te repareren binnen deze opdracht.

## Checklist SPRITE_NORM
1. Leest op 1× als echte Pokémon: ja, naast de 6 game-Rotoms leest het als een Rotom-vorm (gloedrand, oranje, Rotom-ogen, spits) en als DJ Rotom (twee speakers, kop-kubus, display met equalizer, bliksem met noot).
2. 3/4 naar links-voor: ja, uit het bevroren silhouet; zijvlakken rechts zichtbaar, verre oog smaller.
3. Ledematen: n.v.t. (apparaat); alle onderdelen van de bron geteld: 2 speakers, 4 conussen, kop, spits, ogen, grijns, display, snoer, bliksem, noot.
4. Geen Escher: overlap klopt (kop vóór het zijvlak van de linkerspeaker, rechterspeaker vóór het zijvlak van de kop, met donkere naad).
5. Lijf over echt skelet: silhouet bevroren; kasten zijn bewust recht (Frost/Wash ook), conussen met de hand rond.
6. Kop: n.v.t. als percentage; de kop-kubus volgt de bron.
7. Ogen geïntegreerd: iris donker boven / licht onder, wit rondom, zwart opzij, zoals de game-Rotom.
8. Kenmerken op 1×: conussen, display en ogen lezen; de noot leest pas vanaf 2×.
9. Omlijning per kleurgroep, licht linksboven, geen open randen: ja (script).
10. Geen Chernobyl: geen zwevende delen; snoer en bliksem zijn verbonden.

## Wat nog niet (helemaal) klopt
- De witte noot is op 1× een witte vlek in de bliksem; als noot leesbaar vanaf 2×. Groter kan niet binnen het bevroren silhouet.
- De kop-kubus is smal (voorvlak 10 px) door het silhouet; ogen en display staan daardoor dicht op elkaar. Leest wel als gezicht.
- Het oranje is vlakker dan Heat/Wash (die zijn rond); bewust, want het zijn kasten zoals Frost.
- Het display is kleiner dan in de bron (8 px breed) en de equalizer is een skyline van 6 staafjes in plaats van losse blokjes.
- Smaakvraag voor Jordi: de gloed is bleek mint zoals in de bron; de game-gloeden zijn verzadigder.

## Lessen
- De gloed-buitenrand mag automatisch (1 = grenst aan transparant, anders 2): dat is de GF-regel en geeft nooit open randen; teken alleen het lijf met de hand.
- Een volledig witte ring om een Rotom-oog leest als een bril; laat de iris de bovenrand raken (zoals de game-Rotom).
- Conussen als zwarte schijf met ring lezen als gaten; een navy stofkap met glans onderaan maakt er een koepel van.
- Twee ronde onderdelen boven elkaar: minstens één rij paneel ertussen, anders lezen ze als een "8".
- `check.py` en `spritelib.hoenn_species()` werken niet meer sinds de Hoenn-dex weg is (Claude: aparte taak).
