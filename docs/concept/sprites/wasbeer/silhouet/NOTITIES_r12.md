# Wasbeer silhouet ronde 12 (maker-agent, 2 nov)

Bestanden: `ronde12.txt` (met de hand gelegd tekstraster), `ronde12_1x.png` (1-bit), `vel_ronde12.png` (silhouet 4x/1x, omtrek over de onderlaag, Gumshoos, Weavile, foto 10/11/15), `onderlaag_r12.py` (+ `onderlaag_r12.txt`), `vel_r12.py`.
Werkwijze (kolibrie/Coathief): onderlaag = omtrek van foto 10 (`omtrek.py`) gespiegeld en zo geschaald (0,154) dat de fotokop op de kop van ronde 11 valt; dan vallen de beenlengte (±15 rijen) en de armhoogte vanzelf goed. Kop = ronde11.txt (rijen 7–22) 3 rijen omhoog en 4 kolommen naar rechts. Daarover rij voor rij met de hand het silhouet gelegd als één geheel; daarna alleen benoemde zones gerepareerd (koevoetklauwen, buidel, staarthaak, rechte stukken). Geen buizen, geen geknipte stukken, geen sjablonen.

## Studie Gen 3 (frame 1, op 8x bekeken)
| | Gumshoos | Weavile | Sneasel | Sandslash |
|---|---|---|---|---|
| px / bbox | 1269 / 54x52 | 1267 / 51x56 | 976 / 49x45 | 1597 / 58x50 |
| kop / hoogte | 19/52 = 37% | ±22/56 = 40% (incl. veren) | 19/45 = 42% | ±20/50 = 40% |
| beenlengte | kort, ±8 rijen (15%) | lang, ±14 rijen (25%), knie gebogen | ±13 rijen (29%), dun | kort, ±10 rijen |
| armen | aan de schouder direct onder de kop, klein, tegen de borst | nabije arm vanaf de schouder vóór de borst, klauw vooruit; verre arm laag achter het lijf | beide armen zijwaarts gestrekt vanaf de schouder, lucht tussen arm en lijf | nabije arm naar voren met grote klauwen; verre klauwen hangen onder de borst |
| 3/4-draaiing | kop naar links, borst (gele baan) naar de kijker, staart naar rechts achter | lijf licht gedraaid, kop iets naar links, verre been kleiner/hoger | kop 3/4 links, verre arm/been kleiner | kop bijna frontaal, lijf naar links, stekelrug rechts achter |
| klauwen | geen | 3 witte, gebogen, tegen elkaar | 3 witte haken per hand, uit elkaar | 2 crème klauwen tegen elkaar als één gebogen vorm (= ons koevoetmodel) |
Les: het lijf is één massa met de kop er bovenop; ledematen lezen omdat er een kolom lucht naast staat (Sneasel), niet door binnenlijnen.

## Maten ronde 12
- 1403 px, bbox 60x55 (kolom 1–60, rij 3–57). Coathief 1315 → ×1,07 (aan de lage kant voor fase 3, maar binnen Gumshoos/Weavile ±1270 en Sandslash 1597).
- Kop rij 3–21 = 19/55 = 35%. Benen: kruis rij 43 → voet rij 57 = 15 rijen (27%, Weavile-lengte).

## Check (SPRITE_OPDRACHT §2, FAKEMON_CHECKLIST, SPRITE_NORM)
| punt | oordeel |
|---|---|
| Houding foto 10: op 2 poten, romp ±30° voorover, kop vooruit, verre poot reikt, nabije hangt, staart laag achter | ok: de omtrek over de onderlaag volgt foto 10 (kop, borst, armhoogte, beide benen, staartaanzet) |
| Niet rechtop/mensachtig, niet horizontaal | ok: romp diagonaal, kop vóór het lijf; breedte komt van staart + klauwen, niet van een liggende romp |
| 3/4 naar links-voor | ok in silhouet (snuit links, verre oor klein links, nabij oor groot rechts, verre been kleiner en hoger); de draaiing van de borst moet de kleur laten zien |
| Beide armen zichtbaar, van de schouders, één hoger | ok: verre arm reikt op borsthoogte (rij 22–26) naar voren zoals op foto 10; nabije arm hangt vanaf de schouder vóór de buik met 1–2 kolommen lucht tussen arm en buik (rij 30–36), dus geen klauwen uit de buik |
| Koevoetklauwen (rechte steel, bocht, recht eindstuk, gespleten punt, 2 klauwen tegen elkaar) | ok: hoog: steel 6 px vooruit, bocht omlaag, eindstuk 4 rijen, punt `#.#`; laag: steel 4 rijen omlaag, bocht vooruit, eindstuk 5 px, punt met V. Haak leest op 1x, de V alleen op 4x (zoals de proef) |
| Kop = ronde 11 | ok: rij voor rij overgenomen; alleen de oren 1–2 rijen boven de schedel uitgetrokken (nabij oor 7 px breed = 31% van de kopbreedte, naar foto 11) zodat de kruin geen rechte lijn van 15 px is |
| Buidel: geleidelijk uit de rug, bolle onderkant, dichtgetrokken opening bij de schouder | ok in de omtrek: rug loopt vanaf de nek 1 kolom per rij uit (geen bult), smalst bij de schouder met een knoopje/plooi (rij 19–20), breedst en bol onderaan, met een inham boven de staartaanzet (rij 39) zodat de onderkant overhangt als een zak. Plooi en zakrand moeten in de kleur verder lezen |
| Staart: dik, taps, haak | ok: 8 rijen dik aan de basis, zakt eerst iets (ligt laag zoals op foto 10) en loopt dan omhoog in een haak met de punt omlaag |
| Lijf niet te dun, geen dikke reet | ok: romp ±24 px zonder buidel (Gumshoos ±25); dij één rond vlak onder de buidel |
| Ledematen ≥5 px, lucht ertussen, geen telgang | ok: benen 5–8 px, 3–4 kolommen lucht tussen de benen; armen 4–5 px |
| Rechte lijnen ≥4 px | ok na reparatie (buikfront, staartrand, schenen); langste resterende: 4 px |
| Leest op 1x als één dier | ok: kop met twee oren, twee armen met haken, twee poten, haakstaart; geen losse delen |

## Open (voor de kleurronde, geen silhouetzwakte)
- Het silhouet kan niet laten zien dat de nabije arm vóór de buik ligt en dat de buidel een eigen vlak is: dat moet de kleur doen (donkere onderarm over geelbruine buik; buidel in vachtkleur met de plooi bovenaan).
- Kop van ronde 11 heeft een vrij steile gezichtsvoorkant; bevroren door Jordi ("prima"), dus niet aangeraakt.

## Lessen
- Foto-omtrek schalen op de kop van de goedgekeurde kop (niet op de totale hoogte) gaf hier meteen Weavile-beenlengte en de juiste armhoogte; alleen romp en poten moesten breder.
- Onderlaag en silhouet met dezelfde verschuiving tekenen; een offset van 4 kolommen maakte de eerste overlay onbruikbaar.
