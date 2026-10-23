# DJ Rotom (Electric/Steel, boombox-vorm): ronde 1

Eerste Gen 3-frontsprite, zelf getekend met de inspiratie (`inspiratie/`, fanart van anderen) alleen als referentie: de vorm, de kleurrol en de noot-antenne. Er is niets overgenomen.

Bestanden: `anim_front.png` (64×128, 2 frames), `normal.pal`, `compare.png` (naast Rotom en de vijf andere vormen zoals ze in de game staan, op 3× en 1×), `zoom.png` (6× met raster) en `bron/`.

## Ontwerp
- **Direct herkenbaar als Rotom-vorm:** het apparaat is Rotom-oranje (dezelfde ramp als Heat, Wash en Frost), de Rotom-kop zit als koepel in het midden met de scheve kuif, en de ogen zijn Rotom-ogen (wit omrand, blauwe iris die onderaan donkerder wordt, zwart bovenooglid). Net als bij alle vormen loopt er een **elektrische gloed van 2 px** rondom (binnen licht, buiten donker) in plaats van een zwarte buitenlijn.
- **Gloedkleur mintgroen** (zoals de inspiratie). Hij verschilt van Rotom (cyaan), Mow (vol grasgroen), Fan (geel), Frost (violet), Wash (blauw) en Heat (rood).
- **Boombox:** een brede, lage kast in driekwart. De voorkant kijkt naar links, de zijkant zit rechts met ventilatiesleuven, de bovenkant is licht. Verder twee speakers (stalen rand, donkere conus, ring, stofkap), een cassettedek met spoeltjes in het midden en een chromen handvat achter de kop.
- **Electric:** de antenne is een plasma-bliksem met een witte kern die in een **muzieknoot** eindigt. Zo heeft hij, net als de andere vormen, een plasma-ledemaat zonder zwarte lijn.
- **Steel:** het chroom van het handvat, de speakerranden, het cassettedek en de stofkappen.
- **Mond = equalizer:** het donkere scherm onder de ogen heeft gloeiende staafjes. Het leest als Rotoms tandengrijns én als een display.
- **Frame 2:** de beat valt. De speakers pompen (ring en stofkap 1 px groter), de equalizer springt naar een ander patroon, de noot wipt op (de kern lost op in de gloed), er gaan twee geluidsgolven uit de linkerspeaker en hij **knipoogt** met het dichtbije oog.

## Werkwijze
`bron/render.py uit.txt` maakt de vormen en shading (`sprlib.py` uit `cuyby/ronde1/bron`). De noot-bliksem is daarin met de hand per pixel getekend (ASCII-raster). `bron/hand.txt` bevat de ogen per pixel (met `bron/patch.py`), en het resultaat staat in `bron/anim_front.txt`. Reproduceren: `render.py r.txt` → `patch.py r.txt bron/hand.txt uit.txt` → `tools/concept/sprites/ascii_sprite.py load uit.txt normal.pal anim_front.png`. Het vergelijkingsvel komt uit `cuyby/ronde1/bron/compare_sheet.py`.

## Palet (indexindeling, §5)
`{'gloed': [1,2], 'oranje': [3,4,5,6], 'staal': [7,8,9], 'conus': [10,11], 'wit': [12], 'oog': [13,14]}`, omlijning 15. In de echte game delen alle Rotom-vormen het kop-oranje en de oogkleuren. Hier staan die ook op eigen indexen (3–6, 12–14), zodat ze gelijk te houden zijn met de andere vormen.

## check.py (`--stage 3`, als grote soort)
- Geen FOUT. Hoogte 58, breedte 56, oppervlak ±2240 (zo groot als Frost en Wash, die ook het vak vullen). 15 kleuren. `.frontPicSize = MON_COORDS_SIZE(64, 64)`, `.frontPicYOffset = 5`.
- LET OP **rand zwart 0 / lichte rand**: dat is de gloed rondom, zoals bij alle Rotom-vormen.
- LET OP **licht boven** en **binnenlijnen zwart 0,13**: de lichte bovenkant van de kast, en de zwarte lijnen tussen kast, speakers, deck en kop (boxy apparaat).
- LET OP **verschil frame 1-2 0,09**: Rotom-vormen bewegen vooral in hun plasma; hier zijn het de speakers, de equalizer, de noot, de golven en de knipoog. Op 1× is het subtiel.

## Wat ik zelf nog zwak vind
- **Te stijf en te recht** naast de andere vormen. Heat, Wash en Frost staan schuin en hebben bollere, 'levende' vormen; de kast is hier een strak blok. Een paar graden kanteling, of een iets bollere kast (afgeronde hoeken, bolle speakers), maakt hem levendiger.
- **Weinig plasma:** de andere vormen hebben grote plasma-armen (Heat, Frost, Wash). Hier is het alleen de antenne. Mogelijk: plasma-'koptelefoon' of handen die aan de knoppen draaien.
- **De ogen** zijn nog wat klein en braaf voor Rotom (die kijkt ondeugender, met scherper schuine leden).
- **De kop-koepel** gaat met een zwarte lijn over in de kast. Bij Frost zit het gezicht ín het apparaat; bij ons kan de koepel nog meer in de kast opgaan.
- **Wit (12)** wordt gedeeld door de oogwitten, de kern van de noot en de spoeltjes. Voor kleurvarianten moet de plasmakern later een eigen index krijgen.
- **Gloed:** de mint is vrij licht, waardoor de buitenrand op een lichte achtergrond wat wegvalt. Een donkerdere buitentint (zoals bij Mow) maakt het silhouet scherper.
- Back en icoon ontbreken nog.
