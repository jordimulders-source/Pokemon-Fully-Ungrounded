# Nachtaap fase 2: kleursprite ronde 9 (kené volgens de 3D-projectie)

Basis is ronde 8, variant B. Jordi: "b is wel mooier, maar klopt het patroon nog? is het niet teveel naar ons perspectief gevormd?"

De loop van het patroon is nu de projectie van de dikke kené op het 3D-poppetje (`silhouet/kene_dik_64.npy`). Ik heb niets herschikt. Alleen dunne stukken zijn langs dezelfde loop verdikt, en hapjes en ruis zijn opgeschoond. Elke toevoeging staat met een reden in `bron/kene.py` (lijsten `EXTRA` en `RUIS`).

## Bewijs (`bron/diff_uitvoer.txt`)
- **Alpha-diff:** 0 (1459 px, zowel tegen de `.txt` als tegen de `.npy`).
- **Open randen:** 0. Er zijn 0 losse pixels in de zone.
- **Palet:** gelijk aan variant B.
- **Diff buiten de zone t.o.v. variant B:** 0. In de zone zijn 211 px gewijzigd.
- **Patroon: 186 px.**
  - 39 daarvan vallen buiten de projectie. Dat komt alleen door de verdikking (voorste punt, band 2 omlaag, band 3, de splitsing) en het dichten van de hapjes.
  - 27 projectiepixels zijn niet gebruikt. Daarvan liggen er 26 op de omlijning (die blijft staan) en 1 is ruis (32,26).
  - Gevolg: de middenlijn op de rugtop valt in de projectie grotendeels samen met de bovenste omlijning. Zichtbaar blijven het voorste stuk (achter de kop), de aanzetten van de banden en de splitsing bij de staartwortel.
- **Kleinste doorsnede:** ≥ 3 px overal, behalve 4 px op twee uiteinden die tegen de omlijning lopen. Daar is het 2 px:
  - de top van band 2 bij de ruggengraat, (33–34, 27);
  - band 3 aan de rand van het achterlijf, (46, 35–36).
  - Verdikken kan daar alleen door de omlijning te overschrijven, of door band 1 en 2 tegen elkaar te laten lopen.

## Kleur
- Vlak maanzilver (idx 15) op de lichtkant, vlak lila (idx 6) in de lijfschaduw.
- Geen bevel.
- 1 px basis (idx 4) tussen het patroon en het vachthooglicht.

## Wat het vel laat zien
- **Variant B:** de zijbanden lopen schuin naar voren.
- **Ronde 9:** de banden lopen vanaf de rug vrijwel recht over de flank omlaag (band 1 bij x 30–33, band 2 bij x 38–42), zoals in 3D. Band 3 is een smalle strook langs de achterkant van het achterlijf. Vooraan buigt de rugband over de schouder naar achter de kop.
- Tussen band 2 en band 3 zit onderaan maar 1 px vacht (x 43, y 39–41). Dat komt uit de projectie, waar ze ook dicht bij elkaar liggen; band 3 kon alleen naar binnen dikker.

## Lessen
- **Een patroon op een bol eerst in 3D leggen en projecteren.** In beeld getekende banden volgen het perspectief van de kijker, niet het lijf (Jordi: "teveel naar ons perspectief gevormd").
- **Een projectie op 64 px heeft dunne stukken en pixels op de omlijning.** Verdik langs dezelfde loop en tel apart hoeveel pixels buiten de projectie vallen. Zo blijft de loop controleerbaar.
