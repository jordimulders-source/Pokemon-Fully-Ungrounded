# Onweerswolk-Altaria frontsprite, ronde 6 (vanaf r5-proef, alleen lijf + rechtervleugel: MOET 6b)

Start: `sprite_r5/proef_eindkeuring.png` (r5 + MOETEN 1–6). Bouwen vanuit `altaria/`: `python3 sprite_r6/bouw.py && python3 sprite_r6/vel.py`.
Bestanden: `altaria_r6.png`, `altaria_r6_8x.png`, `vel.png` (r6 | proef | model | game-Altaria op 8×; lijf en rechtervleugel 16× naast het natieve model; 1× op licht/donker), `bouw.py`, `bollen.txt` (opgemeten bollen), `fix.py` (handreparaties per pixel).

## Diff
- r6 ↔ proef: **393 px** — lijf (X10–53, Y44–57) 296, rechtervleugel (X38–60, Y16–31) 97, elders **0**, alpha 0.
- Kop, ogen, snavel, hals, kuif, static, linkervleugel, buitenrand, silhouet: diff 0 (assert in `bouw.py`: alles buiten de wolkvulling van de zone = proef).
- Geen zwart buiten de pupillen; geen rechte naden ≥ 5 px meer (controle `naden()`); Y57 heel donker (MOET 6).
- 13 kleuren incl. transparant, palet ongewijzigd.

## Werkwijze
1. Per modelbol plek, breedte/hoogte, licht/midden/donker en (bij de lichte bollen) de hooglichtkern opgemeten op het natieve model (`bollen.txt`, achter → voor).
2. Elke bol belicht van linksboven als bolvorm (kern 6 → licht 5 → midden 4 → donker 3); de voorste bol wint; aan de onder-/rechtergrens van een bol een onderboog in 3 (geen selout). Kernen ≥ 3×2 op modelplek.
3. Oude selout-naden van r5 in het lijf die geen bol raken → 3. Ontkorrelen (vlakjes < 3 px → dichtstbijzijnde toon; ring van 5 rond een kern blijft).
4. 77 px handreparaties (`fix.py`), zie hieronder.

## Per bol
Lijf:
- LB1 (X16–19): kern 16–18,44–45, ring 15 en 16–17,46, naad naar LB2 op X19–20.
- LB2 (X20–23): kern 20–21,44–45.
- F (kern bevroren): onderboog als boog (22–24,46) → (25–29,47) → (29–32,46); de rechte naad Y47 X21–30 is weg.
- R: onderboog schuin oplopend naar rechts (37–40,46 → 40–43,45).
- S (X29–36): kern 31–33,47–49 (≥ 3×2), ring, linkergrens donker (model-lijn), onderboog Y52–53.
- LL (X11–17): kern 11–14,47–48 met ring 15,47–48; onderboog Y51–52 (was de rechte naad Y49).
- M1 (X18–29): donkere bol zoals het model, middenkap Y48–51 met ronde onderkant (19 en 23,51 donker).
- M2 (X37–44): lichte kap 37–41,48–50; RR/RL rechts donker met middenkap.
- Rok: K1-kap 14–18,53–55; K2-kap als koepel (27–29,54 / 26–32,55 / 26–29,56); K3-kap rond (34–40,53–55); Y57 donker.
Rechtervleugel:
- A (punt): kern 57–59,17 + 56–58,18, ring 55–57,19, punt rechts donker.
- B: kern 47–49,21–22, ring 46,22 / 50,20–22 / 47–49,23, onderboog (46,23) → (45–51,24).
- Rb: kap 44–45,23 + 43–44,24.
- C: kern 41–43,25 + 40–43,26, ring 40–42,27, onderboog 41–43,29 / 44–45,28.
- D1: kap 46–48,25, onderboog 46–49,27. D2: kap 44,26–27. E: kap 39,29 + 38–39,30. F2: kap 45–47,29 + 44–45,30.
- Rechts van de static donker (schaduwzijde, model).

## Eerlijke twijfels
- De bollen lezen nu als bollen (geen platen meer), maar minder scherp dan in het model: het model scheidt ze met zwarte lijnen; hier alleen 3 tegen 4/5 (ΔL ±22), zoals gevraagd ("onderboog in 3", "niet zwart").
- Rechtervleugel: bollen zijn klein (2–4 px); A, B en C lezen, Rb/D1/D2/F2 zijn op 1× nauwelijks losse bollen.
- 18 vlakjes < 3 px blijven over; allemaal ring- of boogpixels van kleine bollen (functie), geen losse middentint in een vlak.
- De rechte naad (7–11,25) in de linkervleugel uit de opdracht is níet aangepakt: linkervleugel is bevroren (assert).
- De bevroren bovenkant (Y ≤ 43) heeft nog de r5-stijl (selout-naden); de overgang op Y44 is daardoor zichtbaar.
