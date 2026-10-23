# Olinguito ronde 14: dichtbije achterpoot naar achteren, vloeiender romp (basis ronde 13)

Jordi op ronde 13: de 3/4-constructie klopt, het Escher-effect is weg. Twee kleine punten:
1. "De poot rechtsvoor mag nog iets verder naar achteren."
2. "Het lichaam is wat rechthoekiger geworden; het gaat niet zo geleidelijk over als bij andere sprites, zie Mightyena."

Alleen `lijf`, `been_voor` en `been_achter` in `bron/delen_abs.txt` zijn veranderd. Kop, masker, ogen, mond, palet, armen, klauwen, staart en animatie zijn pixel voor pixel ronde 13.

## 1. Poot
- Verschoven: de **dichtbije achterpoot** (rechts in beeld, voorgrond; deel `been_voor`), **3 px naar rechts**, ongewijzigd getekend. Jordi heeft bevestigd dat deze poot bedoeld was.
- De dij valt nu over de achterkant van de heup en vormt het onderste deel van de ronde achterkant (x57 op het breedste punt); de voet staat onder de heup in plaats van halverwege de buik.
- De **verre achterpoot** (`been_achter`) ging 1 px mee naar rechts. Hij blijft links van en hoger dan de dichtbije (voet y52 tegen y54) en komt nu onder de ingesnoerde buik vandaan, zodat de verhouding klopt.
- Het gat tussen voorklauwen en achterpoten is groter; het dier staat langer.

## 2. Romp (Mightyena als voorbeeld)
In Mightyena (`graphics/pokemon/mightyena/anim_front.png`) zakt de borst diep tussen de voorpoten (y43–44), stijgt de buiklijn dan in een holle curve naar een hoog ingetrokken lies (y41–42) en valt pas bij de dij weer naar beneden; de rug loopt in één zachte boog van schouder naar staartaanzet. Overgenomen:
- **Buiklijn als S-curve:** borst laagst (y49), daarna stijgt de onderrand met toenemende stappen naar achteren (eindes per rij: y48 → x33, y47 → x37, y46 → x40, y45 → x42, y44 → x44; stappen 4,3,2,1 i.p.v. de vlakke rij y47 van x34–40 in ronde 13). De lies ligt 3 rijen hoger dan in ronde 13 en sluit aan op de voorkant van de dij.
- **Rug als boog:** nek y34 → heup y32 (top 3 px breed, geen plat stuk) → ronde achterkant met stappen 2,2,1,1,0,1,0,1 naar x56 en de dij tot x57. Geen verticale rechte kont meer zoals ronde 13 (x53–54 over 7 rijen).
- Schaduw volgt de nieuwe vorm: lichte band over het midden, schaduw onder de kop, de buik en de achterkant.

## §0-checklist (SPRITING.md)
1. **Lichaam én blik diagonaal:** ok; ongewijzigde 3/4-boon van ronde 13, verre poten links-hoger en in schaduw.
2. **Geteld en verbonden:** ok; 4 poten, elk onder zijn schouder of heup; bouw9: geen open randen in beide frames.
3. **Geen rechte lijnen:** ok; bouw9 meldt geen rechte randstukken > 4 px (een eerste versie had er een van 5 px bovenop de heup; opgelost).
4. **Ogen geïntegreerd:** ok (ongewijzigd).
5. **Silhouet op 1×:** ok; leest langer en slanker, met een duidelijke taille.
6. **Formaat:** 1096 / 1113 px (ronde 13: 1068 / 1084), binnen 1000–1100 voor frame 1.
7. **Pose niet stijf:** ok; sluiphouding, poten op vier hoogtes.

## Controle (bouw9)
- Open randen: geen. Rechte randstukken > 4 px: geen. Zwart-aandeel rand 0,59 / 0,59.

## Bestanden
- `anim_front.png`, `normal.pal` (= ronde 13), `compare.png` (boven: ronde 13 en 14, beide frames, 1× en 3×; onder: Mightyena, Poochyena).
- `bron/delen_abs.txt` is de bron. Bouwen: `sh bron/bouw.sh <ronde14-map> [preview.png]`; `python3 bron/vergelijk14.py <repo-root>` maakt compare.png.
