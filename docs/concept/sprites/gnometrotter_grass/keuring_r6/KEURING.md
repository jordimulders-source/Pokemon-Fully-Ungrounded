# Keuring Gnometrotter Grass r6 (verse keurder, 23 nov)

Gekeurd: `../sprite_r6/gnometrotter_grass.png` · model `../hybride/model_hybride.png` · zusje `../../gnometrotter_rock/af/gnometrotter_rock.png` · Gen 3-hout: Nuzleaf/Shiftry/Trevenant.
Vel: `vel.png` (r6 8× met zones R1–R5 | Rock af 8× | model | 1×). Coördinaten (x,y) in spritepixels, indexen = palet van de sprite (6/7/8/15 roze donker→licht, 9/10/11 blauw donker→licht).
Scope (Jordi): neus, rechterschouder/-arm, linkerhand, lijf (roze romp + blauwe benen). Muts, bladbaard, riem, zolen, stok: alleen ter info. Neusboogkleur wacht op Jordi: niet geteld.

## Oordeel: **FAIL** (benen), romp BIJNA

## 1. Blind (1× en 8×)
- Op 1× leest hij als dezelfde kabouter als Rock af; roze romp leest als ton met duigen, dus als hout. Neus en armen ok.
- Wat meteen opvalt: de **benen zijn veel lichter en vlakker dan bij Rock af** (grote lichtblauwe vlakken, bijna geen donkerste blauw), en de **rechterheup onder de riem is licht** waar het lijf van het licht af draait. De duiglijnen in de romp lezen op 8× nog als rechte kolommen.

## 2. Trouw (binnen de scope)
| Onderdeel | Gemeten | Oordeel |
|---|---|---|
| Neus | Vorm, hooglicht 15 linksboven, 7 rechtsonder; volume ok. Boogkleur niet geteld. | OK |
| Rechterarm/-schouder | x44–61, y22–41: arm en hand pixel-gelijk aan Rock af (alleen de rompkant x44–47 verschilt, die hoort bij het lijf). | OK |
| Linkerhand | Pixeldiff met Rock af in x0–15, y27–37: alleen de stok (x4–10, y36–37), de hand is 0 px anders. | OK |
| Romp | Duigen op de modelposities; het model heeft golvende naden, de sprite rechte. Leest als hout (ton, een paar grote vormen, alleen roze tinten). | OK qua vorm |
| Benen | Model: op beide dijen en op de laarzen een paar grote diagonale plankvormen. Sprite: alleen één boog op de linkerdij (rij 43–46 in 10); **rechterdij heeft geen enkele materiaalvorm** (x31–42, y41–47 is één lichtvlak). | FOUT ("vergeet de benen niet") |

## 3. Gen 3-techniek
| Zone | Meting | Oordeel |
|---|---|---|
| Romp (x28–47, y19–36) | 4 tinten (lum 105/139/183/206), sikkel in 6 onderaan (grootste 6-vlak x31–37, y33–37) en rechts: volume is er. **Maar de duiglijnen zijn nog recht:** naad x34 in 6 loopt kaarsrecht over y24–32 (9 rijen), nerf x38 in 7 over y24–32 (9 rijen), naad x30 over y29–33 en x31 over y20–23; de "buiging" is één pixel verspringen aan het eind. Jordi: "de rechte lijnen mogen wat minder recht, onthoud het perspectief". | BIJNA |
| Romp ruis (x38–44, y26–32) | Losse pixels: (40,32)=8 en (40,31)=7 als enkele pixel tussen andere tinten; 6 in diagonale 1–2 px-stukjes (41,26),(42–43,27),(41,29),(40,30) die door het 7/8-vlak kriskras lopen. Leest als spikkel, niet als één nerf. | FOUT |
| Benen (x15–51, y36–56) | Blauw: 11 = 181 px, 10 = 120 px, **9 = 30 px** (Rock af op dezelfde plek ±110 px 9). Grootste 11-vlak **100 px** (x31–49, y36–47): effen. 9 staat bijna alleen als selout aan de linker(licht)kant (x16–18, y42–53); **geen donkere sikkel rechts/onder** aan dijen en laarzen (keuring r5 punt J is niet uitgevoerd). Rechterheup x43–50, y36–42 is 11 (licht) tegen de zwarte rand, Rock af heeft daar 9/10: lichtrichting klopt niet. ≥3 tinten per vorm: op de dijen en laarzen feitelijk 2 (11/10). | FAIL |
| Belijning lijf | Zwart rechts/onder doorlopend, eigen donker links: ok. Geen open randen gevonden in de scope. | OK |
| Trapjes | Geen nieuwe in de scope. | OK |

Buiten scope (info): muts en bladbaard nog effen (r5 E–G), riem en zolen effen (r5 I, K).

## 4. Reparaties (niets hertekenen; vormen uit het model of Rock af, alleen tinten/lijnen)
**R1 Romp-duigen (x28–46, y19–36):** de naden x30/31, x34/35, nerf x38 en naad x43/44 echt laten buigen met de ton (links van het midden x≈37 bol naar links, rechts naar rechts): **geen enkele duiglijn langer dan 4 rijen in één kolom**, verloop over de hoogte ≥ 2 px (bijv. naad 35 → 34 → 33 → 33 → 34 → 35 van boven naar onder), golvend zoals de naden in het model. Licht/donker-tinten schuiven mee; geen nieuwe tinten.

**R2 Ruis (x38–44, y26–32):** opschonen tot vlakken ≥ 3 px: (40,32)→7, (40,31)→8 of samenvoegen met het buurvlak; de 6-stukjes (41,26),(42,27),(43,27),(41,29),(40,30) óf tot één doorlopende nerf verbinden óf naar 7. Eén nerf, geen spikkel.

**R3 Rechterheup (x43–50, y36–42):** de blauwe en lijnpixels hier 1-op-1 van Rock af overnemen (diff 0 binnen de zone, riempixels uitgezonderd). Rock af: (48,37),(48,38),(49,38),(47,39),(48,39),(46,40),(47,40),(48,40),(48,41) = 9; (45,40),(43–47,41) = 10; (48,36),(49,36) = 1.

**R4 Dijen (x17–50, y42–48):** materiaal uit het model: op de rechterdij 1–2 grote diagonale plankvormen zoals in het model (naden in 9, schaduwkant in 10); tintverdeling volgens Rock af: rechts en onder 9-sikkel (Rock af x39–50 rij 44–47), het lichtvlak 11 alleen linksboven op elke dij. Doel: grootste 11-vlak ≤ ±40 px; 9 ≥ ±70 px in x17–50, y42–48.

**R5 Laarzen (x15–29 en x39–51, y48–56):** r5 punt J alsnog: 9-sikkel 2–3 px aan de rechter-/onderkant van elke laars, de bolling volgend (Rock af: x22–28, y49–50 en x45–50, y53–55 zijn 9); in het model ook één plankvorm per laars.

Neusboogkleur: wacht op Jordi. Daarna opnieuw keuren; R3 en R5 zijn met een diff tegen Rock af te controleren.
