# Altiplano (hoogvlakte rond de startstad): concept-tileset

Secondary bij de General-primary (paletten 6–12). Opnieuw maken: `python3 tools/concept/tiles/altiplano_tiles.py`
(vaste seed, hulpjes in `tools/concept/tiles/tilelib.py`). Nog niet in de game; geen kaarten.

## Bestanden
Zelfde opzet als `la_paz/`: `tiles.png`, `palettes/`, `metatiles.bin`, `metatile_attributes.bin`, `metatile_names.json`,
`sheet.png`, `tiles_sheet.png`, `paletten.png`, `mockup.png`/`mockup_2x.png` (30×20) en `vergelijking.png`
(naast een stuk Route 111 op dezelfde schaal).

## Wat erin zit
- **Grond (palet 6):** goudgele aarde (4 varianten: kaal, droge sprietjes, kiezels), onverharde weg als autotile
  (9 randstukken + 4 binnenhoeken), bofedal (drassig kussenveen) als autotile met twee poel-varianten, lage richel
  (springen naar het zuiden, `MB_JUMP_SOUTH`).
- **Planten (palet 7, als bovenlaag op de aarde):** ichu als hoog gras (`MB_TALL_GRASS`: vier pollen per vak),
  losse ichu-pol, grote ichu-pol (2×2), tola-struik, yareta (kussenplant), roze bloempjes (cantuta); elk ook op de
  aarde met sprietjes.
- **Steen (palet 8):** losse steen, kei (2×2) met korstmos, lage rotsheuvel (4×3), pirca-muurtjes (horizontaal met
  uiteinden, verticaal, vier hoeken), houten poort van de lamakraal, apacheta (stenen stapel op een pas, 1×2).
- **Adobe (palet 9):** strodak (2 rijen, l/m/r), adobe-muur (2 rijen) met deur (blauw geverfd), raam; huisjes van
  elke breedte. Rond voorraadhuisje met kegeldak (2×3).
- **Queñua (palet 10):** grote boom (2×3) met kronkelige rode schilferstammen en kleine donkere bladtrossen, en een
  kleine (1×2).
- **Verre bergen (palet 11):** herhaalbare besneeuwde keten (4×3) voor de rand van een kaart.
- **Palet 12 is vrij** (bijv. voor de zoutvlakte of een lagune later).

## Budget
- **307 / 512 tegels, 121 / 512 metatiles**, 6 van de 7 paletten in gebruik.
- Per onderdeel (tegels): rotsheuvel 41, pirca 28, adobe 28, queñua 28, bergen 28, bofedal 23, ichu 22, weg 20,
  voorraadhuisje 19, aarde 16, kei 16, strodak 10, apacheta 8, rest 20.
- Ruim 200 tegels over: genoeg voor bijv. een kapelletje, een refugio/berghut, lagune-oevers of een tweede rotsstijl.

## Hergebruik en credits
- Alles zelf getekend; geen tegels van anderen. De rotsheuvel volgt de vorm van de General-rotsen (brokken).
- Water, gras en bomen uit General blijven bruikbaar; de rotsbergen van Route 111 (General) passen qua stijl naast de
  goudgele aarde (zie `vergelijking.png`), al zijn ze rozer dan onze grijze steen.

## Wat ik zelf nog niet goed vind
- **Rotsheuvel** leest nog als een grijze wolk: te weinig donkere voet en geen duidelijke grondschaduw. Een versie met
  de General-rotsvorm (zoals Route 111) en een platte, begaanbare top zou beter passen.
- **Bofedal** heeft rechte randen (autotile) en een vrij gelijkmatig patroon; echte bofedales zijn grillig en
  glinsteren. Grillige randstukken en een paar geanimeerde poeltjes (tilesetanimatie) zouden helpen.
- **Pirca-hoeken** zijn functioneel maar hoekig; een ronde lamakraal (zoals ze echt zijn) vraagt nog schuine stukken.
- **Ichu-velden** zijn nog vrij gelijkmatig; een tweede hoog-gras-variant (andere pollenstand) tegen herhaling.
- **Aarde** is erg egaal: goed voor de rust, maar op een grote route misschien saai. Meer subtiele varianten
  (scheurtjes, kiezelplekken, schapenpaadjes) kosten weinig.
- **Bergketen** is regelmatig (twee toppen per 4 vakken); voor een vergezicht met variatie een paar losse toppen
  erbij, en de Illimani uit de La Paz-set past hier ook (ander palet nodig).
- Er zijn nog **geen kliffen/terrassen** voor hoogteverschil anders dan de richel; die horen bij de eerste echte route.
- Geen dieren in de tegels (lama's, vicuña's): dat zijn Pokémon/NPC's als objecten (immersie).
