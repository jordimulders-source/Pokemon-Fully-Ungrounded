# Salticonda – kleurronde 3b (vanaf kleur3: alleen kuif en snuit)

Jordi (letterlijk):
- "ik wil het sandaconda hoofd als motief, dus iets groter dan silicobra, de neusbult, kijken naar anaconda bronmateriaal, gewoon dat het een volgroeide slang lijkt"
- Over kleur3: "kijk dat is echt al veel beter de goede kant op" / "Die kuif mag nog iets groter" / "en mag je idd echt met zouttexturen spelen".

Opdracht (Claude): de kop moet minstens 1 px lucht aan de bovenrand hebben. De kuif moet als zoutplaten lezen (lichte opstaande randen, Y-naden, warm oker in de naden, eventueel een opkrullend randje), iets groter in de breedte en naar achteren, en hij moet de punt van de kegel blijven vormen. Daarnaast moet de neusbult duidelijker worden, naar Sandaconda, met de neusgaten erin. De snuit mag iets langer en breder worden, in dezelfde 3/4-hoek. Oog, wenkbrauw, halsband en lijf zijn bevroren.

## Bestanden
- `salticonda.png` en `salticonda_raster.txt`: 64×64, palet van E/kleur3, 14 kleuren, transparency 0.
- `vel.png` bevat:
  - pre-evo, E, kleur3 en kleur3b op 4× en 1×, op licht en donker;
  - de koppen op 8× (pre-evo, Sandaconda, kleur3, kleur3b);
  - de kuif van kleur3b en kleur3 op 8×.
- Scripts in `../scripts/`:
  - `kop3b.py`: met de hand gezette rijen, in globale coördinaten. De bevroren zones worden na het tekenen letterlijk uit kleur3 teruggezet.
  - `check_kleur3b.py`: controle van de bevroren zones, de bovenrand, open randen en losse pixels.
  - `vel_kleur3b.py`: maakt het vel.

## Wat er veranderde
**Kuif:**
- **Plaats:** de top ligt nu op rij 1, dus rij 0 is leeg. De punt van de kegel ligt op x 26–29.
- **Maat:** hij loopt aan de achterkant 1–2 px verder door dan in kleur3 (tot x 44, met een opkrullend randje op x 45). Hij is dus breder.
- **Vijf zoutplaten:**
  - voorhoofd;
  - top (de kegelpunt);
  - achter-boven;
  - achter-midden;
  - achter-onder.
- **Y-punten (3):** (25,5), (31,4) en (37,12), trapsgewijs en zonder kruis.
- **Naden:** in warm oker `g` (stof en klei), nooit zwart.
- **Opstaande randen:**
  - de plaat aan de lichtkant van een naad heeft een lichte rand (`a`);
  - de andere kant ligt in de schaduw (`c`);
  - daardoor staan de platen op als korstplaten.
- **Korrel:** 2–3 lichte pixels in de bovenrand van de toplaat (`a` tussen `b`), als zoutkristal in het licht.
- **Opkrullend randje:** de plaat achter-midden krult op het eind 1 px uit het silhouet (44–45, 13).
- **Bewust níet:** geen kubussen, geen kristalpunten en geen spikkels over het hele vlak.

**Snuit:**
- **Neusbult:** een opstaande, lichte kap bovenop het snuitfront (x 4–12, y 5–10), met een dip naar het voorhoofd erachter en een zachte schaduwrand (`c`) eronder.
- **Neusgaten:** zitten in de kap, als korte donkere spleetjes aan de voorkant: dichtbij 2 px, veraf 1 px. Zo lezen ze als neusgaten en niet als oogjes. Een 2×2-blok op licht las als een tweede oog en is teruggedraaid.
- **Snuitfront:** 1–2 px verder naar links dan in kleur3 (x 4–5) en hoger, maar niet puntig.
- **Hoek:** het front blijft naar de kijker staan, dus dezelfde 3/4.
- **Kaak:** 1 px mee naar voren.

## Checklist
| Punt | Oordeel |
|---|---|
| 1 px lucht boven | ok (rij 0 leeg). |
| Kuif leest als zoutplaten, geen gladde kap | ok. Vijf platen met opstaande lichte randen en oker naden, korrel op de top en een opkrullend randje. |
| Kuif iets groter, breder en naar achteren, punt van de kegel | ok. Naar achteren tot 44/45, de top als afgeronde punt. |
| Neusbult naar Sandaconda, neusgaten erin | ok. |
| Snuit iets langer en breder, 3/4 | ok. Het front staat naar de kijker; niet puntig en geen krokodillenbek. Een lange mondlijn vanaf de punt is geprobeerd en teruggedraaid, omdat hij naar krokodil neigde. |
| Oog, wenkbrauw, halsband en lijf bevroren | ok (0 pixels anders, zie hieronder). |
| Omlijning en open randen | ok: 0 open randen, h aan de lichtkant, K/O rechts. |
| Geen Nacli, geen ruis, geen zwart in de naden | ok. |

## Diff-bewijs (`python3 scripts/check_kleur3b.py`)
- **Bevroren zones:** 0 pixels anders dan kleur3. Dat zijn:
  - het oog (x 20–33, y 10–14 en x 23–30, y 15);
  - de wenkbrauw (x 21–33, y 7–9; x 23–30, y 6; x 25–27, y 5);
  - de wang en gezichtslijn (x 33–36, y 9–19);
  - de halsband en het hele lijf (alle rijen ≥ 20);
  - alles buiten x 0–47, y 0–25.
- **Gewijzigd:** 262 pixels, allemaal binnen x 4–45, y 0–19: de kuif en de snuit.
- **Palet:** gelijk. Modus P, transparency 0.
- **Open randen:** 0.
- **Losse pixels:** 45. Het zijn bewuste details: de trappen van de naden, de lichte randen, de korrel, het opkrulrandje, de neusgaten en de gezichtsdetails die al uit kleur3 kwamen.

## Eerlijk oordeel
- **Kuif:** op 8× lezen de platen nu als korstplaten met naden en opstaande randen. Op 1× blijft het rustig.
- **Snuit:** hij heeft een duidelijke neuskap zoals bij Sandaconda en is ouder van vorm. Het oog en de wenkbrauw zijn dezelfde als in kleur3.
- **Vergelijking met kleur3:** naast elkaar oogt het gezicht niet vreemder dan kleur3.
- **Wat ik heb teruggedraaid:** de tussenstappen die wél vreemd oogden:
  - een vooruitstekende neusknop als eendenbek;
  - een 2×2-neusgat dat als oog las;
  - een lange mondlijn als krokodil.
- Ik zie geen open zwak punt.

## Lessen
- Een donker 2×2-blok midden op een licht vlak leest als oog, ook als het een neusgat moet zijn. Neusgaten worden daarom korte horizontale spleetjes, tegen de rand of tegen een schaduwrand.
- Een neusbult die vóór het snuitfront uitsteekt leest als eendenbek. De bult moet bovenop het front staan, met een dip erachter en een schaduwrand eronder.
- Een lange mondlijn vanaf de snuitpunt maakt een slangenkop al snel een krokodil, dus houd de mond kort en achteraan.
- Zoutplaten lezen pas als de naad aan twee kanten iets doet: een lichte rand aan de kant die naar het licht staat en schaduw aan de andere kant. Een naad alleen, zelfs in oker, blijft vlak.
