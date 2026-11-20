# Hoatzin fase 2, r17 (20 nov): pixelblad uit het model, niets getekend

Opnieuw bouwen: `sh alles.sh` (reduceer → pixelblad → bouw → raster_model). `check.py` = die van r16.

## Methode
1. `reduceer.py`: natief model `../r1/natief.png` (200×200, figuur 146×182 cellen) → **gehele factor 3**, fase y 7 / x 32 → 49×61 blokken.
   Modelkleuren eerst in 28 k-means-clusters; per 3×3-blok wint het meest voorkomende cluster (modus), celkleur = gemiddelde van díe pixels (echte modelkleur, niet gemengd).
   Dunne lijnen die als minderheid zouden verdwijnen winnen: donker (L<62) bij ≥2/9, licht (vleugelstrepen L≥140) bij ≥2/9, bruin (kuifstrengen) bij ≥3/9; ligt de lijn over een blokgrens, dan alleen het blok met de meeste lijnpixels (nooit 2 px dik).
2. `pixelblad.py`: figuur op x 7–55, y 3–63 (49×61; **3 px marge boven**, tenen op rij 63, gecentreerd). `pixelblad.png` (14×, rood per 8), `pixelblad.csv` (x,y,hex), `naast.png` (pixelblad | model zelfde plek/raster | r16).
3. `bouw.py` + `klassen.py`: per cel kleurgroep uit de modelkleur (mauve, kuifbruin, grijs, blauw, buik, staart) → palet:
   1 lijn #1C101A · mauve 2–5 #3A2633 #64485A #8C6A7E #B494A8 (model-tinten L 20/45/82/118/157, lichtste van L 181 naar 157 getrokken, stappen ±36) · kuif 6–7 en blauw/rood 8–10, buik D 11–13, grijs 14–15 = r16.
   Donkere modelvulling (geen dunne lijn) → tint 2, niet zwart; poten (onder de buik) → grijs 14/15 met zwarte lijn, zoals het model.
4. Bevroren uit `../r16/hoatzin.png` (`bevroren.py`), elk als geheel verschoven naar de nieuwe uitlijning (`schuif.json`, gemeten met overlap op het pixelblad):
   snavel + oog samen (+1,+1) (oog valt dan precies op het modeloog; snavelpunt ligt 1 px links van de modelomtrek, x 6 i.p.v. 7: niet aangepast, de kop blijft één geheel), buik (0,+1), staart (−1,0).
5. Opschonen: 36 randpixels in lichte tint → lijn; 63 losse pixels zonder gelijke 8-buur → meest voorkomende buurkleur (geen strepen/lijnen, niets bevroren).

## Afwijking t.o.v. het gemapte pixelblad (stapA.npy), per zone
| zone | px | afwijkend | bevroren | opschoning |
|---|---|---|---|---|
| kuif | 229 | 26 | 2 | 24 |
| kop | 84 | 50 | 44 | 6 |
| vleugel | 761 | 51 | 1 | 50 |
| nek/lijf | 507 | 121 | 96 (buik) | 25 |
| poten | 153 | 31 | 25 | 6 |
| staart | 212 | 87 | 87 | 0 |
Totaal 324 van 1740; silhouet t.o.v. het pixelblad 26 px (alleen waar bevroren r16-delen 1 px over de modelomtrek vallen). Silhouet t.o.v. r16: 403 px anders.

## Gecontroleerd (Jordi's gele lijnen)
- Bovenkant past: bovenste pixel y 3. Vleugel- en kuifomtrek = modelomtrek (raster_model.png).
- Kuif: vier ronde mauve plukken achter, bruine strengen ervoor, dunne strengen links naar links/omlaag (x 5–8, y 10–19) en rechts tot x 27 uit het model.
- Nek: lichte voorkant (tint 4, 3–4 px) loopt door tot op de buik; donkere streep achter het oog langs de nek (tint 2 met dunne lijnen) zoals het model.
- Poten/tenen/klauwen: uit het model, niets getekend.

## Zwak (eerlijk)
- Kuifstrengen in het model zijn ±⅓ px breed; op 1× blijft een bruine waaier met een paar lijnen, niet elke streng.
- Poten zijn dun en wat rafelig (model op ⅓); 1 zwart 2×2-klontje bij (20,56) waar tenen kruisen.
- check.py: 52 "dambord"-treffers, vrijwel allemaal diagonale 1-px vleugelstrepen (5 op 3) en kuifstrengen (6/7); geen om-en-om.
- Buik (bevroren r16) heeft een andere omtrek dan de modelbuik (model ronder en lager); niet aangeraakt.
