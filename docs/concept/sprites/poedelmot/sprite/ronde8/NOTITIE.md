# Poedelmot sprite ronde 8 (6 nov): alleen de achterpoten + de onderrand van het lijf, vanuit ronde 6

Jordi over ronde 7 (letterlijk): "je luistert niet, het is driekwart perspectief, dus de poot links hoort helemaal niet zover naar links te zitten. Dan valt die maar deels buiten beeld. Het perspectief wat je hebt gedaan is dus juist helemaal niet zoals giratina. Daarnaast zitten de poten niet vast aan het lichaam zoals in elke bronfoto maar heb je maar weer wat verzonnen en ze los vastgemaakt. Dit is echt waardeloos wat je doet en dit moet beter"

Eerder (letterlijk): "stop de achterste poten maar weg als bij giratina, maakt niet uit dat je ze maar half ziet" / "die achterste 4 functioneren zoals we hier willen" / "maak ze vast aan het lichaam ook en zorg dat ze niet overdreven groot in beeld zijn" / "houd rekening met het driekwart perspectief, dus links zitten ze meer aan de onderkant dan rechts" / "kijk bijv naar giratina".

Basis: ronde 6. Ronde 7 is niet gebruikt.

## Eerst kijken (`paneel_achterpoten.png`, onderste rij van `keurvel.png`)
- **Giratina** (`graphics/pokemon/giratina/anim_front.png`, frame 1, op 8× en 16× bekeken):
  - Linkervoorpoot x10-20, rechtervoorpoot x35-48, beide met de voet onderaan (y55-63).
  - **Verre (linker) achterpoten:** geen poot links naast het lijf. Alleen een donker stuk voet (gouden klauw in schaduw) komt onder de buik uit, tussen de voorpoten (x17-33, y52-58), half achter de linkervoorpoot en tegen de rechtervoorpoot aan. Die voet staat hoger (y56-58) dan de voorvoeten (y61-63).
  - **Nabije (rechter) achterpoten:** rechts achter de rechtervoorpoot (x48-60, y48-58), direct onder het achterlijf dat naar rechts doorloopt tot x60. Ze staan ook hoger dan de rechtervoorvoet.
  - Alle poten zijn kort en dik. Het lijf komt laag; de poten zijn stompjes/voeten eronder. Er is geen omlijning tussen lijf en dij, alleen een schaduwlijn waar de poot vóór iets anders valt.
- **foto_tak_katoen (_2 is dezelfde foto):**
  - De wol van het lijf loopt zonder grens door in de poten; elke poot is een voortzetting van de wolmassa, geen los staafje.
  - Links zie je achter de voorste linkerpoot alleen een plukje van een poot (onderaan, x≈285-300 op 750 px). Rechts komen de poten uit de wollige flank, achter elkaar, onder het lijf.
- **vilt_poten_LEIDRAAD:** de poten groeien uit de wol van het lijf; geen naad of aanhechting, de wol loopt door tot in de poot.
- **Fout in ronde 6/7:** links een zwarte lijn tussen flanklob en P (P hing eronder) en P stond ver naar links naast het lijf; rechts hing S naast een leeg stuk (ronde 6) of aan een smal heupje (ronde 7).

## Wat er gedaan is
- **Links (verre kant):** P is weg. De flanklob van ronde 6 sluit onderaan af met wol op rij 51 en een onderrand op rij 52 (x11-15), tegen de linkervoorpoot aan. Er staat geen poot meer links naast het lijf.
- **Verre achterpoot (het stukje dat je ziet, zoals bij Giratina):** de omlijning onder de buik (rij 52, x24-27) is wol geworden. De buik loopt zo door in een kort stompje (x24-29, y52-56), in schaduwtinten, tegen de rechtervoorpoot aan, met een punt (`121`) en 2 klauwtjes op y57: één rij hoger dan de linkervoorpoot (y58). De tweede verre achterpoot is niet te zien.
- **Rechts (nabije kant):** het lijf loopt door in een **achterlijf** onder de vleugel, achter de rechterarm (x39-45, y45-52). Uit die massa komen zonder naad:
  - **S**, direct achter de rechtervoorpoot (x36-40), kort, punt op y57, 2 klauwtjes op y58 (één rij hoger dan de rechtervoorpoot, y59);
  - **R1**, daarachter (x42-44), kleiner en donkerder, met een tapse binnenlijn waar S ervoor valt, punt op y55, 2 klauwtjes op y56.
- **Niet overdreven groot:** S is 5 px breed, R1 3 px, het verre stompje 4-5 px; de sprite wordt rechts niet breder dan ronde 6 (x45).
- **Toets naast Giratina (1×, 8×, 16×):** links verborgen, alleen een stukje voet tussen de voorpoten; rechts zichtbaar achter de rechtervoorpoot onder een doorlopend achterlijf. Elke achterpoot loopt in de wol van het lijf over, zonder omlijning ertussen.

## Diff (`controle.txt`, `diff.png`)
- 158 px gewijzigd tegen ronde 6: 0 buiten de achterpootzone, 0 in de voorpoten van ronde 6.
- Boven rij 51: 27 px gewijzigd, allemaal pixels die in ronde 6 transparant waren (het nieuwe achterlijf onder de vleugel); 0 bestaande pixels veranderd.
- `diff.png`: grijs = ronde 6, blauw = voorpoten (ongewijzigd), rood = gewijzigd.
- 0 lichte pixels op de buitenrand, 13 kleuren.

## Bestanden
- `poten.py` → `raster.txt`; `teken.py` → `anim_front.png`, `normal.pal`, `sprite_8x.png`; `controle.py` → `controle.txt`, `diff.png`;
- `paneel.py` → `paneel_achterpoten.png` (ronde 6, ronde 8 en Giratina op 16×, tak-foto, LEIDRAAD);
- `keurvel.png` (keurvel.py met ronde 6, Giratina, tak-foto, LEIDRAAD, close-up 16×; paneel eronder); keuring in `keurvel.png.keuring.md`.

## Zwakke punten (eerlijk)
1. **Verre achterpoot tussen de voorpoten:** zo staat hij bij Giratina, maar op 1× kan het stompje lezen als een derde, kleine voorpoot. Vraag aan Jordi of dit het "deels buiten beeld" is dat hij bedoelt.
2. **Flanklob links:** de lob van ronde 6 (x10-15) steekt nu als een blok uit onder links, met een vrij rechte onderrand (rij 52, 5 px). Dat is lijfvorm van ronde 6, niet aangepast.
3. **Inham tussen arm en vleugel** (x39-42, y41-44) is transparant gebleven (boven de onderrand, niet aangeraakt); het achterlijf sluit er nu onder aan.
4. **Wol:** de achterpoten zijn net zo glad als de voorpoten (hoort bij de latere wolronde, "de armen mogen nog wat meer fluffy").
5. Een onafhankelijke keurder is nog niet geweest.
