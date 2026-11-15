# Eindkeuring steenjaguar r4 (Dragonfly Cave + Gen 3)

Gekeurd: `steenjaguar_r4.png` (13 nov). Bevroren en niet gekeurd: oog (x11–14, y18–20 + directe omgeving), buikschaduw, silhouet, mozaïekindeling.
Hulpbeelden in `eindkeuring/`: `vel_buitenlijn.png` (r4 · selout A · selout B · Raikou · Absol · Persian · Entei · Manectric, op 4× en op 1× wit/donker/gras; `vel.py`), `huidig_vs_selout_8x.png` (r4 links, A rechts), `selout_voorstel.png` + `_8x` (A), `selout_voorstel_b.png` + `_8x` (B, aanbevolen), script `selout.py`.

## Eindoordeel: **PASS** (2 kleine MOET-punten, beide alleen tint/rand)
Blind op 1× leest hij meteen als een brullende, sluipende katachtige van steen, en hij staat niet uit de toon naast Raikou, Entei en Persian: hij is een nette Gen 3-sprite die zo kan blijven. Omlijning is overal 1 px en gesloten, geen lichte kleur op de rand, 16 kleuren, licht van linksboven (gem. luma vlak: linksboven 120, rechtsboven 113, linksonder 121 (lichte voorpoot = modelstuk), rechtsonder 84). Het enige echte verschil met Game Freak is de buitenlijn: die is 100% zwart, echte Gen 3-sprites 45–68%. Verder één lichte poot-onderkant. De vele kleine clusters zijn voegen (2/3) en modelstukjes, zoals gevraagd behouden.

## Meting
| Meting | Resultaat |
|---|---|
| Kleuren | 15 + transparant (max 16) |
| Palet (luma) | omlijning 1 (14) · steen-zwart 4 (38), grijs 5 (121) · lila 2 (80) 6 (96) 7 (131) 8 (177) · rood 3 (64) 9 (74) 10 (111) 11 (149) · crème 12 (143) 13 (191) 14 (232) 15 (252) |
| Stappen | lila 16/35/46 · rood 10/37/38 · crème 48/41/20 |
| Buitenrand | 255 px, allemaal index 1; geen open randen, geen dubbele lijn |
| Clusters < 3 px | vrijwel alleen voegen in 2/3, staartpunt (4/5), tanden (15), neus-/oogglans: modelstukjes, toegestaan |

## Per eis
| Eis | Oordeel |
|---|---|
| Omlijning 1 px, gesloten | PASS |
| Geen zwart/gekleurd om en om | PASS (nu alles zwart; geldt ook voor het voorstel, zie §Buitenlijn) |
| Licht linksboven | PASS, behalve poot-onderkant (MOET 2) |
| Schaduw als sikkel | PASS (buik bevroren; poten licht links, 9/3 rechts) |
| Geen pillow shading / banding | PASS |
| Clusters < 3 px | PASS (voegen + modelstukjes) |
| Contrast per tintstap | PASS met kanttekening: voeg 2 in 6 (16) en voeg 3 in 9 (10) lezen nauwelijks (ter info) |
| ≤ 16 kleuren | PASS (15) |
| Geen lichte kleur op de buitenrand | PASS |

## Buitenlijn (vraag van de eigenaar: "de buitenste lijn is helemaal zwart" · "of dat werkt of niet past")
**Hoe Gen 3 het doet (gemeten, randpixels naast transparant, frame 1):**
| Sprite | zwart totaal | zwart boven/links | zwart onder/rechts | selout-tinten (luma) |
|---|---|---|---|---|
| Raikou | 54% | 22% | 72% | grijs 104, goud 99, paars 118 |
| Absol | 56% | 28% | 75% | blauwgrijs 102 (langs wit!), 75, 52 |
| Persian | 51% | 30% | 65% | okerbruin 87 |
| Entei | 45% | 25% | 56% | grijs 81, bruin 47/90 |
| Manectric | 59% | – | – | grijs 79, bruin 99 |
| Rock: Regirock / Golem / Onix / Aggron | 61 / 63 / 47 / 68% | | | |
| **steenjaguar r4** | **100%** | 100% | 100% | – |

Regel bij Game Freak: onder/rechts (schaduwkant) en langs donkere delen zwart; boven/links een selout in een donkere tint van het aangrenzende vlak, luma ±75–105. Langs wit/lichte vlakken geen lichte selout maar een middentint (Absol: blauwgrijs 102). Zwart blijft ook bovenaan waar de rand een zwart of donker deel raakt. Steen-Pokémon doen hetzelfde, alleen iets meer zwart.

