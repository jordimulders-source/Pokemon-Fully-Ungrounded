# Salticonda – kleurronde 3c (vanaf 3b: kuif groter, neusgaten terug)

Jordi (letterlijk):
- "Die kuif mag nog iets groter"
- "en mag je idd echt met zouttexturen spelen"
- Over 3b: "is rechts de nieuwe versie? ik dacht dat ik meer kuif zei ipv minder"
- "ik wil het sandaconda hoofd als motief, dus iets groter dan silicobra, de neusbult, kijken naar anaconda bronmateriaal, gewoon dat het een volgroeide slang lijkt"

Opdracht (Claude):
- **Kuif:** zichtbaar groter, ±15–25% meer oppervlak dan kleur3. Hij groeit naar achteren en rechtsboven, als een kam of kraag van zoutplaten. Bovenaan blijft 1 px lucht en de textuur van 3b blijft.
- **Neusgaten:** zichtbaar terug, zoals in kleur3, met het verre gat kleiner.
- **Neuskap:** loopt zacht over in de snuit.
- **Bevroren:** al het andere van 3b.

## Bestanden
- `salticonda.png` en `salticonda_raster.txt`: 64×64, palet gelijk aan E/kleur3/3b, transparency 0.
- `vel.png`: kleur3, 3b en 3c naast elkaar; koppen op 9× en het geheel op 4× en 1×, op licht en donker.
- Scripts in `../scripts/`:
  - `kop3c.py`: kraag, kuiftop en snuitpixels, met de hand bepaald.
  - `check_kleur3c.py`: diff-bewijs.
  - `kuifmaat.py`: kuifmaten.
  - `vel_kleur3c.py`: maakt het vel.

## Kuifmaat (`python3 scripts/kuifmaat.py`)
Het masker is voor elke versie hetzelfde:
- rij 0–5 vanaf x 13;
- rij 6–9 vanaf x 21 (boven en achter het oog);
- rij 10–19 vanaf x 34 (achter de gezichtslijn).

| Versie | Oppervlak | Breedte | Hoogte |
|---|---|---|---|
| kleur3 | 309 px | 31 (x 13–43) | 20 (vanaf rij 0) |
| kleur3b | 270 px | 31 (x 15–45) | 19 (vanaf rij 1) |
| **kleur3c** | **367 px** | **38 (x 13–50)** | **19 (vanaf rij 1)** |

- 3c is **+19% ten opzichte van kleur3** en +36% ten opzichte van 3b.
- 3b was inderdaad 13% kleiner dan kleur3. Daar had Jordi gelijk: de top was een rij gezakt en de voorkant van de kuif was weggetrokken.

## Wat er veranderde
**Kuif:**
- **Voorkant en top:**
  - Hij ligt weer hoog over het voorhoofd, zoals in kleur3 (voorrand op x 13–16 in rij 3–5).
  - Hij heeft twee plaattoppen op rij 1, met een inkeping op (25,1) waar de voorhoofdnaad begint.
  - Rij 0 blijft leeg.
- **Kraag:**
  - Hij steekt 3–6 px over de oude achterrand uit, tot x 50, en groeit ook rechtsboven.
  - De oude achterrand is de kraagnaad geworden (oker `g`).
  - Drie dwarsnaden delen de kraag in vier platen. Ze lopen schuin naar buiten af, dus geen rechte streep.
  - Elke dwarsnaad maakt een Y op de kraagnaad.
  - Op rij 12 zit een kleine inkeping in het silhouet tussen twee platen.
- **Textuur:** die van 3b blijft: okernaden, lichte opstaande randen, schaduw aan de andere kant en korrels op de top. Elke kraagplaat heeft een lichte rand (`a`/`b`) langs de naad aan de lichtkant.
- **Bewust níet:** geen kubussen, geen kristalpunten, geen zwart in de naden.

**Snuitfront:**
- **Neusgaten:**
  - dichtbij 3 px donker (O O / O), tegen de voorrand, zoals in kleur3;
  - veraf 1×2 (K/K), kleiner;
  - allebei in de neuskap.
- **Overgang van de kap:**
  - De dip achter de kap is ondieper: (12,6) is nu rand en (11–12,7) zijn plaattint `b`, dus er zit geen gat meer.
  - De schaduwrand onder de kap is één tint (`b` in plaats van `c`) en loopt naar achteren uit in `a`. Zo loopt de kap als bult in de snuit over.

## Diff-bewijs (`python3 scripts/check_kleur3c.py`)
- **Gewijzigd ten opzichte van 3b:** 158 pixels:
  - kuif: 139 (rij 1–6 vanaf x 13 en de kraagzone vanaf de oude achterrand);
  - snuitfront: 23 (x 4–14, y 5–10);
  - deze twee zones overlappen op rij 5–6, x 13–14.
- **Buiten kuif en snuitfront:** 0.
- **Bevroren zones** (oog, wenkbrauw, wang en gezichtslijn, halsband, lijf): 0.
- **Palet:** gelijk; transparency 0.
- **Rij 0:** leeg.
- **Open randen:** 0.

## Checklist
| Punt | Oordeel |
|---|---|
| Kuif zichtbaar groter dan kleur3 (+15–25%) | ok: +19%, 7 px breder, kraag over de achterkant. |
| Zoutplaten (naden, randen, korrel), geen ruis | ok. |
| 1 px lucht boven | ok. |
| Neusgaten zichtbaar, verre gat kleiner | ok. |
| Kap zacht in de snuit | ok: dip en schaduwrand op één tint. |
| Oog, wenkbrauw, halsband en lijf bevroren | ok (0). |
| Gezicht niet vreemder dan kleur3 | ok, zie hieronder. |

## Eerlijk oordeel
- **Kuif:** naast kleur3 is hij nu duidelijk groter: hoog over het voorhoofd en met een kraag van platen over de achterkant.
- **Gezicht:**
  - Het heeft zijn neusgaten weer, zoals in kleur3.
  - Met de zachtere kap leest de snuit als snuit met een neusbult, niet als losse klont.
  - Het oog en de wenkbrauw zijn die van kleur3.
- **Silhouet:** de kop is zwaarder geworden. Op 1× is het een grote zoutkop op de kegel, en zo hoort hij volgens Jordi's "meer kuif".
- Ik zie geen open zwak punt.

## Lessen
- **Meten:** meet de grootte van een onderdeel met één vast masker voor elke versie. 3b "voelde" groter door de textuur, maar was 13% kleiner. Meer textuur oogt niet als meer kuif.
- **Kraag tekenen:** een kraag die over een bestaand silhouet groeit, bouw je zo:
  - de oude rand wordt de naad (die tint op de plek van de oude omlijning);
  - de nieuwe buitenrand krijgt overal omlijning waar er boven, onder of naast niets is;
  - anders ontstaan open randen of zweeft er een seam-pixel aan de rand.
- **Dwarsnaden:** een dwarsnaad over een smalle kraag laat je schuin aflopen (halverwege een rij lager), anders leest hij als rechte streep.
