# Cuyby ronde 5: C6 (+ variant asym)

Basis: `../ronde4/anim_front.png` (goedgekeurd; de PNG is leidend, `ronde4/bron` bouwt nog de oogversie). Openstaand uit `checklist_keuring/KEURING.md` §1. Oogwijziging niet opnieuw gedaan (afgekeurd door Jordi). Palet ongewijzigd, transparency=0. Frame 2 = dezelfde wijziging 1 rij hoger (zoals ronde 3–4). Script: `bron/cuyby5.py` (rekent het bewijs uit).

| Punt | Wat | Waar (frame 1) | Pixels |
|---|---|---|---|
| C6 linker voetkussen 1 px hoger | Kussen `cd` van (26–27,45) naar y44 met omlijning eromheen; (26,43) wordt bovenrand `1`. Op y45 lopen de zijlobben 1 px door (`4` links op x25, `3` midden op x28), zodat onder het kussen alleen zijn eigen onderrand `11` staat. Op y46 krijgen de lobben hun onderrand (x25, x28) en ontstaat een inkeping van 2 px onder het kussen. | x25–28, y43–46 | 13 |

**Pixeldiff buiten de zone: 0** (beide frames). Open randen: 0 nieuw. Oppervlak blijft 794.
**Waarom het nu geen zwarte balk is:** de vorige poging liet op y45 vier keer `1` naast elkaar staan (x25–28). Nu lopen de lobben door tot naast het kussen, en het zwart onder het kussen is maar 2 px breed met een inkeping eronder. Het kussen ligt dus 1 px hoger in een kuiltje, net als het rechter maar dan hoger.
**Zelfcheck** (1× en 3× naast ronde 4, `checklist_keuring/TOEGEPAST2.png`): op 3× staat het linker kussen zichtbaar hoger dan het rechter en is het niet zwaarder geworden. Op 1× zie je het nauwelijks. Gezicht en de rest zijn ongewijzigd.

## variant_asym/ (klein, ter keuze)
Ronde 5 plus A5. De rechter (schaduw)flank hangt 1 px verder uit op y33–39: de oude randpixel `9` wordt `8` en er komt een nieuwe `9` naast (frame 2 1 rij hoger). 14 px per frame. De bovenkant van de bol (y28–32) en de pootjes blijven gelijk. Script: `bron/cuyby5_asym.py`.
- Symmetrie: 0,927 (ronde 4) → 0,932 (ronde 5) → **0,916** (variant). Zo klein gehouden als gevraagd; dat haalt de bolgrens niet, maar dat doen Jigglypuff en Wooloo ook niet.
- Op 3× oogt de bol rechtsonder iets voller, alsof hij op zijn rechterkant leunt. Op 1× zie je het nauwelijks.

## Lessen
- Een kussen of detail 1 px verschuiven naar de rand: laat de buurvorm (lob, vacht) 1 px meelopen in plaats van de lege plek met omlijning te vullen. Anders ontstaat een zwarte balk.
- Pixeldiff met zones plus een check op open randen (randkleur moet een omlijningskleur zijn) in één script (`bron/fu.py`, `report()`): dat geeft het bewijs in één regel.
- Verplaatst blok raakt een buurdeel (alpaca-handschoen en achtervoet): sluit de pixels van dat buurdeel expliciet uit van het verplaatste masker.
