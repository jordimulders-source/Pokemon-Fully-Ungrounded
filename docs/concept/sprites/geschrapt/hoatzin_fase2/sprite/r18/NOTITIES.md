# Hoatzin fase 2, r18 (20 nov): r17 + linkerpoot + nek los van de vleugel

Jordi op r17: "linkerpoot is helemaal niet gelukt" · "nek is nog steeds niet voldoende los van de vleugel" · "de rest klopt qua vorm".
`sh alles.sh`. Pixeldiff t.o.v. r17: 98 px, **0 buiten de zones** (poot 28, nek 70). Alpha anders: 10 px, allemaal in de poot. check.py: om-en-om 0, zwarte klonten 0 (de klont bij (20,56) is weg), dambord 51 (diagonale vleugelstrepen, zoals r17).

## Linkerpoot (verre poot, x 15–27, y 51–59)
Per spritepixel gemeten in het natieve model (`meetpoot.txt`: achtergrond/9, donker/9, gemiddeld grijs) en zo overgenomen (`bouw18.py`, tabel POOT):
- scheen y 51–53 schuin van x 26–27 naar x 25: lijn | grijs | lijn;
- bovenste teen: lijn y 54 (x 19–23), grijs y 55 x 19–26 (licht 15 op x 21–22 en 24–25 waar het model L ≥ 100 is), lijn y 56 tussen de tenen;
- onderste teen y 57 x 17–21 (grijs, 2 als schaduw), onderlijn y 58; teenpunten x 16–18; klauwen zwart (17,58) en (18,59).
- r17-rafels links/onder (x 12–16, y 59–61) weg. De bevroren buik ligt niet over de poot (gecontroleerd: geen buikpixel in de zone), dus maar één optie.

## Nek (alleen kleur binnen de r17-pixels, `nek.py`)
Per rij y 23–40: xe = begin van de lichte vleugelvoorrand (tint 5). Grenslijn = donkerste modelpixel in xe−3..xe−1 → lijn 1, doorlopend (hooguit 1 px verspringen; bij y 36→37 sluit hij aan op de buikrand).
Tussen lijn en xe → 4 (lichte vleugelrand als eigen strook). Links van de lijn, onder de kop (y ≥ 27): nek-pixels in tint 2 → 3, of 4 waar het model licht is (gem. L ≥ 96, weinig donker). Donkere modellijntjes in de nek blijven.
Telling: grenslijn 17, vleugelrand 17, nek 36.

`poot_vel.png`: linkerpoot en nek, elk r18 | r17 | pixelblad | model op 16×.
