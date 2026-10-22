# Nachtaap fase 1, ronde 2: "Maanogen"

Bestanden: `anim_front.png` (64×128, 2 frames, geïndexeerd, index 0 transparant), `normal.pal`, `thumbnails.png` (drie silhouetten), `compare.png` (ronde 1 en 2 naast Abra, Espurr, Oranguru, Natu, Elgyem, Hatenna, Munna en Treecko/Torchic/Mudkip, op 3× en 1×, plus de silhouettest op 1× en 2×). Bron: `bron/build.py` (sprite), `bron/thumbs.py` (silhouetten), `bron/compose.py` (vel). De vormen komen uit de nieuwe hulpbibliotheek `tools/concept/sprites/layerlib.py`: lagen van ellipsen en lijnen, automatisch 1 px omlijning met selout en licht van linksboven; ogen, voorhoofdteken en handen zijn met de hand gezet (pixelrijen in `build.py`).

Opnieuw maken: `python3 bron/build.py . && python3 bron/compose.py . && python3 bron/thumbs.py thumbnails.png` (vanuit deze map).

## Silhouetten (thumbnails.png)
- **A, zittend met de staart opzij (gekozen):** grote ronde kop, peerlijf in meditatiehouding, de spiraalstaart rechtop naast de kop. De spiraal breekt het silhouet, zoals de kuif van Torchic of de vin van Mudkip.
- **B, spiraal als halo boven de kop:** het meest symmetrisch, maar in het zwart leest het als een beker of trofee, en een halo trekt naar Fairy of een engel.
- **C, zwevend druppellijf met de spiraal als slinger:** het meest "Psychic-geestje", maar de aap verdwijnt en de spiraal wordt te klein. Dat sluit aan bij de waarschuwing in de kritiek.

