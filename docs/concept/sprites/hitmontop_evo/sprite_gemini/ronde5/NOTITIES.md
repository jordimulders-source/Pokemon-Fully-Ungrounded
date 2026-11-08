# Hitmongroove: sprite naar het Gemini-model, ronde 5 (maker)

Basis: `ronde3/raster.txt` (torso c). Jordi over de eindkeuring, letterlijk: "nee de arm mag niet langer, de koordband mag wel smaller als dat er prima uit blijft zien, ga het verder perfectioneren".

## Opgeleverd
| Bestand | Wat |
|---|---|
| `capoeira.png` + `raster.txt` | Beste variant (arm A). |
| `capoeira_armB.png` + `raster_armB.txt` | Alternatief (arm B); verder pixel voor pixel gelijk aan A. |
| `vel.png` | r5 / armB / r3 / model op 8×; steunarm op 12×; kop op 12×; 1× en 2× licht/donker naast Hitmontop en Hitmonchan. |

Opbouw (met de hand, scripts alleen voor montage): `pas_toe.py ronde3/raster.txt hand_reparaties.txt` → `zet.py … hand_armA.txt` (of `hand_armB.txt`) → `zet.py … hand_hoorn.txt` → `maak.py`.

## Wat er veranderd is
1. **Reparaties 3–7 uit EINDKEURING.md** (`hand_reparaties.txt`): selout vrije bovenarm (17,26), manchet lichtkant grijs (30,51–52), geen 4 aan de lichtkant van de torso, sikkel taps, kruisnaad 1 px, schaduwstrook kop taps. Niet teruggebracht uit r4: glans als sikkel, selout op de dunne benen, vage tenen.
2. **Steunarm** (reparatie 1–2 vervangen door een nieuwe arm). Hand en manchet staan op dezelfde plek, totale lengte gelijk (torso tot pols rij 41–49).
   - Koordband 3 → 2 rijen, gedraaid koord met schuine groeven (A), geen dambord, selout A links. Leest op 1× en 2× nog als koord.
   - Geen zwarte onderrand van de torso meer: de rechterrand van torso en arm is één lijn (x35, zoals in het model), de schaduw 4 van de torso loopt door in de arm.
   - Taps: binnenkant 5 px onder de band → 4 px bij de pols; linkerrand buigt (x29 → x30), selout 5 links, glans 2 als korte diagonale streep, schaduw 4 rechts als sikkel (1-2-2-2-1 breed).
   - **A**: schouderrij huid (rij 42), band rij 43–44, arm rij 45–49.
   - **B**: band direct op de schouder (rij 42–43), arm rij 44–49 (één rij huid meer onder de band).
3. **Hoorn**: rond nopje → scherpe punt naar linksonder, gemeten op het model (punt x8, onderrand rij 49 x8–11): bovenrand selout 5, onderrand recht zwart, punt (8,49), glimpje 2. Verder niets aan de kop.

## Controle
- 16 kleuren incl. transparant, index 0 transparant; 0 losse omlijningspixels.
- Silhouetverschil t.o.v. r3: A 12 px, B 14 px; alleen steunarm/band (x35 rij 40–49, x36 band, x29 rij 46; B ook x28 rij 42 en −x28 rij 44) en hoorn (8,49). Let op: (35,40) ligt net boven de armzone; nodig zodat de torso zonder deuk in de arm overloopt.
- Pixeldiff buiten de opdrachtzones: alleen de benoemde keurderreparaties.
- Nieuwe kleine vlakjes zijn bedoeld: koordgroeven (zoals de band om de vrije arm), glans/selout van de arm, de hoorn (7 px binnenkant, kan niet groter). 3 randpixels zonder zwart = bewuste selout (A aan de band, grijs aan de manchet).

## Zwakke punten (eerlijk)
- De hoorn blijft klein (model-maat); hij leest als punt, maar is korter en dikker dan de dunne spies in het model.
- De rechterrand van de arm is vrijwel recht (zoals het model); de curve zit links en in de band.