**Voorstel (regel per kleurgroep, alleen randpixels met transparant boven of links; muil x2–11 y23–29 blijft zwart):**
- grenst aan lila 7/8 → **2** (luma 80): 28 px
- grenst aan rood 10/11 → **3** (luma 64): 44 px
- grenst aan crème 13/14 → A: **12** (luma 143) · B: **1 blijft zwart** (aanbevolen): 16 px
- grenst aan zwart 4/5, donkere tinten 2/6/3/9, tanden 15 → **1**
- losse gekleurde randpixel zonder gekleurde buur → terug naar 1. Er wisselt alleen per heel randstuk (zoals de mozaïekstukken), nergens zwart en gekleurd om en om.

Coördinaten (x,y):
- **2:** (14,15) (15,15) (16,16) (17,16) (4,20) (25,22) (26,23) (27,24) (34,27) (35,27) (36,28) (37,28) (6,34) (6,35) (7,36) (19,50) (51,50) (18,51) (18,52) (17,53) (13,56) (14,56) (12,57) (11,58) (11,59) (11,60) (54,16) (55,16)
- **3:** (6,17) (18,17) (19,17) (20,17) (21,17) (22,17) (57,17) (5,18) (58,18) (4,19) (59,19) (53,22) (54,23) (28,24) (29,24) (54,24) (30,25) (31,25) (32,26) (33,27) (42,28) (43,28) (44,28) (45,28) (46,29) (47,29) (50,29) (48,30) (49,30) (15,38) (15,39) (15,40) (16,41) (16,42) (17,43) (18,44) (18,45) (19,46) (20,48) (19,49) (52,51) (52,52) (51,53) (50,54)
- **12 (alleen A; in B blijven deze 1):** (11,15) (12,15) (13,15) (8,16) (9,16) (10,16) (7,17) (54,26) (53,27) (38,28) (39,28) (40,28) (52,28) (51,29) (16,54) (15,55)

**Eerlijk oordeel: werkt het?** Ja, maar bescheiden, en alleen als B. Op 8× wordt de bovenrand van rug, nek en voorpoot zachter en meer "gebeeldhouwd", en het aandeel zwart zakt van 100% naar 72% (183 van 255), dicht bij Aggron (68%) en Golem (63%). Op 1× is het verschil klein, omdat veel randstukken (staartpunt, neus, borst, achterpoten) aan zwarte of donkere mozaïekstukken grenzen en daar terecht zwart blijven. Variant A past niet: crème 12 (luma 143) is lichter dan elke selout in de gemeten sprites (max ±118) en maakt de bovenkant van de kop open en vaag (zie `huidig_vs_selout_8x.png`); daarom blijven de crèmestukken zwart. Rondom zwart is niet fout (het is consequent en past bij hard steen), maar het oogt zwaarder en "stickeriger" dan Game Freak; B is de veilige middenweg.

## MOET
1. **Buitenlijn: selout B** zoals hierboven (72 px: 28× 1→2, 44× 1→3; crème en de rest blijven 1). Reden: 100% zwart tegen 45–68% bij Gen 3; lichtkant hoort een donkere tint van het vlak te krijgen. Beeld: `eindkeuring/selout_voorstel_b.png` / `_8x.png`. (Keuze van de eigenaar; als hij rondom zwart wil houden, is dat geen fout.)
2. **Poot-onderkant voorpoot:** (14,61) (15,61) (16,61) (18,61) (19,61) van **8 → 7**. Reden: lichtste tint direct op de onderrand, aan de schaduwkant; elke poot in Raikou/Absol/Entei heeft onderaan de schaduwtint. Geen clusters < 3 px als gevolg (sluit aan op 7 bij (19,60), (20,60)).

## MAG
1. **(56,51) 13 → 12:** losse crèmepixel tegen de rechter (schaduw)rand van de achterpoot; het stuk blijft, alleen in schaduw.
2. **Staartpunt minder ruis:** (48,18) en (46,20) van **5 → 4**. De overige grijze pixels (50,17), (51,18), (52,18), (49,19), (50,19) vormen dan één diagonale ribbel zoals in het model; nu leest het 4/5-patroon op 1× als ruis.

## Ter info voor de eigenaar
- Voegen 2 in lila 6 (verschil 16) en 3 in rood 9 (verschil 10) zijn op 1× bijna onzichtbaar; in de schaduwdelen verdwijnt de mozaïekindeling daardoor. Een donkerdere voegtint kan alleen met een paletwijziging (palet zit vol op 16): ontwerpkeuze, niet nodig voor PASS.
