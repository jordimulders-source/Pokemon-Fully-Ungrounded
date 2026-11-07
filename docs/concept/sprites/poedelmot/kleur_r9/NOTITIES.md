# Poedelmot: kleur r9 (maker, zuinig)

Maatstaven (Jordi): (1) heel accuraat op het model, (2) een Gen 3-sprite volgens onze eisen. Gebouwd vanaf r8 (r8 ongewijzigd). Keuring r8: `kleur_r8/poedelmot.png.keuring.md`.
Jordi daarnaast: "kijk goed naar belijning ook, lijnen van het hoofd, lijnen van de bontkraag, lijnen van de vleugel" en "dat de poten allemaal precies kloppen".

Bestanden: `raster.txt`, `poedelmot.png`, `normal.pal`, `palet.py`, `vel.py` → `vel.png` (r9 | r8 | model 8× en close-ups) + **`lijnen_model_vs_r9.png`** (links de lijnenkaart van het model: aandeel donkere modelpixels per spritepixel; rechts alleen de lijntinten van r9 op wit). `controle.py` → `controle_uitvoer.txt`. Lagen: `stappen/bouw9.sh` (nieuw: `k_r9.py`, `k_modlijn.py`, `k_slot.py`, aangepast `k_r8.py`, `k_spriet5.py`).

## Gedaan
1. **Krullen**: brede, ondiepe liggende schubbogen (⌒, straal 3,5, boog 120°), 1 px, één tint (`6`), op de modelplekken in rijen. Geen verticale kolommen meer. Het vleugelvlak is wit-crème zoals het model.
2. **Sprieten**: de nerf is een vloeiende boog langs de bovenrand (berekende kromme, geen vaste trapjes). De ribben zijn evenwijdige schuine lijnen "\" in één tint (`4`) om de 3 px; geen schaakbord.
3. **Tinten**: crème-groep met 3 tinten (`A` 247, `7` ±215, `6` ±174; stappen ±32/41) plus lijnen. `9` → `7`/`A`, `5` → `6` buiten de sprieten, grijs `8` geschrapt.
4. **Kraag en kin**:
   - Vier plukjes `7` in de kraag.
   - De kinboog blijft, nu vloeiend (2-6-2: (19–20,41), (21–26,42), (27–28,41)), met crème snuit erboven.
5. **Buik**: bolle segmentplaten (`7`) met naden `6` die naar het midden omlaag buigen.
   - Klauwtjes: per groep twee diagonale klauwtjes `2` met `3` ertussen; geen `4` meer op de rand.
6. **Lijnen van het model** (`k_modlijn.py`, alleen boven y48):
   - Waar de lijnenkaart van het model een lijn heeft (≥30% donker), is een binnenlijn `3` gezet: kop, masker, kraagrand, vleugelaanzet en vleugelnaad.
   - Binnenlijnen van mij op plekken waar het model geen lijn heeft (< 12%), links van x40, zijn weggehaald.
   - Dat is een scriptstap op de modelkaart, gevolgd door opschonen.

## Poten: model vs r9 (uit de lijnenkaart en de close-up van het model)
| Poot/pluim | Model (positie, vorm, klauwtjes) | r9 |
|---|---|---|
| A, links voor | x11–19, y47–56; hangende ovale pluim, valt vóór de kraagrand; klauwtjes (16–19,55–57), 2 stuks schuin naar linksonder | x15–22, y47–55; ovale pluim; klauwgroep (18–20,55–57) met 2 klauwtjes. Klopt in plek, iets smaller. |
| B, links midden | x19–27, y47–57; ovaal achter A; geen eigen klauwtjes zichtbaar boven B2 | x22–30, y47–55; ovaal. Extra klauwgroep (22–24,55–56) **die niet in het model staat** (ligt deels op de bevroren silhouetrand) |
| B2, onder B | x20–28, y55–59; kleine pluim; klauwtjes (20–23,58–59) | pluim x24–31, y55–58; klauwtjes (24–26,58–59). Klopt in stand, 2–3 px naar rechts (silhouet). |
| Lijf/middenstuk | x27–35, y47–56; tan segmentplaten, grotendeels achter de pluimen; klauwtjes (26–30,57–58) | x30–41 platen; klauwgroep (32–33,57–58), 2 px rechts van het model |
| C, midden voor | x34–41, y53–61; ronde pluim vóór alles, laagste punt; klauwtjes (34–39,59–61), 2 stuks | x34–41, y54–61; klauwgroep (35–39,60–61) met 2 klauwtjes. Klopt. |
| D, rechts midden | x40–46, y50–59; ovaal achter C; klauwtjes (41–46,58–59) | x41–47, y51–58; klauwgroep (43–46,58–59). Klopt. |
| E, rechts achter | x44–54, y45–57; grootste pluim achteraan, onder de achtervleugel; geen klauwtjes zichtbaar | x43–55, y45–57; geen klauwtjes. Klopt. |

Aantal: het model heeft **6 pluimen** (A, B, B2, C, D, E) plus het middenstuk, en **5 klauwgroepen**. r9 heeft 6 pluimen en **6 klauwgroepen**: de groep (22–24,55–56) onder B is te veel. Die ligt op de bevroren silhouetrand; daar kan alleen de kleur veranderen. Repareren: die pixels in de pluimkleur zetten, met een lijntint op de rand.

## Controle
- Alpha-diff 0. Open randen 0 (geen uitzonderingen meer nodig).
- Selout: 3 reeksen zonder afwisseling.
- Losse pixels 0, clusters < 3 px 0.
- Donker-aandeel 0,231.

## Eerlijke zwakke punten
- **Pootlijnen**: de lijnenkaart van het model is onder y48 te rommelig om over te nemen. Daar staan de pluimcontouren nog van r5/r8 en volgen ze het model alleen ongeveer (zie de tabel). De extra klauwgroep onder B staat er nog.
- **Vleugelnaad**: door de modellijnen is de naad op y35–37 deels 2 px dik geworden (klonterig).
- **Kopomtrek**: links valt die samen met de silhouetrand; rechts (x36–42, y34–46) staat de modellijn maar deels.
- Alleen de eindstand en het lijnenpaneel bekeken (gebruikslimiet).
