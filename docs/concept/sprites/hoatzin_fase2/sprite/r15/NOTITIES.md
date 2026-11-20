# Hoatzin fase 2, r15 (20 nov): reparaties op r14 (kop, oog, snavel, nek, vleugel en buikkleur blijven)

`sh alles.sh`: kuif15.py (verre vleugel, kuifplukken, kruin) → rest15.py (buiktop, voeten, staart, nekrand) → check → diff → vel
(r15 | r14 | model | Archeops | Braviary, kop 12x r15 | model | r14). Hulpjes: zoom.py, modelgrid.py, kijk.py, toon.py (npy bekijken).
Pixeldiff t.o.v. r14: 354 px, **0 buiten de zones**. Per zone: verre vleugel/kuif/kruin 196, buiktop 8, voeten 94, staart 53, nekrand 3. Silhouet: 56 px.
check.py: dambord 0, om-en-om 0, zwarte klonten 0. 16 kleuren, palet ongewijzigd.

| punt | r15 |
|---|---|
| 1 verre vleugel | 4 ronde toppen (x8-9, 12-13, 16-17, 20-21), elk top 4 linksboven en 3; scheidingen 2 (2-3 px vanaf de inkeping, ongelijk lang); lijn 2 boven/links, 1 alleen op de aflopende rechterrand. Geen 1 meer binnenin. |
| 2 kuif | 6 plukken met verschillende hoek en lengte: P1 steil linksboven (tip 5,8, steekt uit), P2 kort recht omhoog (tip 11,9), P6 kort ±60° (tip 17,7), P3 lang 45° (tip 21-23,7, steekt uit), P4 vlak naar rechts (tip 25-26,12, steekt uit), P5 rechts-omlaag (loopt over in de punt 28,19, steekt uit). Per pluk 7 boven/links, 6 kern, 2 alleen onder/rechts (bij P1/P2 alleen bij de voet). Tips 2-3 px bruin met 1 aan het eind/onder. |
| 3 kruin | koepel x7-20 y14-19: 7 linksboven, 6 kern, twee korte verticale haarstreepjes 7 (x12 en x17); 2 als gebogen sikkel (18,17)-(19-22,18)-(18-20,19)-(15-18,20); (9-10,20) bruin i.p.v. 2. |
| 4/7 nabije voet | naar de modelmaat (x23-38, y55-63): palm + 3 tenen van 3 rijen (E/D/2), omlijnd: links schuin omlaag, midden omlaag en iets naar links, rechts schuin omlaag. Klauwen 2 px diagonaal: (23,59)-(22,60), (28,62)-(27,63), (38,58)-(39,59). (36,59),(37,59) en de klauwbalk (26-29,59) weg. |
| 5 verre teen | y54 lijn 1, y55 E, y56 2 (x17-22); (16,56) diagonaal naar de klauw (15,57-58). De korte verre teen omlaag (x22-24, y57-61) is weg: die viel onder de nabije linker teen/klauw. |
| 6 buiktop | koepel: y35 x22-23, y36 x20-25 (B C C B B A), (19,37) C. |
| klein | staart: vlak 2, lichte rand 3 links, twee doorlopende veerlijnen 1 met elk een 3-rand rechts ervan (geen dambord, geen dubbele zwarte trapjes meer). Nekrand 5 onderbroken op y34 (x17-19 → 4). Staartrand naast de rechter teen (40,57-58) in 1. |

Zwak / eerlijk: de kruinkoepel blijft een vrij brede bruine massa (minder strepig dan het model); de verre teen omlaag uit het model ontbreekt; de nabije voet leest op 8x nog wat als een kruis (tenen weinig gebogen).
