# Picapau-evolutie: sprite r15 (keuringsreparaties 1–10 op r14)

Bron: `../r14/picapau_evo.png.keuring.md` (FAIL, 10 reparaties). Alles met de hand in `reparaties.txt`, per zone, in het formaat van `slierten.txt` (`_` = transparant). Geen formules of schaduwregels in code: `bouw_r15.py` zet alleen de pixels uit het tekstbestand op r14.

## Bevroren: bewijs (`diff_uitvoer.txt`)
- 319 px veranderd, allemaal binnen een reparatiezone; **0 px buiten de zones**.
- **Snavel P5: 0 px verschil** (36 px, de snavelregels uit `../r11/p5.txt`, rij 8-13).
- **Slierten: 0 px verschil** (97 px uit `slierten.txt`).
- Omtrek (transparant ↔ gevuld) alleen gewijzigd in: voeten 33 px, bliksem 20 px, staartlus 6 px (dunner, vloeiende bocht; reparatie 8), verre vleugel 1 px (inkeping op (9,5); reparatie 9). De omtrek van de nabije vleugel is **niet** veranderd (zie zwakke punten).

| zone | px | wat |
|---|---|---|
| 1 voeten | 64 | grijze balken weg; verre voet hoger en achter in G met twee teentjes; nabije voet met tarsus en drie tenen (links, midden omlaag, rechtsonder), elk met een klauw van G + k (2 px) |
| 2 buik | 31 | grens tussen a en b als ronde boog rond een lichtmassa linksboven; e alleen als sikkel rechtsonder (1 px bovenaan, 3 px onderaan) |
| 3 vleugelvoorrand | 62 | de 2-strook over de hele lengte is weg; glans 2 alleen bij de pols (rij 12-15, 11 px); dekveren één tint 3; binnenlijn 4 als bolle boog (3 px breed aan de uiteinden, 8-9 px in het midden) |
| 4 kop | 17 | j-strook links weg; glans van 7 px linksboven (x21-23, y3-5); schaduwsikkel 3 rechts die naar onderen breder wordt (x27-29, y7-13) |
| 5 bliksem | 36 | tand naar links (x1-5, y36-39: 2 rijen vulling met selout erboven en zwart eronder) en een inkeping rechts (rechterrand van x9 naar x7); het onderste stuk schuift 2 px naar links, zodat het een echte Z wordt |
| 6 wang | 11 | 1 px naar rechts; (23,10-12) is nu kastanje, met lucht tussen wang en snavel |
| 7 stippen | 44 | 7 ronde stippen (2×2 a + sikkel van 3 px e rechtsonder); twee stippen die in de voorrand lagen zijn verplaatst naar het vleugelvlak, de stip op (32-33,30-31) vervalt |
| 8 staartlus | 9 | grijze G op (11,48-50) nu zwart; de blokhoeken (x13-22, y54-60) zijn 2 px dik en lopen als bocht |
| 9 verre vleugel + keel | 27 | twee veertoppen ((11,2) en (8,6)) met een inkeping en een scheidingslijn 4 van de inkeping naar (13,9); de donkere vlek onder de snavel is nu keel in kastanje (3 onder de snavel, 2 eronder) |
| 10 netheid | 18 | oogrand (23,6) en (25,7) zwart; lichte randen van de handpennen zijn verschillend lang en eindigen taps (veer 1 stopt op rij 9, veer 2 op rij 11, veer 3 op rij 13); steunstaart: vlakjes samengevoegd en de tweede schachtlijn weg |

## Controle (`controle_uitvoer.txt`)
- Geen lichte kleur op de buitenrand.
- Geen losse pixels.
- Geen pixels die alleen diagonaal vastzitten.
- 15 kleuren + transparant. Er is geen kleur bijgekomen: de stiptint is de bestaande e (crèmeschaduw), dus niets samengevoegd.
- Eén tintcluster kleiner dan 3 px: G (19-20,11) in de bevroren snavel. Die was al bekend en mag.

## Bestanden
- `picapau_evo.png`, `normal.pal`, `raster.txt`.
- `reparaties.txt`: het handwerk, per zone.
- `bouw_r15.py`: zet het handwerk op r14, draait de controle en maakt de diff per zone.
- `platen.py` → `vel.png`: r15, r14, Pidgeot, Staraptor, Picapau en Raichu Gen 1 op 8×, met daaronder elk op 1× (licht en donker).
- Draaien: `python3.11 bouw_r15.py && python3.11 platen.py`.
- `bouw_r14.py` is een kopie uit r14 en hoort niet bij r15. Niet draaien: hij bouwt r14 opnieuw.

## Eerlijke zwakke punten
1. **De omtrek van de vleugelvoorrand is nog de trap van r14.** De opdracht bevriest de omtrek, behalve bij de voeten en de bliksem. Daarom zit de bolle boog alleen binnenin: de dekverenband is breed in het midden en smal aan de uiteinden, en de binnenlijn buigt. Een echt bolle buitenrand vraagt ±6-10 px bij x30-35, y17-21. Die pixels vullen de lucht tussen lijf en vleugel. Vraag eerst of dat mag; het kan als variant.
2. **De voorrand leest nog als een lichtere strook.** Er staat nu één tint (3) tegen de selout, zonder banding. Toch is de band als geheel lichter dan het vleugelvlak, net als de lichte dekveren bij Pidgeot.
3. **De voeten zijn klein en druk.** Op 8× zijn de drie tenen en klauwen te lezen. Op 1× is de nabije voet een grijs klauwtje en de verre voet een donker vlekje. De verre voet heeft geen eigen tarsus, alleen de r14-stomp (16-17,38).
4. **Het onderste stuk van de bliksem is smal** (3 px vulling plus rand), smaller dan het bovenste stuk. De tand is 2 rijen vulling dik: dat haalt de eis, maar het is het minimum. Hij lijkt op Raichu Gen 1 (breed stuk, tand opzij, smal stuk), maar staat gespiegeld omdat de lus onderaan vastzit (de pose is bevroren).
5. **De buik is nog steeds de lichtste en grootste vlek.** De sikkel en de bredere b onderaan maken hem rustiger, maar op 1× trekt hij nog altijd de meeste aandacht.
6. **De verre vleugel** heeft twee veertoppen. Op 1× kan hij nog altijd als pluk achter de kop lezen. Er staan maar twee toppen omdat de rechterrand achter de kop doorloopt.
7. **De stippen zijn 3×3 en dus iets groter dan in r14.** Het zijn er 7 in plaats van 9.
8. **Niet gekeurd.** Een onafhankelijke keuring moet nog.

Er is niets gecommit en niets verwijderd.
