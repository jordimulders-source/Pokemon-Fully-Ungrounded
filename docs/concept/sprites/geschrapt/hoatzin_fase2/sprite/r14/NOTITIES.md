# Hoatzin fase 2, r14 (19 nov): reparaties op r13 (kop/oog/snavel van r13 blijven)

`sh alles.sh`: kuif14.py (kuif, verre vleugel, kruin) → rest14.py (buik, voeten, staart, nekbinnenlijn) → check → diff → vel
(r14 | r13 | model | Archeops | Braviary, kop 12x r14 | model | r13).
Pixeldiff t.o.v. r13: 327 px, **0 buiten de zones**. Per zone: kuif/verre vleugel/kruin 120, buik 29, voeten 63, staart 107, nekbinnenlijn 12. Silhouet: 41 px.
check.py: dambord 0, om-en-om 0, zwarte klonten 0.

| punt | r14 |
|---|---|
| 1 kuif | veren waaieren vanaf de kruin in de hoeken van het model: F1 linksboven (tip 6,9), F2 omhoog en iets naar links (9,9), F3 schuin rechtsboven (18,10), F4 45 graden (tip 23,7), F5 vlak naar rechts (tip 26,12), F6 naar rechts en omlaag tot (29,19). Tips van F1, F4, F5 en F6 steken omlijnd uit tegen de lucht. Kern 7, schaduwkant 6, aansluiting op de kruin zoals in r13. |
| 2 kruin | x8-18, y17-19: vlak 6, 7 linksboven, 2 alleen als sikkel rechtsonder naar de nek. |
| 3 verre vleugel | puntige veertoppen (8/3, 13/3, 17/4, 20/7); vlak 3, korte schaduwkolom 2 rechts per veer (niet doorlopend), geen 4 meer. Daardoor geen kam van lichte staafjes. Toppen: selout 2 links, zwart rechts. |
| 4 buik | bovenrand als koepel van (17,40) naar (24,36); bovenste rij D links, naar rechts C, kleine D-ovaal linksboven, B-sikkel rechts (2-3 px vanaf y42). Het D-blok en de rechte C-rij zijn weg. Het palet is niet veranderd. |
| 5 nabije voet | kleine palm (y55-56) + 3 tenen schuin gespreid: voor-links omlaag (tip 27,58), midden omlaag en iets naar links (31,57 → 30,61), rechts omlaag (37,58); tenen licht links/boven (F), E, onderkant palm 2; zwarte klauwen (26,59)-(25,60), (30,62)-(29,63), (38,59-60). Geen lichte balk op y56. |
| 6 verre teen | één onderrand: y56 = 2 (x17-22), y57 transparant; klauw blijft op (15,57-58). |
| klein | staart bijna zwart: vlak 2, twee scheidingen 1 op een derde en twee derde van de breedte, buitenlijn 1; komt los van de vleugel. Nek/vleugel: binnenlijn 1 langs de voorrand van de vleugel (x24-29, y24-35). |

Zwak: de kruin is volgens de opdracht met 6 gevuld en blijft daardoor een vrij brede bruine band onder de veren; de nabije voet is klein naast het model.
