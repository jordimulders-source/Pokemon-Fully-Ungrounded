# Nachtaap fase 2: kleursprite ronde 8 (F1 uit `../ronde7/EINDKEURING.md`)

Basis is ronde 7. Alleen de kené is veranderd, in de zone x 17–49, y 24–50. De kop (x ≤ 24, y ≥ 36), de armen, de staart en de omlijning zijn niet aangeraakt.

Er zijn twee versies met dezelfde vorm:
- **ronde 8** (`nachtaap.png`): het palet is gelijk aan ronde 7.
- **variant B** (`variant_eigen_kleur/nachtaap.png`): het patroon heeft een eigen kleurgroep (regel 1 van de keurder).

## Bewijs (`bron/diff_uitvoer.txt`, `bron/bouw_uitvoer.txt`)
- **Alpha-diff:** 0 voor beide (1459 px, zowel tegen de `.txt` als tegen de `.npy`).
- **Open randen:** 0 voor beide.
- **Losse pixels in de zone:** 0.
- **Ronde 8:**
  - diff buiten de zone t.o.v. ronde 7: 0, palet gelijk;
  - in de zone zijn 266 px gewijzigd: de oude kené eruit plus het nieuwe patroon van **186 px**, binnen het budget van 150–190.
- **Variant B:**
  - buiten de zone zijn alleen de 9 verre vingertoppen veranderd, van idx 15 (`f`, e2c8a0) naar idx 13 (`e`, d0b696, de crème-schaduw). Dat was nodig om index 15 vrij te maken; de handen lezen hetzelfde (op 6× nagekeken);
  - idx 15 is nu het patroon: **maanzilver a8c4ec**.
- **Kleinste doorsnede** (`bron/doorsnede.py`: per patroonpixel de kortste rij- of kolomrun door die pixel): **3 px**, in beide versies. Er zitten 0 pixels onder 3 px in.

## Vorm (naar het poppetje)
De banden staan per rij met de hand in `bron/kene.py` (lijsten `M`, `B1`, `B2`, `BC`).

- **Middenlijn op de ruggengraat:** 3 px dik, 1–2 px onder de bovencontour.
  - Hij loopt van achter de kop (x 17–19, y 31–33) over de top (x 23–32, y 27–29) naar de staartwortel (x 40–42, y 32–34).
  - De treden zijn 2–3 px breed en 1–2 px hoog.
- **Zijbanden over de nabije flank,** elk 3 px dik:
  - Bovenaan liggen ze vlakker en lager worden ze steiler: de x verschuift +1, +1, +1 per blok van 2–4 rijen. Zo lopen ze om de bol.
  - Tussen de banden zit 3–4 px vacht.

| Band | Waar | Eindigt op |
|---|---|---|
| Band 1 | x 24–29 | y 41 |
| Band 2 | x 31–35 | y 43 |
| Band C | x 41–44, achterlijf (vanaf het eind van de middenlijn) | y 45 |

  - De eindpunten liggen dus op verschillende hoogtes.
- **Stompjes op de verre kant:** niet gedaan. Boven de middenlijn zit maar 1–2 px tot de omlijning, dus een stompje zou de omlijning raken.
- **Een vierde band:** past niet. De flank is ±22 px breed: 3 banden van 3 px met 3–4 px ertussen vullen hem al.

## Kleur
- **Geen bevel.** Op de lichtkant is de band vlak idx 7 (in variant B idx 15). Waar het lijf in de schaduw ligt (`s`), is de hele band vlak idx 6. De overgang volgt de evenaar van de bol.
- **Rond de banden 1 px basis (idx 4)** overal waar het vachthooglicht (idx 5) ze zou raken.
- **Variant B:** maanzilver (idx 15, luma ±191) op de lichtkant en idx 6 in de schaduw. Er was maar één paletslot vrij, dus de schaduwtint van het patroon is het bestaande lila.

## Voor Jordi (smaak, geen gebrek)
- Het patroon is nu duidelijk en vlak. Daardoor oogt de rug veel drukker dan in ronde 7: op 1× leest hij als een gestreept dier.
- Variant B maakt het patroon een eigen kleur, passend bij de maan. Ronde 8 houdt het lila van het poppetje.

## Lessen
- **Meet de dikte van een patroon met een script** (de kortste rij- of kolomrun per pixel). Treden van 2 px aan een schuine band geven zonder dat je het ziet 2-px-doorsneden.
- **Een patroon dat tegen de omlijning loopt, verliest daar zijn bovenste pixel** (de omlijning blijft staan). Leg treden daarom niet direct onder een rand die stijgt of daalt.
- **Een paletslot vrijmaken:** een bijna-gelijke tint met weinig pixels (hier 9) samenvoegen met de dichtstbijzijnde tint uit dezelfde groep. Controleer daarna op 6× of het onderdeel hetzelfde leest.