## Ontwerp (dier × idee × type)
- **Dier:** een babynachtaap met tarsierproporties. De kop is 54% van de hoogte en zo breed als het lijf met de benen. Hij heeft kleine, laag geplaatste oortjes (de echte nachtaap heeft verstopte oortjes; met grote, hoge oren werd het een Mickey-silhouet) en de witte vlekken boven de ogen van de nachtaap.
- **Idee:** een kleine ziener of genezer in meditatie. De vingertoppen liggen tegen elkaar voor de borst, met magenta kussentjes bovenaan (de handen van de latere healer). Frame 2 heft één hand met gespreide vingers als een zegen.
- **Type (Psychic):**
  - **Ogen:** frame 1 heeft halfgesloten oogleden in vachtkleur met een zachte (niet zwarte) bovenrand. Onderin zitten twee gloeiende **maansikkels** in maan-cyaan, zonder pupil: je ziet niet waar hij kijkt. In frame 2 gaan de ogen **wijd open** tot twee volle, gloeiende manen met een piepkleine pupil. Dat is het schrikmoment ("eng"), terwijl de hand zegent ("lief").
  - **Voorhoofd:** twee symmetrische **zilveren sikkels** boven de ogen (gestileerd uit de witte vlekken van de nachtaap) en in het midden een **magenta edelsteen-ruit** (zoals bij Espeon en Kadabra).
  - **Houding:** frontaal, symmetrisch en mediterend. De benen zijn gevouwen tot een plat zitkussen, met alleen de lange voeten met de tenen naar buiten. Er zijn **geen knieën** meer (Jordi's punt).
  - **Spiraal:** de Nazca-spiraalstaart is groot: ruim 1½ slag (1¾ zoals in de kritiek liet de slagen samenvallen tot ringen), 2 px dik en met transparante ruimte tussen de slagen, zodat het op 1× een spiraal blijft en geen ring wordt. Hij heeft een gloeiende magenta punt. In frame 2 komt hij 1 px omhoog.
  - **Kleur:** lavendel (vacht), zilverwit (sikkels, snuit, borst), maan-cyaan (ogen) en magenta als accent (edelsteen, oren, neus, vingertoppen, staartpunt). Er zit geen zwart met geel of rood in en geen tanden. Daarmee blijft het weg van Umbreon en Noctowl (Dark).
- **Driehoek met de andere starters:** midden-licht en koel (lavendel/zilver) tegenover de lichte, warme alpaca en de donkere, warme olinguito.

## Paletindeling (recept-formaat, §5)
```
'nachtaap': {'vacht': [1, 2, 3, 4], 'zilver': [5, 6, 7], 'magenta': [8, 9, 10], 'ogen': [11, 12, 13], 'wit': [14]}
```
| index | kleur | onderdeel |
|---|---|---|
| 0 | #94cd9c | transparant |
| 1–4 | #ded5f6 #ac9cd5 #7362a4 #41316a | vacht licht→donker (2 = basis; 3 = schaduw, ooglid en lichte buitenlijn; 4 = selout/binnenlijnen) |
| 5–7 | #f6f6ff #bdc5de #8b8bb4 | zilver: sikkels op het voorhoofd, snuit, borst |
| 8–10 | #ffacd5 #ee6aa4 #ac3973 | magenta: edelsteen, binnenkant van de oren, neus, vingertoppen, staartpunt, mondje (f2) |
| 11–13 | #eefff6 #8beee6 #39a4ac | ogen (maangloed; 13 alleen in frame 2) |
| 14 | #ffffff | glans (alleen frame 2, in de open ogen) |
| 15 | #101010 | omlijning, pupillen |

Gebruik in frame 1 (index 1..15): 28 / 378 / 421 / 114 · 72 / 53 / 55 · 12 / 18 / 14 · 26 / 22 / 0 · 0 · 228.
**Let op voor het recept:** in de vacht is index 3 iets vaker dan de basis 2 (421 tegen 378). Dat komt doordat de lichte buitenlijn (selout aan de lichtkant), de oogleden en het zitkussen index 3 gebruiken. Geef het recept daarom `'_base': {'vacht': 2}`, of maak bij een volgende ronde de lichte buitenlijn index 4. Het zilver is in balans (5/6/7 = 72/53/55; 5 is groot door de sikkels).

## check.py (`--stage 1`)
```
LET OP  geen back.png
LET OP  geen icon.png
OK      hoogte (px)                  46  (Hoenn fase 1 p10..p90: 30..58, mediaan 40)
OK      breedte (px)                 52  (Hoenn fase 1 p10..p90: 29..61, mediaan 42)
OK      oppervlak (px)               1441  (Hoenn fase 1 p10..p90: 527..1674, mediaan 912)
OK      kleuren gebruikt             15  (Hoenn fase 1 p10..p90: 10..15, mediaan 13)
OK      rand: aandeel zwart          0.564  (Hoenn fase 1 p10..p90: 0.235..0.578, mediaan 0.403)
OK      rand linksboven: helderheid  0.319  (Hoenn fase 1 p10..p90: 0.262..0.533, mediaan 0.38)
OK      rand rechtsonder: helderheid 0.176  (Hoenn fase 1 p10..p90: 0.059..0.296, mediaan 0.151)
OK      licht links(-)/rechts(+)     -0.041  (Hoenn fase 1 p10..p90: -0.424..0.154, mediaan -0.134)
OK      licht boven(-)/onder(+)      -0.111  (Hoenn fase 1 p10..p90: -0.531..0.1, mediaan -0.193)
OK      aandeel schaduwtinten        0.526  (Hoenn fase 1 p10..p90: 0.157..0.597, mediaan 0.404)
OK      dithering (schaakbord)       0.0229  (Hoenn fase 1 p10..p90: 0.0153..0.0936, mediaan 0.0461)
OK      losse pixels                 3  (Hoenn fase 1 p10..p90: 1..26, mediaan 8)
OK      binnenlijnen zwart           0.049  (Hoenn fase 1 p10..p90: 0.01..0.113, mediaan 0.033)
OK      verschil frame 1-2           0.311  (Hoenn fase 1 p10..p90: 0.282..0.792, mediaan 0.618)
species_info: .frontPicSize = MON_COORDS_SIZE(56, 48), .frontPicYOffset = 6
```
De back en het icoon zijn niet gevraagd in deze ronde. Er is geen enkele FOUT.

## Checklist Pokémon-design
- [x] **Dier × idee × type:** een aap (kop, oortjes, staart, handen), een ziener of genezer (meditatie, gevouwen vingertoppen, zegenende hand) en Psychic (zie hieronder). Of iemand zonder uitleg ook "genezer" noemt, is nog niet getest; "mediterend" en "Psychic" lijken me wel direct te lezen.
- [x] **Type herkenbaar, met minstens drie middelen:** gloeiende ogen die iets onnatuurlijks doen, een voorhoofdteken (sikkels + edelsteen), een frontale, symmetrische meditatiehouding, een spiraalsymbool en lavendel/magenta.
- [x] **Basisvorm:** een grote bal (de kop) op een peer, met een plat kussen eronder. Geen knieën, gewrichten of snuit; de armen zijn stompjes.
- [x] **Eén iconisch, onrealistisch kenmerk:** de grote Nazca-spiraalstaart met de gloeiende punt. Hij breekt het silhouet aan de rechterkant en is op 1× leesbaar.
- [x] **Silhouettest** (compare.png): het silhouet is herkenbaar en niet te verwarren met Abra, Espurr of Natu. Het risico is "aap of muis met een krulstaart": zonder kleur draagt alleen de spiraal het ontwerp.
- [x] **Kleur:** twee hoofdkleuren (lavendel, zilverwit), maan-cyaan voor de ogen en één accent (magenta). Het helderheidscontrast zit tussen het lavendel lijf, de witte sikkels en borst en de donkere omlijning.
- [x] **Gezicht:** frame 1 is kalm en raadselachtig (halfdichte oogleden), frame 2 is het schrikmoment (wijd open, gloeiend) met het zegengebaar. De glans zit alleen in frame 2, met opzet: in frame 1 is er geen pupil en geen glans.
- [x] **Vooruitwijzing:** de sikkels en het zilver worden het maanmotief van de genezer, de gevouwen vingertoppen worden de helende handen, de spiraal groeit per fase en magenta wordt de kleur van zijn helende moves.
- [x] **Starters:** in het trio is hij midden-koel. Naast de 27 starters valt hij op door de kleur (geen enkele starter is lavendel) en door de spiraal.
- [x] **Andere Pokémon van hetzelfde dier:** Oranguru (wijze aap met cape en waaier) en Passimian. De onze is geen mini-Oranguru: geen cape of voorwerp, maar ogen, voorhoofdteken en spiraal.
- [x] **Gespriet, niet geïllustreerd:** egale vlakken, ramps van 3–4 tinten en geen vachtruis (dithering 2%).

## Wat ik zelf nog niet goed vind
- **De gevouwen handen** lezen op 1× als een driehoekje of kegel op de borst. Groter is lastig zonder het lijf te bedekken. Een alternatief is de handen onder de kin of de vingers lichter (zilver) maken.
- **Frame 1-ogen:** halfdichte leden lezen op 3× als "sereen", maar op 1× ook een beetje als "slaperig". Een dunnere, heldere sikkel met een cyaan gloedpixel naast het oog zou mysterieuzer kunnen zijn. Het verschil tussen frame 1 en 2 is klein (0,31, onderaan de Hoenn-spreiding).
- **Groot voor fase 1:** 46×52 px en 1441 px oppervlak (mediaan 912), vooral door de staart. Treecko heeft hetzelfde formaat, maar Abra en Espurr zijn duidelijk kleiner. De kop kan 1–2 px kleiner als Jordi hem te groot vindt.
- **Het lijf onder de kop** (peer + kussen) is nog wat generiek, met vooral schaduwtinten. Een geweven Andes-detail (de aguayo-streep uit de kritiek) zou hier passen, bijvoorbeeld als band om het kussen. Dat heb ik weggelaten om het type niet te overstemmen.
- **Recept:** vacht-index 3 is iets vaker gebruikt dan de basis (zie de paletindeling). Er is nog geen albino- of zwarte proefvariant gedraaid.
