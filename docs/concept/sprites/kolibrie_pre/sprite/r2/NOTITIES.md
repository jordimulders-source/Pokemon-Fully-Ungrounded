# Hummlet r2 (19 nov), maker

Alleen Claude's benoemde reparaties 1–7 op r1, steeds naar het model (`natief.png`, ook als raster-overlay met `scripts/overlay.py`).

## Resultaat
- `hummlet.png`: hoofdversie (oog a), 64×64, P, index 0 transparant, 14 kleuren in gebruik, 679 px, figuur x 12–51, y 24–58 (40 px breed).
- `hummlet_oogB.png`: zelfde sprite met het Starly-oog uit `../../af/kolibrie_pre.png` (pixel voor pixel).
- `onderlaag.png` (= r1), `normal.pal` (oude palet), `vel.png`: r2a | r2b | r1 | onderlaag | oud | Taillow | Starly (8×), 1×/2× op licht/donker/wit, kop 12× (oog a | oog b | model).

## Diff r2 ↔ r1 per reparatiezone (`scripts/controle.py`; buiten de zones: 0 px)
| Reparatie | px anders (oog a) | silhouet |
|---|---|---|
| 1 snavel | 25 | −8 (snavel nu 1 px aan de punt, 2 px vanaf kolom 4) |
| 2 aansluiting snavel/mondhoek | 2 (+ overlap met de vakken van 1 en 4: samen 7 volgens het log) | −1 |
| 3 kopomtrek | 6 | −1 (rij 2 kol 24 weg; rij 0 had al 16–20) |
| 4 volume kop | 8 | 0 |
| 4 volume buik | 24 | 0 |
| 5 oog a / b | 12 / 10 | 0 |
| 6 staart | 12 | 0 |
| 7 vleugellijnen | 5 | 0 |
| **totaal** | 94 (oog b: 92) | −9 (alleen 1–3, zoals gevraagd) |

## Wat er per reparatie gebeurde
1. **Snavel:** onderrand zakt regelmatig 1 rij per 2 kolommen (rij = 1 + x//2), helling gemeten op de onderrand van de modelsnavel (0,49). Kolom 0–3 is 1 px (lijn 1); vanaf kolom 4 2 px: bovenop leisteen 14, onder lijn 1.
2. **Aansluiting:** de donkere klont tussen snavel en oog (4,12), (5,12), (5,13), (6,14) en (7,15) is lila 4. De kopomtrek loopt via (4,11) door tot op de snavel. De gele mondhoek (7,14) staat direct onder het einde van de snavel. Kin: (7,10) selout 2, (7,11) lijn 1. Rij 8 onder de mondhoek is ongewijzigd, want daar heeft het model zelf lijnpixels.
3. **Kopomtrek:** koepel volgens een cirkel met r=7 rond kolom 18,5: rij 0 kol 16–20, rij 1 14–22, rij 2 13–23, rij 3 12–24. De trapjes zijn links 2-1-1 en rechts 2-1-1-1. De selout bovenaan loopt t/m kolom 19, kolom 20 is lijn.
4. **Volume:**
   - kruin: boogje hooglicht 6 op (1,16–18) en (2,15) binnen het 5-vlak;
   - sikkel 3 achter de kop is in het midden 2 px breed (rij 4–8);
   - nekschaduw 3 loopt over rij 9, kol 21–24, naar de vleugel;
   - buik: de sikkel onderaan is 2 px (tint 4), en loopt van linksonder door tot rechts.
   
   De stappen 6→5→4→3 zijn 224/195/161/118, dus ±30–40.
5. **Oog a:** het model-oog 4×4 met afgeronde hoeken (hoekpixels lila), glans 7 linksboven, iris 14, lichte onderrand 5 op (9,19), (9,20) en (8,21). **Oog b:** het Starly-oog uit de oude sprite (3 breed, 7 boven 5, flanken 2), met de glans op dezelfde plek.
6. **Staart:** de bovenste veer krijgt een lichte bovenrand van 1 px in tint 5 (rij 20, kol 35–38) en daaronder de middentint 4. Een scheidingslijn 10 loopt schuin van (21,37) naar (22,35). De onderste veer is blauw 8 met 10, zoals in het model (lila veer boven, blauwe eronder).
7. **Vleugellijnen:** de twee lange donkere veerlijnen uit het natieve model zijn omgerekend naar het doelraster:
   - A: natief (58,61)→(72,78), doel (20,25)→(28,34);
   - B: natief (55,67)→(66,79), doel (19,29)→(24,35).
   
   Ze staan als 1 px-lijn in 10, alleen op blauwe pixels en zonder het eerste en laatste pixel (taps). Lijn A loopt uit in de sikkel onderaan. Twee losse lila pixels uit r1 op lijn A en de vleugelpunt, (25,31) en (27,34), zijn meegenomen.

## Zelf bekeken (8× naast het model)
- Snavel leest als rechte dunne naald, beter dan r1; de leisteen bovenop is op 1× nauwelijks te zien.
- Oog a leest rond met glans; oog b is smaller en hoekiger (Starly-stijl).
- Koepel en volume van de kop zijn duidelijk beter; de buiksikkel geeft de bol.

## Resterende zwakke punten
- Snavel is dunner dan de modelnaald (model aan de basis ±2,5 px). Met 2 px aan de basis volgt hij de opdracht, maar 3 px op kolom 10–13 zou dichter bij het model zitten.
- Onder de mondhoek (rij 6–8, kol 10–13) blijft een donkere massa van snavelonderrand + kinlijn (modellijnen).
- De lichte onderrand van oog a is op 1× subtiel.
- De staartwaaier leest op 8×; op 1× is het een klein licht vlakje met een blauwe onderkant.

## Opnieuw draaien
Eerst `../r1/scripts/alles.sh` draaien. Daarna `stapD.npy` als `r1.npy` naast `zone_t.npy`, `zones_nat.npy` en `natief.png` zetten, en `python3 r2.py && python3 maak2.py && python3 controle.py`.
