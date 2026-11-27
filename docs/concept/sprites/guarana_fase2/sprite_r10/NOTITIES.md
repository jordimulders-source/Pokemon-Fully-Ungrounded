# Guaraná fase 2, ronde 10: buitenrand van de trossen geschulpt (op r9a én r9b)

Jordi over r8 (letterlijk): "hij is nog wat blurry maar dat zit puur in de omlijning van de fruittrossen, de vormen lijken van een afstandje
afgekapt, alsof het rechte lijnen zijn ipv rondere vruchten". r9 deed 31 px; r10 gaat verder.

Bestanden: `guarana2_r10a.png`, `guarana2_r10b.png`, `normal.pal` (= r9 = fase 1-palet), `voor_jordi_r10_8x.png` (r10a | r9a | fase 1, 8×, wit),
`afstand.png` (r10a, r9a op 1× en daarna r10a, r9a op 2×). Bouwen vanuit `guarana_fase2/`:
`python3 sprite_r10/bouw10.py && python3 sprite_r10/vel10.py && python3 sprite_r10/afstand.py`.
Meten: `recht.py SPRITE` (rechte randstukken ≥ 3 px aan de achtergrond: r9a 7 → **r10a 0**), `diag.py` (schuine trappen ≥ 4: 0), `zoom10.py` (20× uitsnede met coördinaten).
a en b krijgen exact dezelfde 108 px wijziging (gecontroleerd: a≠b alleen in de pupillen van L2/R2, zoals r8/r9). Oogwit/pupillen ongewijzigd (assert).

## Silhouet (35 px: 29 erbij, 6 weg; alle binnen 1–2 px van de oude rand)
Linkertros
- (6,25) weg: bovenste vrucht 6-6-7, inkeping (8,26).
- (5,32)(5,33)(6,34) erbij: vrucht rij 30-34 bolt uit, linkerrand 7-6-5-5-6 (was 7-6-6-6-7).
- (8,35)(8,36)(9,37)(10,38)(11,38) erbij, (13,37) weg: vrucht linksonder bolt uit (8-8-9-10, onderkant x10-11), V-inkeping (12-13,37)(12,38) naar de puntvrucht; punt 14-13-13-14.
- (19,29) weg, (19,30)(19,31) erbij, (19,32) weg, (20,33)(20,34) erbij: rechterrand was diagonaal 21-20-19-18 + recht 19-19-19-19; nu 21-20-18 | 19-19 | 18 | 20-20-19:
  L4- en L5-vrucht bollen 1 px om het oog heen, inkeping ertussen.
Rechtertros
- (57,27)(58,29)(58,30)(57,31) erbij: vrucht rij 27-31 = 57-57-58-58-57 (was 56-57-57-57-56).
- (56,33)(55,34)(56,34)(54,35)(55,35)(52,36)(53,36) erbij: vrucht rechtsonder 56-56-55-53 i.p.v. rechte diagonaal 55-54-53.
- (41,28)(42,29) erbij: R1-vrucht links 42-41-42. (43,31) erbij, (43,32) weg: kleine vrucht 44-43-44 + inkeping.
- (42,33)(42,34)(43,35) erbij: oogvrucht linksonder bolt 1 px om het oog heen.
Middelste tros
- (34,24) weg: inkeping tussen M3-oogvrucht en stam (rand was 34-34-34).

## Rand tegen blad/stam (geen silhouetwijziging, rood ↔ groen of lijnrood, 44 px)
- Middelste tros links (was recht x21 over rij 15-25, vrucht zonder lijn tegen het groen): (21,15)(22,15) → blad (inkeping), vrucht J 21-21-22 met lijnrood,
  (21,18) → blad; vrucht C: (21,22)(21,25) → blad (inkepingen), (21,23)(21,24)(22,25) lijnrood; licht verplaatst naar (23,16)(22,17)(22,23).
- Middelste tros boven: top van de bovenste vrucht 26-27 i.p.v. vlak 25-28 ((25,12) blad, (28,12)(29,12) blad = inkeping), lijnrood op (26-27,12)(24,13)(28,13)(23,14)(30,12).
- Middelste tros, onderste vrucht: linkerkant tegen de stam lijnrood (25,26)(24,27)(24,28)(25,29).
- Linkertros boven: bovenste vrucht top 8-9 i.p.v. vlak 7-10 ((7,22) blad-licht, (10,22) blad), lijnrood (8-9,22), vrucht ernaast (12,22)(13,21)(14,21).
- Rechtertros linksboven: was diagonaal 46-45-44-42-42-42; nu 46-45-45 | inkeping | 43-42 ((44,24)(42,25) blad, lijnrood (46,22)(45,23)(45,24)(43,25)).
- Rechtertros boven: vruchttoppen (47,21)(52,21)(54,21) lijnrood.

## Lijnkleur en vulling
- Hele trosrand aan de achtergrond: zwart als de achtergrond rechts/onder ligt, lijnrood links/boven (zoals fase 1); geen vul-/oogwittint op de buitenlijn.
- Oude buitenlijn die binnen komt te liggen: schaduw S aan de schaduwkant (rechts/onder), M aan de lichtkant; (6,32) licht H; (8,34) en (51,36) naad (lijnrood) tussen twee vruchten.
- Om de ogen: L4 (18,30)(18,31), L5 (19,34), rechts (43,34) worden vrucht tussen oogwit en nieuwe lijn (lijn blijft 1 px).

## Zelf bekeken (1×, 2×, 8×)
- 2×: linker- en rechtertros lezen nu als bultjes per vrucht; de middelste tros heeft niet meer de rechte rand tegen het blad. 1×: trossen iets bobbeliger, verschil klein.
- Nog niet gedaan: oogvrucht R2 rechtsboven (rand 56-56, oog met pupil a/b-verschil, niet aangeraakt); punt van de rechtertros loopt in de stam over.
- Niet keurder-getoetst.
