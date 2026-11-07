# Poedelmot sprite ronde 7 (6 nov): alleen de achterpoten, vanuit ronde 6

Jordi (letterlijk):
- bij ronde 5: "de achterpoten zijn wel nog steeds losse aanhangels zonder verbinding";
- bij ronde 6: "voor nu prima, ik weet nog niet of ik definitief hiermee tevreden ben, maar het is veel beter, de armen mogen nog wat meer fluffy". De voorpoten blijven dus pixel voor pixel ronde 6; "meer fluffy" komt later in een wolronde.
- aanvullingen op ronde 7:
  - "ja en houd rekening met het driekwart perspectief, dus links zitten ze meer aan de onderkant dan rechts";
  - "kijk bijv naar giratina";
  - "maak ze vast aan het lichaam ook en zorg dat ze niet overdreven groot in beeld zijn".

## Wat ik zie (vóór het tekenen; `paneel_achterpoten.png`)
- **Giratina** (`graphics/pokemon/giratina/anim_front.png`, frame 1; vak "links lager, rechts hoger" op het paneel):
  - De achterpoten zijn kort en stevig en groeien direct uit de onderkant van het grote achterlijf.
  - De lijfomtrek loopt zonder onderbreking door in de dij. Er zit geen omlijning tussen lijf en poot, alleen een schaduwlijn aan de binnenkant.
  - **Links** (de verre kant) zitten de poten laag, aan de onderkant van het lijf, half eronder.
  - **Rechts** (de nabije kant) zitten ze hoger, op de zijkant van het lijf, en de voet staat verder naar buiten. Daardoor zie je rechts meer van de poot dan links.
- **foto_tak_katoen (_2):**
  - De andere poten komen uit de zijkant van het wollige lijf, onder en achter de voorpoten.
  - De wol van de flank loopt door in de poot, dus geen losse naad.
  - Links zie je alleen een pluk die onder het lijf uitsteekt. Rechts komt een poot schuin uit de zijkant naar de tak.
- **Wat in ronde 6 fout was:**
  - Links scheidde een horizontale zwarte lijn (y51, x11-14) de flanklob van P, waardoor P er los onder hing.
  - Rechts begon S onder een leeg stuk naast de lijfrand (boven S was alles transparant), dus S hing ernaast.

## Wat er gedaan is
- **Links (de verre kant, meer aan de onderkant):**
  - De zwarte lijn onder de flanklob is weg. De flank (x10-14) loopt nu recht omlaag door in **P**, zonder naad.
  - P staat recht onder het lijf, niet schuin naar buiten, en loopt af naar een punt (x11-13, y57) met 2 klauwtjes op y58.
  - **Q** komt onder de buik uit (x23-25): de onderrand van de buik gaat op y52 over in Q. Q loopt af naar een punt met 2 klauwtjes op y57, één rij hoger omdat hij verder naar achteren staat. Q is in schaduwtinten.
- **Rechts (de nabije kant, meer aan de zijkant, hoger):**
  - De lijfrand onder de vleugel krijgt een **heup** (x39-42, y48-51). Daar was alleen de omlijning van de flank.
  - De heup loopt door in **S**, die achter de rechtervoorpoot vandaan komt en afloopt naar een punt (x39-41, y58) met 2 klauwtjes op y59, op dezelfde grond als de rechtervoorpoot.
  - **R1** komt uit dezelfde heup, achter S (x42-43). Hij is donker, eindigt hoger (y56) en heeft 1 klauwtje.
- **Niet overdreven groot:**
  - S is kleiner dan in ronde 6: 5-6 px breed in plaats van 7, zonder uitwaaierende voet. R1 is maar 2 px.
  - P is 5 px breed. Rechts is dus net groter dan links.
- **Diff:**
  - Pixeldiff tegen ronde 6 is 103 px, waarvan 0 buiten de achterpootzone en 0 in de voorpoten van ronde 6 (`controle.txt`).
  - De zone is links x7-14 y51-58, onder de buik x23-25 y52-57 en rechts x37-45 y48-59.
  - Eén pixel van de flankomlijning (x39, y48) is binnenkant van de heup geworden.
  - Er zijn 0 lichte pixels op de buitenrand en 13 kleuren.

## Bestanden
- `poten.py` → `raster.txt`;
- `teken.py` → `anim_front.png`, `normal.pal`, `sprite_8x.png`;
- `controle.py` → `controle.txt`;
- `paneel.py` → `paneel_achterpoten.png`: ronde 6 en 7 op 16×, het Giratina-vak (y36-64) en de onderkant van de tak-foto;
- `keurvel.png`: het keurvel.py-vel met ronde 6, Giratina, de tak-foto, LEIDRAAD en een close-up op 16×, met het paneel eronder. De keuring staat in `keurvel.png.keuring.md`.

## Zwakke punten (eerlijk)
1. **Rij poten:**
   - Op 1× staan er nu vijf poten op een rij aan de onderkant: P, linksvoor, Q, rechtsvoor en S. Q onder de buik kan lezen als een extra (vijfde) voorpoot of als een staartje.
   - Vraag aan Jordi: mag Q onder de buik, of moet hij naast P blijven (ook "aan de onderkant")?
2. **Linkerrand:** P loopt recht onder de flanklob door, waardoor de linkerrand van de sprite een lange rechte lijn is van y46 tot y56. Dat is wel de vorm van de verre kant, maar het is een recht stuk.
3. **R1** is alleen een donker reepje.
4. **Wol:** de achterpoten zijn net zo glad als de voorpoten. Dat hoort bij de latere wolronde.
5. Een onafhankelijke keurder is nog niet geweest.
